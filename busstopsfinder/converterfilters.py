from abstractfilters import AbstractConverterFilter
from shapely.geometry.collection import GeometryCollection
from shapely.geometry import shape, mapping

class Features2GeomFilter(AbstractConverterFilter):
	""" Filters geometries from FeaturesCollection and returns a GeometryCollection shape """
	def filter(self, features):
		try:
			return GeometryCollection([ shape( feature["geometry"] ) for feature in features ])
		except TypeError:
			return None

class Geom2GeoJsonFilter(AbstractConverterFilter):
	""" Filter to Converts geometries in geoJson ready format (py dict) """
	def filter(self, geometry):
		try:
			return mapping(geometry)
		except AttributeError:
			return None