"""PostGIS: project location points and an indexed feature table for every dataset.

Revision ID: 0004
Revises: 0003

Features are kept in sync with `datasets.geojson` by a trigger, so uploads and the public data ingestion need no
code change. Geometries are made valid (ST_MakeValid) and stored in EPSG:4326.
"""
from alembic import op

from app.config import get_settings

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None

CURRENT_ORG = "NULLIF(current_setting('app.current_org', true), '')::uuid"


def upgrade() -> None:
    role = get_settings().app_db_role
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("""
        ALTER TABLE projects ADD COLUMN location geometry(Point, 4326)
        GENERATED ALWAYS AS (CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL
                                  THEN ST_SetSRID(ST_MakePoint(longitude, latitude), 4326) END) STORED""")
    op.execute("CREATE INDEX ix_projects_location ON projects USING GIST (location)")
    op.execute("""
        CREATE TABLE dataset_features (
            id BIGSERIAL PRIMARY KEY,
            dataset_id UUID NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
            org_id UUID NULL,
            geom geometry(Geometry, 4326) NOT NULL,
            properties JSONB NOT NULL DEFAULT '{}'::jsonb
        )""")
    op.execute("CREATE INDEX ix_dataset_features_geom ON dataset_features USING GIST (geom)")
    op.execute("CREATE INDEX ix_dataset_features_dataset ON dataset_features (dataset_id)")
    op.execute("ALTER TABLE dataset_features ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE dataset_features FORCE ROW LEVEL SECURITY")
    op.execute(f"CREATE POLICY features_read ON dataset_features FOR SELECT USING (org_id IS NULL OR org_id = {CURRENT_ORG})")
    op.execute(f"CREATE POLICY features_insert ON dataset_features FOR INSERT WITH CHECK (org_id = {CURRENT_ORG})")
    op.execute(f"CREATE POLICY features_delete ON dataset_features FOR DELETE USING (org_id = {CURRENT_ORG})")
    op.execute(f"GRANT SELECT, INSERT, DELETE ON dataset_features TO {role}")
    op.execute(f"GRANT USAGE ON SEQUENCE dataset_features_id_seq TO {role}")
    op.execute("""
        CREATE FUNCTION sync_dataset_features() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
            DELETE FROM dataset_features WHERE dataset_id = NEW.id;
            INSERT INTO dataset_features (dataset_id, org_id, geom, properties)
            SELECT NEW.id, NEW.org_id,
                   ST_MakeValid(ST_SetSRID(ST_GeomFromGeoJSON((f -> 'geometry')::text), 4326)),
                   COALESCE(f -> 'properties', '{}'::jsonb)
            FROM jsonb_array_elements(COALESCE(NEW.geojson -> 'features', '[]'::jsonb)) AS f
            WHERE jsonb_typeof(f -> 'geometry') = 'object';
            RETURN NEW;
        END $$""")
    op.execute("""
        CREATE TRIGGER trg_sync_dataset_features AFTER INSERT OR UPDATE OF geojson ON datasets
        FOR EACH ROW EXECUTE FUNCTION sync_dataset_features()""")
    op.execute("UPDATE datasets SET geojson = geojson")  # backfill existing datasets


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_sync_dataset_features ON datasets")
    op.execute("DROP FUNCTION IF EXISTS sync_dataset_features()")
    op.execute("DROP TABLE IF EXISTS dataset_features")
    op.execute("DROP INDEX IF EXISTS ix_projects_location")
    op.execute("ALTER TABLE projects DROP COLUMN IF EXISTS location")
