import unittest
from busstopsfinder.geometriesfilters import *
from shapely.geometry import Point


class GeometriesFiltersIntegrationTestCase(unittest.TestCase):
	"""Integration Tests for `geometriesfilters.py`."""
	
	# IntersectGeomFilter
	
	def test_IntersectGeomFilter_None_returning_bufferfilter(self):
		"""Test IntersectGeomFilter with a buffer filter which returns None, expected None """
		testbufferfilter = BufferGeomFilter(None)
		expected = None
		self.assertEqual( expected, IntersectGeomFilter(Point(0,0), buffer_filter=testbufferfilter).filter( Point(0,0) ) )
	
	
	def test_IntersectGeomFilter_same_buffered_geom(self):
		"""Test IntersectGeomFilter on a geom and teh same geom buffered (core functionality correctness granted by the shapely lib), expected: original geom """
		testgeom = Point(0,0)
		expected = Point(0,0)

		self.assertEqual( expected, IntersectGeomFilter(testgeom, buffer_filter=BufferGeomFilter(10) ).filter( testgeom ) )
	

if __name__ == '__main__':
    unittest.main()