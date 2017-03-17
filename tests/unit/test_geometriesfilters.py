import unittest
from busstopsfinder.geometriesfilters import *
from shapely.geometry import Point

class GeometriesFiltersUnitTestCase(unittest.TestCase):
	"""Unit Tests for `geometriesfilters.py`."""
	
	# BufferGeomFilter
	
	def test_BufferGeomFilter(self):
		"""Test BufferGeomFilter in normal conditions (core functionality correctness granted by the shapely lib) """
		testgeom = Point(0,0)
		expected = Point(0,0).buffer(1)

		self.assertEqual( expected, BufferGeomFilter(1).filter( testgeom ) )
	
	def test_BufferGeomFilter_none_geom(self):
		"""Test BufferGeomFilter with None shape, expected None """
		testgeom = None
		expected = None
		self.assertEqual( expected, BufferGeomFilter(0).filter( testgeom ) )
		
	def test_BufferGeomFilter_not_geom(self):
		"""Test BufferGeomFilter with not a geom, expected None """
		testgeom = "I am not an geom"
		expected = None
		self.assertEqual( expected, BufferGeomFilter(0).filter( testgeom ) )
	
	def test_BufferGeomFilter_none_distance(self):
		"""Test BufferGeomFilter with None distance, expected None """
		testdist = None
		expected = None
		self.assertEqual( expected, BufferGeomFilter(testdist).filter( Point(0,0) ) )
	
	def test_BufferGeomFilter_not_int_distance(self):
		"""Test BufferGeomFilter with not int distance, expected None """
		testdist = "I am not an int"
		expected = None
		self.assertEqual( expected, BufferGeomFilter(testdist).filter( Point(0,0) ) )
	
	
	# IntersectGeomFilter
	
	def test_IntersectGeomFilter(self):
		"""Test IntersectGeomFilter in normal conditions (core functionality correctness granted by the shapely lib) """
		testgeom = Point(0,0)
		expected = Point(0,0)

		self.assertEqual( expected, IntersectGeomFilter(testgeom).filter( Point(0,0) ) )
	
	
	def test_IntersectGeomFilter_none_geom1(self):
		"""Test IntersectGeomFilter with a None geom as first geom, expected None """
		testgeom = None
		expected = None
		self.assertEqual( expected, IntersectGeomFilter(testgeom).filter( Point(0,0) ) )
		
	def test_IntersectGeomFilter_not_geom1(self):
		"""Test IntersectGeomFilter with not a geom as first geom, expected None """
		testgeom = "I am not an geom"
		expected = None
		self.assertEqual( expected, IntersectGeomFilter(testgeom).filter( Point(0,0) ) )
	
	def test_IntersectGeomFilter_none_geom2(self):
		"""Test IntersectGeomFilter with a None geom as second geom, expected None """
		testgeom = None
		expected = None
		self.assertEqual( expected, IntersectGeomFilter( Point(0,0) ).filter( testgeom ) )
		
	def test_IntersectGeomFilter_not_geom2(self):
		"""Test IntersectGeomFilter with not a geom as second geom, expected None """
		testgeom = "I am not an geom"
		expected = None
		self.assertEqual( expected, IntersectGeomFilter( Point(0,0) ).filter( testgeom ) )
	
	def test_IntersectGeomFilter_none_bufferfilter(self):
		"""Test IntersectGeomFilter with None Buffer filter, expected intersection geom """
		testbufferfilter = None
		expected = None
		self.assertEqual( Point(0,0), IntersectGeomFilter( Point(0,0), buffer_filter=testbufferfilter).filter( Point(0,0) ) )
	
	def test_IntersectGeomFilter_not_bufferfilter(self):
		"""Test IntersectGeomFilter with a buffer which is not a Buffer filter, expected None """
		testbufferfilter = "I am not a buffer filter"
		expected = None
		self.assertEqual( expected, IntersectGeomFilter(Point(0,0), buffer_filter=testbufferfilter).filter( Point(0,0) ) )
	
	
	# ClusteringGeomFilter
	
	def test_ClusteringGeomFilter(self):
		"""Test ClusteringGeomFilter in normal conditions """
		testgeom = MultiPoint( [Point(0,0), Point(1, 0)] )
		expected = MultiPoint( [ MultiPoint( [Point(0,0)] ).representative_point() ] )
		self.assertEqual( expected, ClusteringGeomFilter( 100, 1 ).filter( testgeom ) )
	
	def test_ClusteringGeomFilter_one_point(self):
		"""Test ClusteringGeomFilter with one point geometry,expected: original input geometry """
		testgeom = MultiPoint( [Point(0,0)] )
		expected = testgeom
		self.assertEqual( expected, ClusteringGeomFilter( 1, 1 ).filter( testgeom ) )
	
	def test_ClusteringGeomFilter_none_geom(self):
		"""Test ClusteringGeomFilter with None geom, expected None """
		testgeom = None
		expected = None
		self.assertEqual( expected, ClusteringGeomFilter( 1, 1 ).filter( testgeom ) )
		
	def test_ClusteringGeomFilter_not_geom(self):
		"""Test ClusteringGeomFilter with not a geom, expected None """
		testgeom = "I am not an geom"
		expected = None
		self.assertEqual( expected, ClusteringGeomFilter( 1, 1 ).filter( testgeom ) )
	
	def test_ClusteringGeomFilter_none_epsilon(self):
		"""Test ClusteringGeomFilter with None epsilon, expected None """
		testeps = None
		expected = None
		self.assertEqual( expected, ClusteringGeomFilter( testeps, 1 ).filter( [ Point(0,0) ] ) )
	
	def test_ClusteringGeomFilter_not_int_epsilon(self):
		"""Test ClusteringGeomFilter with not int epsilon, expected None """
		testeps = "I am not an int"
		expected = None
		self.assertEqual( expected, ClusteringGeomFilter( testeps , 1 ).filter( [ Point(0,0) ] ) )
	
	def test_ClusteringGeomFilter_negative_epsilon(self):
		"""Test ClusteringGeomFilter with negative epsilon, expected None """
		testeps = -1
		expected = None
		self.assertEqual( expected, ClusteringGeomFilter( testeps , 1 ).filter( [ Point(0,0) ] ) )
	

if __name__ == '__main__':
    unittest.main()