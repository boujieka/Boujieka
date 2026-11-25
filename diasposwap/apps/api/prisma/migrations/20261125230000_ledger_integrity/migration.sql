-- Ledger integrity rules enforced by PostgreSQL itself (defence in depth: they hold even if application code is wrong).

-- 1. No zero postings.
ALTER TABLE "LedgerPosting" ADD CONSTRAINT "LedgerPosting_amount_nonzero" CHECK ("amount" <> 0);

-- 2. (A reversal references an existing entry at most once: FK + UNIQUE on "reversesId", declared in schema.prisma.)

-- 3. Append-only: no UPDATE / DELETE / TRUNCATE on ledger tables. Corrections are reversal entries.
CREATE FUNCTION ledger_reject_change() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'ledger is append-only: % on % is not allowed', TG_OP, TG_TABLE_NAME
    USING ERRCODE = 'restrict_violation';
END $$;

CREATE TRIGGER "LedgerEntry_append_only" BEFORE UPDATE OR DELETE ON "LedgerEntry"
  FOR EACH ROW EXECUTE FUNCTION ledger_reject_change();
CREATE TRIGGER "LedgerPosting_append_only" BEFORE UPDATE OR DELETE ON "LedgerPosting"
  FOR EACH ROW EXECUTE FUNCTION ledger_reject_change();
CREATE TRIGGER "LedgerEntry_no_truncate" BEFORE TRUNCATE ON "LedgerEntry"
  FOR EACH STATEMENT EXECUTE FUNCTION ledger_reject_change();
CREATE TRIGGER "LedgerPosting_no_truncate" BEFORE TRUNCATE ON "LedgerPosting"
  FOR EACH STATEMENT EXECUTE FUNCTION ledger_reject_change();

-- 4. Postings may only be added to an entry created in the same transaction (history cannot be extended later).
--    Compares the entry row's xmin with the current top-level transaction id (no savepoints are used by the app).
CREATE FUNCTION ledger_posting_same_tx() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE entry_xmin text;
BEGIN
  SELECT xmin::text INTO entry_xmin FROM "LedgerEntry" WHERE "id" = NEW."entryId";
  IF entry_xmin IS DISTINCT FROM (txid_current() % 4294967296)::text THEN
    RAISE EXCEPTION 'postings can only be added to a ledger entry in the transaction that created it (entry %)', NEW."entryId"
      USING ERRCODE = 'restrict_violation';
  END IF;
  RETURN NEW;
END $$;

CREATE TRIGGER "LedgerPosting_same_tx" BEFORE INSERT ON "LedgerPosting"
  FOR EACH ROW EXECUTE FUNCTION ledger_posting_same_tx();

-- 5. Double entry: at COMMIT, every touched entry has >= 2 postings and sums to zero in each currency.
CREATE FUNCTION ledger_check_balanced() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE n int; bad record;
BEGIN
  SELECT count(*) INTO n FROM "LedgerPosting" WHERE "entryId" = NEW."entryId";
  IF n < 2 THEN
    RAISE EXCEPTION 'ledger entry % needs at least two postings', NEW."entryId" USING ERRCODE = 'check_violation';
  END IF;
  SELECT "currency", sum("amount") AS total INTO bad
    FROM "LedgerPosting" WHERE "entryId" = NEW."entryId"
    GROUP BY "currency" HAVING sum("amount") <> 0 LIMIT 1;
  IF FOUND THEN
    RAISE EXCEPTION 'ledger entry % is unbalanced in %: %', NEW."entryId", bad."currency", bad.total
      USING ERRCODE = 'check_violation';
  END IF;
  RETURN NULL;
END $$;

CREATE CONSTRAINT TRIGGER "LedgerPosting_balanced" AFTER INSERT ON "LedgerPosting"
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION ledger_check_balanced();

-- 6. An entry with no postings at all is caught too.
CREATE FUNCTION ledger_entry_has_postings() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM "LedgerPosting" WHERE "entryId" = NEW."id") THEN
    RAISE EXCEPTION 'ledger entry % has no postings', NEW."id" USING ERRCODE = 'check_violation';
  END IF;
  RETURN NULL;
END $$;

CREATE CONSTRAINT TRIGGER "LedgerEntry_has_postings" AFTER INSERT ON "LedgerEntry"
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION ledger_entry_has_postings();
