"""Type géométrie portable : PostGIS ``geometry(Geometry, 4326)`` ou WKB hexadécimal sous SQLite.

Le WKB est exact (pas d'arrondi, contrairement au WKT par défaut) : une géométrie relue est
identique bit à bit, condition de la reproductibilité des analyses.
"""

import shapely
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from sqlalchemy.types import Text, TypeDecorator


class GeomType(TypeDecorator):
    impl = Text
    cache_ok = True

    def __init__(self, geometry_type: str = "GEOMETRY", srid: int = 4326):
        super().__init__()
        self.geometry_type = geometry_type
        self.srid = srid
        # Attributs lus par les hooks DDL de GeoAlchemy2 : index GiST créés par la migration.
        self.spatial_index = False
        self.dimension = 2
        self.use_typmod = None

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(
                Geometry(self.geometry_type, srid=self.srid, spatial_index=False)
            )
        return dialect.type_descriptor(Text())

    def bind_expression(self, bindvalue):
        return bindvalue

    def column_expression(self, colexpr):
        # Sans cela, GeoAlchemy2 enveloppe la colonne dans ST_AsEWKB() avec son propre type et
        # renvoie un WKBElement en contournant process_result_value. PostGIS renvoie par défaut
        # l'EWKB hexadécimal, exact, décodé ci-dessous.
        return colexpr

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            # EWKB hexadécimal : PostGIS le convertit implicitement en geometry, sans perte.
            return shapely.to_wkb(shapely.set_srid(value, self.srid), hex=True, include_srid=True)
        return shapely.to_wkb(value, hex=True)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, WKBElement):
            return to_shape(value)
        if isinstance(value, (bytes, memoryview)):
            return shapely.from_wkb(bytes(value))
        return shapely.from_wkb(value)  # hex
