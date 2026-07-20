-- CreateEnum
CREATE TYPE "OrganizationType" AS ENUM ('offtaker', 'developer');

-- CreateEnum
CREATE TYPE "UserRole" AS ENUM ('offtaker', 'developer', 'admin');

-- CreateEnum
CREATE TYPE "LoadCriticality" AS ENUM ('faible', 'moyenne', 'elevee', 'critique');

-- CreateEnum
CREATE TYPE "FinancingCapacity" AS ENUM ('equity', 'dette', 'mixte', 'aucune');

-- CreateEnum
CREATE TYPE "Technology" AS ENUM ('solaire', 'stockage', 'hybride', 'groupe_backup');

-- CreateEnum
CREATE TYPE "OpportunityStage" AS ENUM ('identifiee', 'qualifiee', 'term_sheet', 'mandat', 'bouclage_financier', 'realisee', 'abandonnee');

-- CreateEnum
CREATE TYPE "QualificationStatus" AS ENUM ('non_qualifiee', 'qualifiee', 'rejetee');

-- CreateEnum
CREATE TYPE "SimulationMethod" AS ENUM ('cible_fixee', 'optimisation_economique');

-- CreateEnum
CREATE TYPE "Rating" AS ENUM ('A', 'B', 'C', 'D');

-- CreateEnum
CREATE TYPE "MatchStatus" AS ENUM ('propose', 'valide_admin', 'ecarte');

-- CreateEnum
CREATE TYPE "EoiStatus" AS ENUM ('soumise', 'acceptee', 'refusee');

-- CreateEnum
CREATE TYPE "GeneratedBy" AS ENUM ('ia', 'humain');

-- CreateEnum
CREATE TYPE "AiTaskType" AS ENUM ('qualification', 'extraction_facture', 'note_concept', 'explication_matching');

-- CreateTable
CREATE TABLE "organizations" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "type" "OrganizationType" NOT NULL,
    "country" TEXT NOT NULL,
    "sector" TEXT,
    "description" TEXT,
    "website" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "deleted_at" TIMESTAMP(3),

    CONSTRAINT "organizations_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "users" (
    "id" TEXT NOT NULL,
    "organization_id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password_hash" TEXT NOT NULL,
    "full_name" TEXT NOT NULL,
    "role" "UserRole" NOT NULL,
    "is_active" BOOLEAN NOT NULL DEFAULT true,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "sites" (
    "id" TEXT NOT NULL,
    "organization_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "latitude" DOUBLE PRECISION NOT NULL,
    "longitude" DOUBLE PRECISION NOT NULL,
    "country" TEXT NOT NULL,
    "available_area_m2" DOUBLE PRECISION,
    "current_grid_tariff" DOUBLE PRECISION,
    "annual_consumption_kwh" DOUBLE PRECISION,
    "peak_demand_kw" DOUBLE PRECISION,
    "load_criticality" "LoadCriticality" NOT NULL DEFAULT 'moyenne',
    "outage_cost_per_hour" DOUBLE PRECISION,
    "grid_outage_hours_year" DOUBLE PRECISION,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "deleted_at" TIMESTAMP(3),

    CONSTRAINT "sites_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "load_profiles" (
    "id" TEXT NOT NULL,
    "site_id" TEXT NOT NULL,
    "hourly_kw" JSONB NOT NULL,
    "source" TEXT NOT NULL DEFAULT 'profil_type',
    "sector_template" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "load_profiles_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "developer_profiles" (
    "id" TEXT NOT NULL,
    "organization_id" TEXT NOT NULL,
    "min_project_size_kw" DOUBLE PRECISION NOT NULL,
    "max_project_size_kw" DOUBLE PRECISION NOT NULL,
    "financing_capacity" "FinancingCapacity" NOT NULL,
    "track_record_mw" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "projects_completed" INTEGER NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "developer_profiles_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "developer_zones" (
    "id" TEXT NOT NULL,
    "developer_profile_id" TEXT NOT NULL,
    "country" TEXT NOT NULL,
    "region" TEXT,

    CONSTRAINT "developer_zones_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "developer_technologies" (
    "id" TEXT NOT NULL,
    "developer_profile_id" TEXT NOT NULL,
    "technology" "Technology" NOT NULL,

    CONSTRAINT "developer_technologies_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "opportunities" (
    "id" TEXT NOT NULL,
    "site_id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "stage" "OpportunityStage" NOT NULL DEFAULT 'identifiee',
    "qualification_status" "QualificationStatus" NOT NULL DEFAULT 'non_qualifiee',
    "qualification_summary" TEXT,
    "target_reliability_rate" DOUBLE PRECISION NOT NULL DEFAULT 0.95,
    "owner_user_id" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "deleted_at" TIMESTAMP(3),

    CONSTRAINT "opportunities_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "prefeasibility_studies" (
    "id" TEXT NOT NULL,
    "opportunity_id" TEXT NOT NULL,
    "pv_size_kwp" DOUBLE PRECISION NOT NULL,
    "battery_size_kwh" DOUBLE PRECISION NOT NULL,
    "backup_size_kw" DOUBLE PRECISION NOT NULL,
    "annual_yield_kwh" DOUBLE PRECISION NOT NULL,
    "coverage_rate" DOUBLE PRECISION NOT NULL,
    "residual_deficit_kwh" DOUBLE PRECISION NOT NULL,
    "reliability_cost" DOUBLE PRECISION NOT NULL,
    "simulation_method" "SimulationMethod" NOT NULL DEFAULT 'cible_fixee',
    "assumptions" JSONB,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "prefeasibility_studies_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "techno_economic_models" (
    "id" TEXT NOT NULL,
    "prefeasibility_study_id" TEXT NOT NULL,
    "capex" DOUBLE PRECISION NOT NULL,
    "opex_annual" DOUBLE PRECISION NOT NULL,
    "ppa_tariff" DOUBLE PRECISION NOT NULL,
    "irr" DOUBLE PRECISION,
    "payback_years" DOUBLE PRECISION,
    "annual_savings" DOUBLE PRECISION NOT NULL,
    "currency" TEXT NOT NULL DEFAULT 'USD',
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "techno_economic_models_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "grid_emission_factors" (
    "id" TEXT NOT NULL,
    "country" TEXT NOT NULL,
    "emission_factor_tco2_per_mwh" DOUBLE PRECISION NOT NULL,
    "source" TEXT,
    "year" INTEGER,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "grid_emission_factors_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "decarbonization_metrics" (
    "id" TEXT NOT NULL,
    "opportunity_id" TEXT NOT NULL,
    "grid_emission_factor_id" TEXT,
    "annual_co2_avoided_tonnes" DOUBLE PRECISION NOT NULL,
    "lifetime_co2_avoided_tonnes" DOUBLE PRECISION NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "decarbonization_metrics_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "bankability_scores" (
    "id" TEXT NOT NULL,
    "opportunity_id" TEXT NOT NULL,
    "financial_score" DOUBLE PRECISION NOT NULL,
    "technical_score" DOUBLE PRECISION NOT NULL,
    "resilience_score" DOUBLE PRECISION NOT NULL,
    "decarbonization_score" DOUBLE PRECISION NOT NULL,
    "total_score" DOUBLE PRECISION NOT NULL,
    "rating" "Rating" NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "bankability_scores_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "matches" (
    "id" TEXT NOT NULL,
    "opportunity_id" TEXT NOT NULL,
    "developer_profile_id" TEXT NOT NULL,
    "geography_score" DOUBLE PRECISION NOT NULL,
    "size_score" DOUBLE PRECISION NOT NULL,
    "technology_score" DOUBLE PRECISION NOT NULL,
    "bankability_alignment" DOUBLE PRECISION NOT NULL,
    "compatibility_score" DOUBLE PRECISION NOT NULL,
    "explanation" TEXT,
    "status" "MatchStatus" NOT NULL DEFAULT 'propose',
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "matches_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "expressions_of_interest" (
    "id" TEXT NOT NULL,
    "opportunity_id" TEXT NOT NULL,
    "developer_profile_id" TEXT NOT NULL,
    "message" TEXT,
    "status" "EoiStatus" NOT NULL DEFAULT 'soumise',
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "expressions_of_interest_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "messages" (
    "id" TEXT NOT NULL,
    "opportunity_id" TEXT NOT NULL,
    "sender_user_id" TEXT NOT NULL,
    "recipient_user_id" TEXT NOT NULL,
    "body" TEXT NOT NULL,
    "read_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "messages_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "concept_notes" (
    "id" TEXT NOT NULL,
    "opportunity_id" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "generated_by" "GeneratedBy" NOT NULL DEFAULT 'ia',
    "version" INTEGER NOT NULL DEFAULT 1,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "concept_notes_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ai_interactions" (
    "id" TEXT NOT NULL,
    "user_id" TEXT,
    "opportunity_id" TEXT,
    "task_type" "AiTaskType" NOT NULL,
    "model" TEXT NOT NULL,
    "tokens_used" INTEGER NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "ai_interactions_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "organizations_type_idx" ON "organizations"("type");

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- CreateIndex
CREATE INDEX "users_organization_id_idx" ON "users"("organization_id");

-- CreateIndex
CREATE INDEX "sites_organization_id_idx" ON "sites"("organization_id");

-- CreateIndex
CREATE INDEX "sites_country_idx" ON "sites"("country");

-- CreateIndex
CREATE UNIQUE INDEX "load_profiles_site_id_key" ON "load_profiles"("site_id");

-- CreateIndex
CREATE UNIQUE INDEX "developer_profiles_organization_id_key" ON "developer_profiles"("organization_id");

-- CreateIndex
CREATE INDEX "developer_zones_developer_profile_id_idx" ON "developer_zones"("developer_profile_id");

-- CreateIndex
CREATE INDEX "developer_zones_country_idx" ON "developer_zones"("country");

-- CreateIndex
CREATE UNIQUE INDEX "developer_technologies_developer_profile_id_technology_key" ON "developer_technologies"("developer_profile_id", "technology");

-- CreateIndex
CREATE INDEX "opportunities_site_id_idx" ON "opportunities"("site_id");

-- CreateIndex
CREATE INDEX "opportunities_stage_idx" ON "opportunities"("stage");

-- CreateIndex
CREATE INDEX "opportunities_qualification_status_idx" ON "opportunities"("qualification_status");

-- CreateIndex
CREATE UNIQUE INDEX "prefeasibility_studies_opportunity_id_key" ON "prefeasibility_studies"("opportunity_id");

-- CreateIndex
CREATE UNIQUE INDEX "techno_economic_models_prefeasibility_study_id_key" ON "techno_economic_models"("prefeasibility_study_id");

-- CreateIndex
CREATE UNIQUE INDEX "grid_emission_factors_country_key" ON "grid_emission_factors"("country");

-- CreateIndex
CREATE UNIQUE INDEX "decarbonization_metrics_opportunity_id_key" ON "decarbonization_metrics"("opportunity_id");

-- CreateIndex
CREATE UNIQUE INDEX "bankability_scores_opportunity_id_key" ON "bankability_scores"("opportunity_id");

-- CreateIndex
CREATE INDEX "matches_opportunity_id_idx" ON "matches"("opportunity_id");

-- CreateIndex
CREATE INDEX "matches_developer_profile_id_idx" ON "matches"("developer_profile_id");

-- CreateIndex
CREATE UNIQUE INDEX "matches_opportunity_id_developer_profile_id_key" ON "matches"("opportunity_id", "developer_profile_id");

-- CreateIndex
CREATE UNIQUE INDEX "expressions_of_interest_opportunity_id_developer_profile_id_key" ON "expressions_of_interest"("opportunity_id", "developer_profile_id");

-- CreateIndex
CREATE INDEX "messages_opportunity_id_idx" ON "messages"("opportunity_id");

-- CreateIndex
CREATE INDEX "concept_notes_opportunity_id_idx" ON "concept_notes"("opportunity_id");

-- CreateIndex
CREATE INDEX "ai_interactions_opportunity_id_idx" ON "ai_interactions"("opportunity_id");

-- AddForeignKey
ALTER TABLE "users" ADD CONSTRAINT "users_organization_id_fkey" FOREIGN KEY ("organization_id") REFERENCES "organizations"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "sites" ADD CONSTRAINT "sites_organization_id_fkey" FOREIGN KEY ("organization_id") REFERENCES "organizations"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "load_profiles" ADD CONSTRAINT "load_profiles_site_id_fkey" FOREIGN KEY ("site_id") REFERENCES "sites"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "developer_profiles" ADD CONSTRAINT "developer_profiles_organization_id_fkey" FOREIGN KEY ("organization_id") REFERENCES "organizations"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "developer_zones" ADD CONSTRAINT "developer_zones_developer_profile_id_fkey" FOREIGN KEY ("developer_profile_id") REFERENCES "developer_profiles"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "developer_technologies" ADD CONSTRAINT "developer_technologies_developer_profile_id_fkey" FOREIGN KEY ("developer_profile_id") REFERENCES "developer_profiles"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "opportunities" ADD CONSTRAINT "opportunities_site_id_fkey" FOREIGN KEY ("site_id") REFERENCES "sites"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "opportunities" ADD CONSTRAINT "opportunities_owner_user_id_fkey" FOREIGN KEY ("owner_user_id") REFERENCES "users"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "prefeasibility_studies" ADD CONSTRAINT "prefeasibility_studies_opportunity_id_fkey" FOREIGN KEY ("opportunity_id") REFERENCES "opportunities"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "techno_economic_models" ADD CONSTRAINT "techno_economic_models_prefeasibility_study_id_fkey" FOREIGN KEY ("prefeasibility_study_id") REFERENCES "prefeasibility_studies"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "decarbonization_metrics" ADD CONSTRAINT "decarbonization_metrics_opportunity_id_fkey" FOREIGN KEY ("opportunity_id") REFERENCES "opportunities"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "decarbonization_metrics" ADD CONSTRAINT "decarbonization_metrics_grid_emission_factor_id_fkey" FOREIGN KEY ("grid_emission_factor_id") REFERENCES "grid_emission_factors"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "bankability_scores" ADD CONSTRAINT "bankability_scores_opportunity_id_fkey" FOREIGN KEY ("opportunity_id") REFERENCES "opportunities"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "matches" ADD CONSTRAINT "matches_opportunity_id_fkey" FOREIGN KEY ("opportunity_id") REFERENCES "opportunities"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "matches" ADD CONSTRAINT "matches_developer_profile_id_fkey" FOREIGN KEY ("developer_profile_id") REFERENCES "developer_profiles"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "expressions_of_interest" ADD CONSTRAINT "expressions_of_interest_opportunity_id_fkey" FOREIGN KEY ("opportunity_id") REFERENCES "opportunities"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "expressions_of_interest" ADD CONSTRAINT "expressions_of_interest_developer_profile_id_fkey" FOREIGN KEY ("developer_profile_id") REFERENCES "developer_profiles"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "messages" ADD CONSTRAINT "messages_opportunity_id_fkey" FOREIGN KEY ("opportunity_id") REFERENCES "opportunities"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "messages" ADD CONSTRAINT "messages_sender_user_id_fkey" FOREIGN KEY ("sender_user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "messages" ADD CONSTRAINT "messages_recipient_user_id_fkey" FOREIGN KEY ("recipient_user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "concept_notes" ADD CONSTRAINT "concept_notes_opportunity_id_fkey" FOREIGN KEY ("opportunity_id") REFERENCES "opportunities"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ai_interactions" ADD CONSTRAINT "ai_interactions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ai_interactions" ADD CONSTRAINT "ai_interactions_opportunity_id_fkey" FOREIGN KEY ("opportunity_id") REFERENCES "opportunities"("id") ON DELETE SET NULL ON UPDATE CASCADE;

