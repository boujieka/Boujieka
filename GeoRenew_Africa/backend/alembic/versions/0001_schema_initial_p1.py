"""schema initial P1

Revision ID: 0001
Revises: 
Create Date: 2026-11-18

Crée l'extension PostGIS (PostgreSQL uniquement), les tables P1 et les index spatiaux GiST.
Sous SQLite (option locale), les géométries sont stockées en WKB hexadécimal.
"""
from alembic import op
import sqlalchemy as sa

from app.geomtype import GeomType


revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


GEOM_COLUMNS = (("features", "geom"), ("sites", "boundary"), ("layers", "geom"))


def _is_pg() -> bool:
    return op.get_bind().dialect.name == "postgresql"


def upgrade() -> None:
    if _is_pg():
        op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table('audit_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column('actor', sa.String(length=200), nullable=False),
    sa.Column('action', sa.String(length=60), nullable=False),
    sa.Column('entity_type', sa.String(length=60), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('details', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_log_project_id'), 'audit_log', ['project_id'], unique=False)
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('country_iso3', sa.String(length=3), nullable=False),
    sa.Column('technology', sa.Enum('pv', 'eolien', 'bess', 'hybride', name='technology', native_enum=False, create_constraint=True, length=40), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('is_fictional', sa.Boolean(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('display_name', sa.String(length=200), nullable=False),
    sa.Column('role', sa.Enum('lecteur', 'analyste', 'administrateur', name='user_role', native_enum=False, create_constraint=True, length=40), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('datasets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('category', sa.Enum('limite_site', 'exclusion', 'contrainte', 'cadastre_officiel', 'releve_qualifie', 'reseau_electrique', 'etude_reseau', 'accord_gestionnaire', 'autre', name='dataset_category', native_enum=False, create_constraint=True, length=40), nullable=False),
    sa.Column('nature', sa.Enum('observee', 'modelisee', 'hypothese', 'inconnue', name='data_nature', native_enum=False, create_constraint=True, length=40), nullable=False),
    sa.Column('source_name', sa.String(length=300), nullable=False),
    sa.Column('source_url', sa.String(length=1000), nullable=False),
    sa.Column('licence', sa.String(length=300), nullable=False),
    sa.Column('producer', sa.String(length=300), nullable=False),
    sa.Column('reference_date', sa.Date(), nullable=True),
    sa.Column('horizontal_accuracy_m', sa.Float(), nullable=True),
    sa.Column('is_synthetic', sa.Boolean(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.CheckConstraint('horizontal_accuracy_m IS NULL OR horizontal_accuracy_m >= 0', name='ck_dataset_accuracy'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_datasets_project_id'), 'datasets', ['project_id'], unique=False)
    op.create_table('constraint_rules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('dataset_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('kind', sa.Enum('exclusion_stricte', 'contrainte_indicative', name='rule_kind', native_enum=False, create_constraint=True, length=40), nullable=False),
    sa.Column('buffer_m', sa.Float(), nullable=False),
    sa.Column('justification_type', sa.Enum('aucun_buffer', 'hypothese_utilisateur', 'texte_reglementaire_cite', 'norme_technique_citee', 'etude_terrain', name='justification_type', native_enum=False, create_constraint=True, length=40), nullable=False),
    sa.Column('justification', sa.Text(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.CheckConstraint('buffer_m >= 0', name='ck_rule_buffer'),
    sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_constraint_rules_project_id'), 'constraint_rules', ['project_id'], unique=False)
    op.create_table('dataset_versions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dataset_id', sa.Integer(), nullable=False),
    sa.Column('version_no', sa.Integer(), nullable=False),
    sa.Column('sha256', sa.String(length=64), nullable=False),
    sa.Column('original_filename', sa.String(length=300), nullable=False),
    sa.Column('file_format', sa.String(length=30), nullable=False),
    sa.Column('source_crs', sa.String(length=300), nullable=False),
    sa.Column('crs_origin', sa.String(length=40), nullable=False),
    sa.Column('feature_count', sa.Integer(), nullable=False),
    sa.Column('geometry_types', sa.JSON(), nullable=False),
    sa.Column('bbox', sa.JSON(), nullable=True),
    sa.Column('warnings', sa.JSON(), nullable=False),
    sa.Column('imported_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dataset_id', 'version_no', name='uq_dataset_version')
    )
    op.create_index(op.f('ix_dataset_versions_dataset_id'), 'dataset_versions', ['dataset_id'], unique=False)
    op.create_table('features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dataset_version_id', sa.Integer(), nullable=False),
    sa.Column('feature_index', sa.Integer(), nullable=False),
    sa.Column('geom', GeomType(), nullable=False),
    sa.Column('properties', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['dataset_version_id'], ['dataset_versions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_features_dataset_version_id'), 'features', ['dataset_version_id'], unique=False)
    op.create_table('sites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('boundary', GeomType(), nullable=False),
    sa.Column('boundary_dataset_version_id', sa.Integer(), nullable=True),
    sa.Column('boundary_source', sa.String(length=300), nullable=False),
    sa.Column('boundary_accuracy_m', sa.Float(), nullable=True),
    sa.Column('land_status', sa.Enum('inconnu', 'declare_non_verifie', 'verifie_sur_piece', name='land_status', native_enum=False, create_constraint=True, length=40), nullable=False),
    sa.Column('land_evidence_dataset_id', sa.Integer(), nullable=True),
    sa.Column('grid_status', sa.Enum('inconnu', 'etude_en_cours', 'raccordement_confirme', name='grid_status', native_enum=False, create_constraint=True, length=40), nullable=False),
    sa.Column('grid_evidence_dataset_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.ForeignKeyConstraint(['boundary_dataset_version_id'], ['dataset_versions.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['grid_evidence_dataset_id'], ['datasets.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['land_evidence_dataset_id'], ['datasets.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sites_project_id'), 'sites', ['project_id'], unique=False)
    op.create_table('analysis_runs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('input_hash', sa.String(length=64), nullable=False),
    sa.Column('inputs', sa.JSON(), nullable=False),
    sa.Column('results', sa.JSON(), nullable=False),
    sa.Column('software_version', sa.String(length=40), nullable=False),
    sa.Column('engine_version', sa.String(length=40), nullable=False),
    sa.Column('duration_ms', sa.Integer(), nullable=False),
    sa.Column('actor', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_runs_input_hash'), 'analysis_runs', ['input_hash'], unique=False)
    op.create_index(op.f('ix_analysis_runs_site_id'), 'analysis_runs', ['site_id'], unique=False)
    op.create_table('layers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=False),
    sa.Column('kind', sa.String(length=40), nullable=False),
    sa.Column('rule_id', sa.Integer(), nullable=True),
    sa.Column('area_m2', sa.Float(), nullable=False),
    sa.Column('geom', GeomType(), nullable=False),
    sa.ForeignKeyConstraint(['run_id'], ['analysis_runs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_layers_run_id'), 'layers', ['run_id'], unique=False)
    if _is_pg():
        for table, col in GEOM_COLUMNS:
            op.execute(f"CREATE INDEX ix_{table}_{col}_gist ON {table} USING GIST ({col})")


def downgrade() -> None:
    if _is_pg():
        for table, col in GEOM_COLUMNS:
            op.execute(f"DROP INDEX IF EXISTS ix_{table}_{col}_gist")
    op.drop_index(op.f('ix_layers_run_id'), table_name='layers')
    op.drop_table('layers')
    op.drop_index(op.f('ix_analysis_runs_site_id'), table_name='analysis_runs')
    op.drop_index(op.f('ix_analysis_runs_input_hash'), table_name='analysis_runs')
    op.drop_table('analysis_runs')
    op.drop_index(op.f('ix_sites_project_id'), table_name='sites')
    op.drop_table('sites')
    op.drop_index(op.f('ix_features_dataset_version_id'), table_name='features')
    op.drop_table('features')
    op.drop_index(op.f('ix_dataset_versions_dataset_id'), table_name='dataset_versions')
    op.drop_table('dataset_versions')
    op.drop_index(op.f('ix_constraint_rules_project_id'), table_name='constraint_rules')
    op.drop_table('constraint_rules')
    op.drop_index(op.f('ix_datasets_project_id'), table_name='datasets')
    op.drop_table('datasets')
    op.drop_table('users')
    op.drop_table('projects')
    op.drop_table('organizations')
    op.drop_index(op.f('ix_audit_log_project_id'), table_name='audit_log')
    op.drop_table('audit_log')
