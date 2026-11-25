-- CreateSchema
CREATE SCHEMA IF NOT EXISTS "public";

-- CreateEnum
CREATE TYPE "KycLevel" AS ENUM ('NONE', 'BASIC', 'VERIFIED', 'ENHANCED');

-- CreateEnum
CREATE TYPE "ComplianceStatus" AS ENUM ('NOT_CHECKED', 'CLEARED', 'REVIEW', 'BLOCKED');

-- CreateEnum
CREATE TYPE "TransferState" AS ENUM ('DRAFT', 'QUOTED', 'PENDING_VERIFICATION', 'PENDING_FUNDING', 'FUNDED', 'QUEUED', 'PARTIALLY_MATCHED', 'MATCHED', 'SETTLEMENT_PENDING', 'SETTLED', 'FAILED', 'EXPIRED', 'CANCELLED', 'REFUND_PENDING', 'REFUNDED', 'DISPUTED');

-- CreateEnum
CREATE TYPE "CorridorMode" AS ENUM ('SIMULATION', 'DISABLED', 'LIVE');

-- CreateEnum
CREATE TYPE "ProviderOpKind" AS ENUM ('COLLECTION', 'PAYOUT', 'REFUND');

-- CreateEnum
CREATE TYPE "ProviderOpStatus" AS ENUM ('PENDING', 'SUCCEEDED', 'FAILED');

-- CreateEnum
CREATE TYPE "PayoutStatus" AS ENUM ('PENDING', 'SUCCEEDED', 'FAILED', 'EXCEPTION');

-- CreateEnum
CREATE TYPE "AccountType" AS ENUM ('COLLECTION', 'CUSTOMER_FUNDS', 'BENEFICIARY_PAYABLE', 'FEE_REVENUE', 'REFUND_PAYABLE', 'CLEARING', 'RECONCILIATION', 'FX_DIFFERENCE');

-- CreateEnum
CREATE TYPE "AdminRole" AS ENUM ('OPS', 'COMPLIANCE', 'FINANCE', 'AUDITOR', 'SUPERADMIN');

-- CreateTable
CREATE TABLE "User" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "phoneE164" TEXT NOT NULL,
    "fullName" TEXT NOT NULL,
    "countryCode" CHAR(2) NOT NULL,
    "kycLevel" "KycLevel" NOT NULL DEFAULT 'NONE',
    "pep" BOOLEAN NOT NULL DEFAULT false,
    "emailVerified" BOOLEAN NOT NULL DEFAULT false,
    "phoneVerified" BOOLEAN NOT NULL DEFAULT false,
    "mfaEnabled" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deletedAt" TIMESTAMP(3),

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Session" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "tokenHash" TEXT NOT NULL,
    "deviceId" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expiresAt" TIMESTAMP(3) NOT NULL,
    "revokedAt" TIMESTAMP(3),

    CONSTRAINT "Session_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "KycCheck" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "provider" TEXT NOT NULL,
    "level" "KycLevel" NOT NULL,
    "result" TEXT NOT NULL,
    "simulated" BOOLEAN NOT NULL DEFAULT true,
    "checkedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "KycCheck_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Beneficiary" (
    "id" TEXT NOT NULL,
    "ownerId" TEXT NOT NULL,
    "fullName" TEXT NOT NULL,
    "countryCode" CHAR(2) NOT NULL,
    "accountRefEnc" BYTEA NOT NULL,
    "accountMasked" TEXT NOT NULL,
    "verified" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Beneficiary_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Corridor" (
    "id" TEXT NOT NULL,
    "countryA" CHAR(2) NOT NULL,
    "countryB" CHAR(2) NOT NULL,
    "mode" "CorridorMode" NOT NULL DEFAULT 'SIMULATION',
    "maxOrderEurCents" BIGINT NOT NULL,
    "minFillEurCents" BIGINT NOT NULL,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "updatedBy" TEXT NOT NULL,

    CONSTRAINT "Corridor_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "FxRate" (
    "id" TEXT NOT NULL,
    "base" CHAR(3) NOT NULL,
    "quote" CHAR(3) NOT NULL,
    "num" BIGINT NOT NULL,
    "den" BIGINT NOT NULL,
    "source" TEXT NOT NULL,
    "asOf" TIMESTAMP(3) NOT NULL,
    "validFor" INTEGER NOT NULL,

    CONSTRAINT "FxRate_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Quote" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "fromCountry" CHAR(2) NOT NULL,
    "toCountry" CHAR(2) NOT NULL,
    "sendCurrency" CHAR(3) NOT NULL,
    "receiveCurrency" CHAR(3) NOT NULL,
    "principal" BIGINT NOT NULL,
    "fee" BIGINT NOT NULL,
    "rateNum" BIGINT NOT NULL,
    "rateDen" BIGINT NOT NULL,
    "estimatedReceive" BIGINT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expiresAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Quote_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TransferOrder" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "quoteId" TEXT NOT NULL,
    "beneficiaryId" TEXT NOT NULL,
    "idempotencyKey" TEXT NOT NULL,
    "fromCountry" CHAR(2) NOT NULL,
    "toCountry" CHAR(2) NOT NULL,
    "sendCurrency" CHAR(3) NOT NULL,
    "receiveCurrency" CHAR(3) NOT NULL,
    "principal" BIGINT NOT NULL,
    "remaining" BIGINT NOT NULL,
    "fee" BIGINT NOT NULL,
    "refundedPrincipal" BIGINT NOT NULL DEFAULT 0,
    "refundedFee" BIGINT NOT NULL DEFAULT 0,
    "allowPartial" BOOLEAN NOT NULL DEFAULT true,
    "state" "TransferState" NOT NULL DEFAULT 'DRAFT',
    "compliance" "ComplianceStatus" NOT NULL DEFAULT 'NOT_CHECKED',
    "version" INTEGER NOT NULL DEFAULT 0,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expiresAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "TransferOrder_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "StateChange" (
    "id" BIGSERIAL NOT NULL,
    "orderId" TEXT NOT NULL,
    "from" "TransferState" NOT NULL,
    "to" "TransferState" NOT NULL,
    "reason" TEXT NOT NULL,
    "actor" TEXT NOT NULL,
    "at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "StateChange_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "MatchRun" (
    "id" TEXT NOT NULL,
    "startedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "finishedAt" TIMESTAMP(3),
    "engineVer" TEXT NOT NULL,

    CONSTRAINT "MatchRun_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Allocation" (
    "id" TEXT NOT NULL,
    "runId" TEXT NOT NULL,
    "kind" TEXT NOT NULL,
    "takerOrderId" TEXT NOT NULL,
    "makerOrderId" TEXT NOT NULL,
    "takerAmount" BIGINT NOT NULL,
    "takerCurrency" CHAR(3) NOT NULL,
    "makerAmount" BIGINT NOT NULL,
    "makerCurrency" CHAR(3) NOT NULL,
    "rateNum" BIGINT NOT NULL,
    "rateDen" BIGINT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Allocation_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ProviderOperation" (
    "id" TEXT NOT NULL,
    "providerId" TEXT NOT NULL,
    "providerRef" TEXT NOT NULL,
    "kind" "ProviderOpKind" NOT NULL,
    "idempotencyKey" TEXT NOT NULL,
    "amount" BIGINT NOT NULL,
    "currency" CHAR(3) NOT NULL,
    "countryCode" CHAR(2) NOT NULL,
    "status" "ProviderOpStatus" NOT NULL DEFAULT 'PENDING',
    "failureReason" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ProviderOperation_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Payout" (
    "id" TEXT NOT NULL,
    "allocationId" TEXT NOT NULL,
    "beneficiaryOrderId" TEXT NOT NULL,
    "fundingOrderId" TEXT NOT NULL,
    "amount" BIGINT NOT NULL,
    "currency" CHAR(3) NOT NULL,
    "countryCode" CHAR(2) NOT NULL,
    "providerId" TEXT NOT NULL,
    "providerRef" TEXT NOT NULL,
    "attempts" INTEGER NOT NULL DEFAULT 0,
    "status" "PayoutStatus" NOT NULL DEFAULT 'PENDING',

    CONSTRAINT "Payout_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "WebhookEvent" (
    "providerId" TEXT NOT NULL,
    "eventId" TEXT NOT NULL,
    "receivedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "payloadSha" TEXT NOT NULL,

    CONSTRAINT "WebhookEvent_pkey" PRIMARY KEY ("providerId","eventId")
);

-- CreateTable
CREATE TABLE "LedgerEntry" (
    "id" BIGSERIAL NOT NULL,
    "idempotencyKey" TEXT NOT NULL,
    "reference" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "reversesId" BIGINT,
    "simulated" BOOLEAN NOT NULL DEFAULT true,
    "at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "LedgerEntry_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "LedgerPosting" (
    "id" BIGSERIAL NOT NULL,
    "entryId" BIGINT NOT NULL,
    "accountType" "AccountType" NOT NULL,
    "currency" CHAR(3) NOT NULL,
    "scope" TEXT NOT NULL,
    "amount" BIGINT NOT NULL,

    CONSTRAINT "LedgerPosting_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AdminUser" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "role" "AdminRole" NOT NULL,
    "mfaSecretEnc" BYTEA NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "AdminUser_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "DualApproval" (
    "id" TEXT NOT NULL,
    "subjectType" TEXT NOT NULL,
    "subjectId" TEXT NOT NULL,
    "firstBy" TEXT NOT NULL,
    "secondBy" TEXT,
    "decision" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completedAt" TIMESTAMP(3),

    CONSTRAINT "DualApproval_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AuditLog" (
    "id" BIGSERIAL NOT NULL,
    "actor" TEXT NOT NULL,
    "action" TEXT NOT NULL,
    "target" TEXT NOT NULL,
    "ip" TEXT,
    "at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "details" JSONB,

    CONSTRAINT "AuditLog_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "User_phoneE164_key" ON "User"("phoneE164");

-- CreateIndex
CREATE UNIQUE INDEX "Session_tokenHash_key" ON "Session"("tokenHash");

-- CreateIndex
CREATE INDEX "Session_userId_idx" ON "Session"("userId");

-- CreateIndex
CREATE INDEX "KycCheck_userId_idx" ON "KycCheck"("userId");

-- CreateIndex
CREATE INDEX "Beneficiary_ownerId_idx" ON "Beneficiary"("ownerId");

-- CreateIndex
CREATE INDEX "FxRate_base_quote_asOf_idx" ON "FxRate"("base", "quote", "asOf");

-- CreateIndex
CREATE INDEX "TransferOrder_state_fromCountry_toCountry_createdAt_idx" ON "TransferOrder"("state", "fromCountry", "toCountry", "createdAt");

-- CreateIndex
CREATE UNIQUE INDEX "TransferOrder_userId_idempotencyKey_key" ON "TransferOrder"("userId", "idempotencyKey");

-- CreateIndex
CREATE INDEX "StateChange_orderId_idx" ON "StateChange"("orderId");

-- CreateIndex
CREATE UNIQUE INDEX "ProviderOperation_providerId_providerRef_key" ON "ProviderOperation"("providerId", "providerRef");

-- CreateIndex
CREATE UNIQUE INDEX "ProviderOperation_providerId_kind_idempotencyKey_key" ON "ProviderOperation"("providerId", "kind", "idempotencyKey");

-- CreateIndex
CREATE UNIQUE INDEX "LedgerEntry_idempotencyKey_key" ON "LedgerEntry"("idempotencyKey");

-- CreateIndex
CREATE UNIQUE INDEX "LedgerEntry_reversesId_key" ON "LedgerEntry"("reversesId");

-- CreateIndex
CREATE INDEX "LedgerEntry_reference_idx" ON "LedgerEntry"("reference");

-- CreateIndex
CREATE INDEX "LedgerPosting_accountType_currency_scope_idx" ON "LedgerPosting"("accountType", "currency", "scope");

-- CreateIndex
CREATE UNIQUE INDEX "AdminUser_email_key" ON "AdminUser"("email");

-- CreateIndex
CREATE INDEX "DualApproval_subjectType_subjectId_idx" ON "DualApproval"("subjectType", "subjectId");

-- CreateIndex
CREATE INDEX "AuditLog_target_idx" ON "AuditLog"("target");

-- AddForeignKey
ALTER TABLE "Session" ADD CONSTRAINT "Session_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "KycCheck" ADD CONSTRAINT "KycCheck_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Beneficiary" ADD CONSTRAINT "Beneficiary_ownerId_fkey" FOREIGN KEY ("ownerId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Quote" ADD CONSTRAINT "Quote_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TransferOrder" ADD CONSTRAINT "TransferOrder_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TransferOrder" ADD CONSTRAINT "TransferOrder_quoteId_fkey" FOREIGN KEY ("quoteId") REFERENCES "Quote"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TransferOrder" ADD CONSTRAINT "TransferOrder_beneficiaryId_fkey" FOREIGN KEY ("beneficiaryId") REFERENCES "Beneficiary"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "StateChange" ADD CONSTRAINT "StateChange_orderId_fkey" FOREIGN KEY ("orderId") REFERENCES "TransferOrder"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Allocation" ADD CONSTRAINT "Allocation_runId_fkey" FOREIGN KEY ("runId") REFERENCES "MatchRun"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Allocation" ADD CONSTRAINT "Allocation_takerOrderId_fkey" FOREIGN KEY ("takerOrderId") REFERENCES "TransferOrder"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Allocation" ADD CONSTRAINT "Allocation_makerOrderId_fkey" FOREIGN KEY ("makerOrderId") REFERENCES "TransferOrder"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Payout" ADD CONSTRAINT "Payout_allocationId_fkey" FOREIGN KEY ("allocationId") REFERENCES "Allocation"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "LedgerEntry" ADD CONSTRAINT "LedgerEntry_reversesId_fkey" FOREIGN KEY ("reversesId") REFERENCES "LedgerEntry"("id") ON DELETE RESTRICT ON UPDATE RESTRICT;

-- AddForeignKey
ALTER TABLE "LedgerPosting" ADD CONSTRAINT "LedgerPosting_entryId_fkey" FOREIGN KEY ("entryId") REFERENCES "LedgerEntry"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

