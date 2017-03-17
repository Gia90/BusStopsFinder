import unittest
from tests.utilities import featuresGeomsL
from busstopsfinder.converterfilters import *
from shapely.geometry import Point
from shapely.geometry.collection import GeometryCollection

class ConverterFiltersUnitTestCase(unittest.TestCase):
	"""Unit Tests for `converterfilters.py`."""
	
	# Features2GeomFilter
	
	def test_Features2GeomFilter(self):
		"""Test Features2GeomFilter in normal case """
		
		expected = GeometryCollection( [ Point(0.0, 0.0), Point(1.0, 2.0) ] )
		testfeatures = featuresGeomsL( [{
																"type": "Point",
																"coordinates": (0.0, 0.0)
															},
															{
																"type": "Point",
																"coordinates": (1.0, 2.0)
															}])
		
		self.assertEqual( expected, Features2GeomFilter().filter( testfeatures ) )
	
	def test_Features2GeomFilter_none_features(self):
		"""Test Features2GeomFilter on None features , expected: None """
		
		expected = None
		testfeatures = None
		
		self.assertEqual( expected, Features2GeomFilter().filter( testfeatures ) )
	
	def test_Features2GeomFilter_empty_features(self):
		"""Test Features2GeomFilter on empty features , expected: GeometryCollection( [] ) """
		
		expected = GeometryCollection( [] )
		testfeatures = featuresGeomsL( [] )
		
		self.assertEqual( expected, Features2GeomFilter().filter( testfeatures ) )
	
	def test_Features2GeomFilter_not_features(self):
		"""Test Features2GeomFilter on "not features" , expected: None """
		
		expected = None
		testfeatures = "I am not features"
		
		self.assertEqual( expected, Features2GeomFilter().filter( testfeatures ) )
	
	
	# Geom2GeoJsonFilter
	
	
	def test_Geom2GeoJsonFilter(self):
		"""Test Geom2GeoJsonFilter in normal case """
		testgeom = Point(0, 0)
		expected = {
								"type": "Point",
								"coordinates": (0.0, 0.0)
							}
		self.assertEqual( expected, Geom2GeoJsonFilter().filter( testgeom ) )
	
	def test_Geom2GeoJsonFilter_none_geom(self):
		"""Test Geom2GeoJsonFilter on NOne Geom, expected: None """
		testgeom = None
		expected = None
		self.assertEqual( expected, Geom2GeoJsonFilter().filter( testgeom ) )
	
	def test_Geom2GeoJsonFilter_empty_geom(self):
		"""Test Geom2GeoJsonFilter on empty GeometryCollection, expected: geojson with type GeometryCollection and no geoms """
		testgeom = GeometryCollection()
		expected = {
							"type": "GeometryCollection",
							"geometries": []
						}
		self.assertEqual( expected, Geom2GeoJsonFilter().filter( testgeom ) )
	
	def test_Geom2GeoJsonFilter_not_geom(self):
		"""Test Geom2GeoJsonFilter on a not geometry, expected: None"""
		testgeom = "I am not a geom"
		expected = None
		self.assertEqual( expected, Geom2GeoJsonFilter().filter( testgeom ) )


if __name__ == '__main__':
    unittest.main()