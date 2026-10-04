-- =============================================================================
-- Boujieka — Schéma de référence (PostgreSQL + PostGIS)
-- Modèle à six objets : unité territoriale, objet spatial, acteur, droit,
-- assertion, mesure. Voir docs/03-modele-de-donnees.md.
--
-- Hors périmètre de ce schéma : les microdonnées du recensement (ménages,
-- personnes), qui vivent dans une enclave statistique séparée. L'atlas ne
-- reçoit que des agrégats (table mesure).
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- gen_random_uuid()

CREATE SCHEMA IF NOT EXISTS atlas;
SET search_path = atlas, public;

-- -----------------------------------------------------------------------------
-- Types énumérés
-- -----------------------------------------------------------------------------

-- Classes de sensibilité (docs/05)
CREATE TYPE sensibilite AS ENUM ('S0_PUBLIC', 'S1_RESTREINT', 'S2_CONFIDENTIEL', 'S3_PROTEGE_CULTUREL');

-- Cycle de vie d'une assertion (docs/03 §3.3)
CREATE TYPE statut_assertion AS ENUM (
  'DETECTE',   -- télédétection (N1)
  'DECLARE',   -- chef, commune, citoyen (N0)
  'IMPORTE',   -- base sectorielle importée, non encore validée
  'OBSERVE',   -- vérification terrain (N2)
  'VALIDE',    -- autorité compétente (N3)
  'CONTESTE',
  'REJETE',
  'OBSOLETE'
);

CREATE TYPE niveau_collecte AS ENUM ('N0_DECLARATION', 'N1_TELEDETECTION', 'N2_TERRAIN', 'N3_ADMINISTRATIF');

CREATE TYPE type_unite AS ENUM (
  'PAYS', 'REGION', 'DEPARTEMENT', 'ARRONDISSEMENT', 'COMMUNE',
  'VILLAGE', 'QUARTIER',
  'TERRITOIRE_TRADITIONNEL',  -- déclaratif, jamais une limite officielle
  'MAILLE_STATISTIQUE',
  'ZONE_DENOMBREMENT'
);

CREATE TYPE type_acteur AS ENUM (
  'ADMINISTRATION', 'COLLECTIVITE', 'ENTREPRISE', 'ASSOCIATION',
  'COMMUNAUTE', 'CHEFFERIE', 'PERSONNE_PHYSIQUE'  -- PERSONNE_PHYSIQUE : S1 minimum
);

-- -----------------------------------------------------------------------------
-- Sources : d'où vient une information
-- -----------------------------------------------------------------------------
CREATE TABLE source (
  source_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  code           text UNIQUE NOT NULL,          -- ex. 'IMAGERIE_2025_LOT3', 'CARTE_SCOLAIRE_2026'
  libelle        text NOT NULL,
  niveau         niveau_collecte NOT NULL,
  producteur     text,                          -- institution ou outil
  licence        text,                          -- ex. 'ODbL', 'CC-BY-4.0', 'convention <réf>'
  date_reference date,                          -- date d'acquisition / de situation
  description    text
);

-- -----------------------------------------------------------------------------
-- 1. Unité territoriale (référentiel versionné)
-- -----------------------------------------------------------------------------
CREATE TABLE unite_territoriale (
  unite_id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  type            type_unite NOT NULL,
  code_officiel   text,                         -- code administratif officiel si existant
  nom             text NOT NULL,
  parent_id       uuid REFERENCES unite_territoriale(unite_id),
  geom            geometry(MultiPolygon, 4326),
  version_referentiel text NOT NULL,            -- ex. '2026.1'
  valide_depuis   date NOT NULL,
  valide_jusqua   date,                         -- NULL = en vigueur
  officiel        boolean NOT NULL DEFAULT true,  -- false pour territoires traditionnels déclarés
  source_id       uuid REFERENCES source(source_id),
  CHECK (type <> 'TERRITOIRE_TRADITIONNEL' OR officiel = false)
);
CREATE INDEX ON unite_territoriale USING gist (geom);
CREATE INDEX ON unite_territoriale (parent_id);

-- -----------------------------------------------------------------------------
-- Nomenclature (types d'objets, d'usages, de droits) — alimentée par nomenclatures/*.yaml
-- -----------------------------------------------------------------------------
CREATE TABLE nomenclature (
  code        text PRIMARY KEY,                 -- ex. 'ASSET.EDU.PRIMAIRE'
  domaine     text NOT NULL,                    -- 'OBJET', 'USAGE_SOL', 'REGIME', 'DROIT', 'MESURE'
  libelle_fr  text NOT NULL,
  libelle_en  text,
  parent_code text REFERENCES nomenclature(code),
  sensibilite_defaut sensibilite NOT NULL DEFAULT 'S0_PUBLIC'
);

-- -----------------------------------------------------------------------------
-- 2. Objet spatial : tout ce qui existe et se localise
-- -----------------------------------------------------------------------------
CREATE TABLE objet_spatial (
  objet_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  type_code     text NOT NULL REFERENCES nomenclature(code),
  nom           text,
  geom          geometry(Geometry, 4326) NOT NULL,  -- point, ligne ou polygone
  precision_m   numeric,                            -- précision de localisation connue
  sensibilite   sensibilite NOT NULL DEFAULT 'S0_PUBLIC',
  cree_le       timestamptz NOT NULL DEFAULT now()
  -- Les attributs descriptifs (nom alternatif, état, usage…) sont des assertions.
);
CREATE INDEX ON objet_spatial USING gist (geom);
CREATE INDEX ON objet_spatial (type_code);

-- Identifiants officiels sectoriels (code école, n° titre foncier, n° permis…)
CREATE TABLE identifiant_externe (
  objet_id   uuid NOT NULL REFERENCES objet_spatial(objet_id),
  systeme    text NOT NULL,                     -- ex. 'CARTE_SCOLAIRE', 'CADASTRE_MINIER'
  valeur     text NOT NULL,
  source_id  uuid REFERENCES source(source_id),
  PRIMARY KEY (systeme, valeur, objet_id)
);

-- -----------------------------------------------------------------------------
-- 3. Acteur
-- -----------------------------------------------------------------------------
CREATE TABLE acteur (
  acteur_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  type          type_acteur NOT NULL,
  nom           text NOT NULL,
  identifiant_officiel text,                    -- n° registre, acte de reconnaissance…
  unite_id      uuid REFERENCES unite_territoriale(unite_id),
  sensibilite   sensibilite NOT NULL DEFAULT 'S0_PUBLIC',
  CHECK (type <> 'PERSONNE_PHYSIQUE' OR sensibilite <> 'S0_PUBLIC')
);

-- -----------------------------------------------------------------------------
-- 4. Droit / relation (inspiré de ISO 19152 LADM : droits, restrictions, responsabilités)
-- -----------------------------------------------------------------------------
CREATE TABLE droit (
  droit_id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  type_code       text NOT NULL REFERENCES nomenclature(code),  -- ex. 'DROIT.TITRE_FONCIER', 'DROIT.CONCESSION_FORESTIERE'
  objet_id        uuid NOT NULL REFERENCES objet_spatial(objet_id),
  acteur_id       uuid NOT NULL REFERENCES acteur(acteur_id),
  reference_acte  text,                         -- n° de titre, décret, arrêté, permis
  autorite        text,                         -- autorité compétente émettrice
  part            numeric CHECK (part IS NULL OR (part > 0 AND part <= 1)),  -- indivision
  valide_depuis   date,
  valide_jusqua   date,
  sensibilite     sensibilite NOT NULL DEFAULT 'S1_RESTREINT'
  -- Le statut (DECLARE / VALIDE / CONTESTE) est porté par l'assertion associée.
);
CREATE INDEX ON droit (objet_id);
CREATE INDEX ON droit (acteur_id);

-- -----------------------------------------------------------------------------
-- 5. Assertion : qui affirme quoi, quand, comment, avec quel statut
-- -----------------------------------------------------------------------------
CREATE TABLE assertion (
  assertion_id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  -- cible : exactement une des trois
  objet_id        uuid REFERENCES objet_spatial(objet_id),
  droit_id        uuid REFERENCES droit(droit_id),
  acteur_id       uuid REFERENCES acteur(acteur_id),
  attribut        text NOT NULL,                -- ex. 'existence', 'usage', 'etat', 'nom', 'droit'
  valeur          jsonb NOT NULL,
  statut          statut_assertion NOT NULL,
  source_id       uuid NOT NULL REFERENCES source(source_id),
  auteur          text,                         -- compte agent / institution (pseudonymisé si besoin)
  preuve_uri      text,                         -- photo, acte scanné, image
  -- bitemporalité
  valide_depuis   date,                         -- vrai sur le terrain depuis
  valide_jusqua   date,
  enregistre_le   timestamptz NOT NULL DEFAULT now(),
  remplace_id     uuid REFERENCES assertion(assertion_id),
  sensibilite     sensibilite NOT NULL DEFAULT 'S0_PUBLIC',
  CHECK (num_nonnulls(objet_id, droit_id, acteur_id) = 1)
);
CREATE INDEX ON assertion (objet_id, attribut);
CREATE INDEX ON assertion (droit_id);
CREATE INDEX ON assertion (statut);

-- Un droit ne peut être VALIDE que via une source administrative (N3)
CREATE FUNCTION controle_validation_droit() RETURNS trigger AS $$
BEGIN
  IF NEW.droit_id IS NOT NULL AND NEW.statut = 'VALIDE' THEN
    IF (SELECT niveau FROM source WHERE source_id = NEW.source_id) <> 'N3_ADMINISTRATIF' THEN
      RAISE EXCEPTION 'Un droit ne peut être validé que par une source administrative (N3)';
    END IF;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_controle_validation_droit
  BEFORE INSERT OR UPDATE ON assertion
  FOR EACH ROW EXECUTE FUNCTION controle_validation_droit();

-- -----------------------------------------------------------------------------
-- 6. Mesure : valeurs quantitatives datées (capacité, effectifs, population agrégée…)
-- -----------------------------------------------------------------------------
CREATE TABLE mesure (
  mesure_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  objet_id      uuid REFERENCES objet_spatial(objet_id),
  unite_id      uuid REFERENCES unite_territoriale(unite_id),
  indicateur    text NOT NULL REFERENCES nomenclature(code),  -- ex. 'MESURE.POP_TOTALE'
  valeur        numeric NOT NULL,
  borne_basse   numeric,                        -- intervalle d'incertitude (estimations)
  borne_haute   numeric,
  est_estimation boolean NOT NULL DEFAULT false,
  date_reference date NOT NULL,
  source_id     uuid NOT NULL REFERENCES source(source_id),
  sensibilite   sensibilite NOT NULL DEFAULT 'S0_PUBLIC',
  CHECK (num_nonnulls(objet_id, unite_id) = 1),
  CHECK (borne_basse IS NULL OR borne_haute IS NULL OR borne_basse <= borne_haute)
);
CREATE INDEX ON mesure (unite_id, indicateur, date_reference);

-- -----------------------------------------------------------------------------
-- Normes officielles pour le calcul des déficits (docs/06 §3)
-- -----------------------------------------------------------------------------
CREATE TABLE norme (
  norme_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  code          text NOT NULL,                  -- ex. 'EDU.ELEVES_PAR_SALLE'
  valeur        numeric NOT NULL,
  unite         text NOT NULL,
  officielle    boolean NOT NULL,               -- false = référence internationale étiquetée
  texte_source  text NOT NULL,                  -- référence du texte ou du document
  autorite      text NOT NULL,
  valide_depuis date NOT NULL,
  valide_jusqua date
);

-- -----------------------------------------------------------------------------
-- Anomalies issues du rapprochement (file de vérification)
-- -----------------------------------------------------------------------------
CREATE TABLE anomalie (
  anomalie_id   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  unite_id      uuid REFERENCES unite_territoriale(unite_id),
  objet_id      uuid REFERENCES objet_spatial(objet_id),
  type          text NOT NULL,                  -- 'ECART_SOURCES', 'SANS_TITRE', 'DOUBLON', ...
  description   text NOT NULL,
  niveau_requis niveau_collecte NOT NULL,       -- N2 ou N3
  statut        text NOT NULL DEFAULT 'OUVERTE' CHECK (statut IN ('OUVERTE', 'AFFECTEE', 'RESOLUE', 'CLASSEE')),
  cree_le       timestamptz NOT NULL DEFAULT now()
);

-- -----------------------------------------------------------------------------
-- Vue : valeur courante par objet et attribut (meilleur statut, puis plus récente)
-- -----------------------------------------------------------------------------
CREATE VIEW assertion_courante AS
SELECT DISTINCT ON (objet_id, attribut) *
FROM assertion
WHERE objet_id IS NOT NULL
  AND statut NOT IN ('REJETE', 'OBSOLETE')
  AND (valide_jusqua IS NULL OR valide_jusqua >= current_date)
ORDER BY objet_id, attribut,
  CASE statut
    WHEN 'VALIDE'   THEN 1
    WHEN 'OBSERVE'  THEN 2
    WHEN 'IMPORTE'  THEN 3
    WHEN 'DETECTE'  THEN 4
    WHEN 'DECLARE'  THEN 5
    WHEN 'CONTESTE' THEN 6
  END,
  enregistre_le DESC;

-- -----------------------------------------------------------------------------
-- Contrôle d'accès par ligne (exemple sur objet_spatial)
-- Le rôle applicatif positionne : SET app.niveau_acces = 'S1_RESTREINT';
-- -----------------------------------------------------------------------------
ALTER TABLE objet_spatial ENABLE ROW LEVEL SECURITY;
CREATE POLICY lecture_par_sensibilite ON objet_spatial FOR SELECT
  USING (
    sensibilite = 'S0_PUBLIC'
    OR (sensibilite = 'S1_RESTREINT'
        AND current_setting('app.niveau_acces', true) IN ('S1_RESTREINT', 'S2_CONFIDENTIEL'))
    OR (sensibilite = 'S3_PROTEGE_CULTUREL'
        AND current_setting('app.acces_patrimoine_protege', true) = 'oui')
  );
-- À étendre aux tables assertion, droit, acteur, mesure.
