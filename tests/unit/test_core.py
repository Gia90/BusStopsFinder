import unittest
from busstopsfinder.core import *
from busstopsfinder.core import _ActivityFeaturesFilter
from tests.utilities import featuresPropsL

class CoreUnitTestCase(unittest.TestCase):
	"""Unit Tests for `core.py`."""
	
	# geoJson_data activity keys
	_prev_activity_key = "previous_dominating_activity"
	_cur_activity_key = "current_dominating_activity"
	
	# _ActivityFeaturesFilter
	
	def test_ActivityFeaturesFilter_cautious_results(self):
		"""Test _ActivityFeaturesFilter at cautious level with some results """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "still",
															self._cur_activity_key:	"in_vehicle"
														}
													])
													
		expected = testfeatures
		
		self.assertEqual( expected, _ActivityFeaturesFilter( Levels.CAUTIOUS ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_cautious_NOresults(self):
		"""Test _ActivityFeaturesFilter at cautious level with empty results [] (but it would have been accepted if level=NORMAL) """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "still",
															self._cur_activity_key:	None
														}
													])
													
		expected = featuresPropsL( [] )
		
		self.assertEqual( expected, _ActivityFeaturesFilter( Levels.CAUTIOUS ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_normal_results(self):
		"""Test _ActivityFeaturesFilter at normal level with some results """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "still",
															self._cur_activity_key:	None
														}
													])
													
		expected = testfeatures
		
		self.assertEqual( expected, _ActivityFeaturesFilter( Levels.NORMAL ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_normal_NOresults(self):
		"""Test _ActivityFeaturesFilter at normal level with empty result [] (but it would have been accepted if level=AGGRESSIVE) """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "on_foot",
															self._cur_activity_key:	None
														}
													])
													
		expected = featuresPropsL( [] )
		
		self.assertEqual( expected, _ActivityFeaturesFilter( Levels.NORMAL ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_aggressive_results(self):
		"""Test _ActivityFeaturesFilter at aggressive level with some results """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "on_foot",
															self._cur_activity_key:	None
														}
													])
													
		expected = testfeatures
		
		self.assertEqual( expected, _ActivityFeaturesFilter( Levels.AGGRESSIVE ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_aggressive_NOresults(self):
		"""Test _ActivityFeaturesFilter at aggressive level with empty results [] """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "on_foot",
															self._cur_activity_key:	"on_bicycle"
														}
													])
													
		expected = featuresPropsL( [] )
		
		self.assertEqual( expected, _ActivityFeaturesFilter( Levels.AGGRESSIVE ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_anylevel_NOresults(self):
		"""Test _ActivityFeaturesFilter at any level with empty results [] """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: None,
															self._cur_activity_key:	None
														}
													])
													
		expected = featuresPropsL( [] )
		
		self.assertEqual( expected, _ActivityFeaturesFilter( Levels.NORMAL ).filter(testfeatures) )
		self.assertEqual( expected, _ActivityFeaturesFilter( Levels.CAUTIOUS ).filter(testfeatures) )
		self.assertEqual( expected, _ActivityFeaturesFilter( Levels.AGGRESSIVE ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_none_features(self):
		"""Test _ActivityFeaturesFilter with negative level, expected value: same output of  _ActivityFeaturesFilter with level NORMAL """
		
		testfeatures = None
		expected = None
		
		self.assertEqual( expected, _ActivityFeaturesFilter( ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_no_features(self):
		"""Test _ActivityFeaturesFilter with no features, expected: [] """
		
		testfeatures = []
		expected = []
		
		self.assertEqual( expected, _ActivityFeaturesFilter( ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_not_features(self):
		"""Test _ActivityFeaturesFilter with not a features, expected: [] """
		
		testfeatures = "I am not features"
		expected = None
		
		self.assertEqual( expected, _ActivityFeaturesFilter( ).filter(testfeatures) )
	
	
	def test_ActivityFeaturesFilter_negative_level(self):
		"""Test _ActivityFeaturesFilter with negative level, expected value: same output of  _ActivityFeaturesFilter with level NORMAL """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "on_foot",
															self._cur_activity_key:	"still"
														}
													])
		
		testlevel = -2
		expected = _ActivityFeaturesFilter( Levels.NORMAL ).filter(testfeatures)
		
		self.assertEqual( expected, _ActivityFeaturesFilter( testlevel ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_overmax_level(self):
		"""Test _ActivityFeaturesFilter with a level over the maximum, expected value: same output of  _ActivityFeaturesFilter with level NORMAL """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "on_foot",
															self._cur_activity_key:	None
														}
													])
		
		testlevel = 999
		expected = _ActivityFeaturesFilter( Levels.NORMAL ).filter(testfeatures)
		
		self.assertEqual( expected, _ActivityFeaturesFilter( testlevel ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_none_level(self):
		"""Test _ActivityFeaturesFilter with a None level, expected value: same output of  _ActivityFeaturesFilter with level NORMAL """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "on_foot",
															self._cur_activity_key:	None
														}
													])
		
		testlevel = None
		expected = _ActivityFeaturesFilter( ).filter(testfeatures)
		
		self.assertEqual( expected, _ActivityFeaturesFilter( testlevel ).filter(testfeatures) )
	
	def test_ActivityFeaturesFilter_not_level(self):
		"""Test _ActivityFeaturesFilter with a not a valid level, expected value: same output of  _ActivityFeaturesFilter with level NORMAL """
		
		testfeatures = featuresPropsL( [ 
														{
															self._prev_activity_key: "on_foot",
															self._cur_activity_key:	None
														}
													])
		
		testlevel = "I am not a valid level"
		expected = _ActivityFeaturesFilter( Levels.NORMAL ).filter(testfeatures)
		
		self.assertEqual( expected, _ActivityFeaturesFilter( testlevel ).filter(testfeatures) )
	
	
	# Levels
	
	def test_Levels_str(self):
		""" Test Levels str method in normal conditions, expected corresponding string representation of the level """
		
		testCautiousLevel = Levels.CAUTIOUS
		expectedCautios = "CAUTIOUS"
		
		testNormalLevel = Levels.NORMAL
		expectedNormal = "NORMAL"
		
		testAggressiveLevel = Levels.AGGRESSIVE
		expectedAggressive = "AGGRESSIVE"
		
		self.assertEqual( expectedCautios, Levels.str(testCautiousLevel) )
		self.assertEqual( expectedNormal, Levels.str(testNormalLevel) )
		self.assertEqual( expectedAggressive, Levels.str(testAggressiveLevel) )
	
	def test_Levels_str_none_level(self):
		""" Test Levels str method passing a None level, expected: "UNKNOWN" """
		
		testLevel = None
		expected = "UNKNOWN"
		
		self.assertEqual( expected, Levels.str( testLevel ) )
	
	def test_Levels_str_not_level(self):
		""" Test Levels str method passing not a valid level, expected: "UNKNOWN" """
		
		testLevel = "I am not a valid level"
		expected = "UNKNOWN"
		
		self.assertEqual( expected, Levels.str( testLevel ) )
	
	def test_Levels_str_negative_level(self):
		""" Test Levels str method passing a negative level value, expected: "UNKNOWN" """
		
		testLevel = -999
		expected = "UNKNOWN"
		
		self.assertEqual( expected, Levels.str( testLevel ) )
	
	def test_Levels_str_overmax_level(self):
		""" Test Levels str method passing a level over the maximum value, expected: "UNKNOWN" """
		
		testLevel = 999
		expected = "UNKNOWN"
		
		self.assertEqual( expected, Levels.str( testLevel ) )
	
	def test_Levels_valid(self):
		""" Test Levels valid method in normal conditions with valid Level, expected True """
		
		testCautiousLevel = Levels.CAUTIOUS
		testNormalLevel = Levels.NORMAL
		testAggressiveLevel = Levels.AGGRESSIVE
		expectedValid = True
		
		self.assertEqual( expectedValid, Levels.valid(testCautiousLevel) )
		self.assertEqual( expectedValid, Levels.valid(testNormalLevel) )
		self.assertEqual( expectedValid, Levels.valid(testAggressiveLevel) )
	
	def test_Levels_valid_none_level(self):
		""" Test Levels valid method in normal conditions with valid Level, expected True """
		
		testLevel = None
		expectedValid = False
		
		self.assertEqual( expectedValid, Levels.valid(testLevel) )
	
	def test_Levels_valid_not_level(self):
		""" Test Levels valid method in normal conditions with valid Level, expected True """
		
		testLevel = "I am not a valid level"
		expectedValid = False
		
		self.assertEqual( expectedValid, Levels.valid(testLevel) )
	
	def test_Levels_valid_negative_level(self):
		""" Test Levels valid method passing a negative level value, expected: False """
		
		testLevel = -999
		expectedValid = False
		
		self.assertEqual( expectedValid, Levels.valid( testLevel ) )
	
	def test_Levels_valid_overmax_level(self):
		""" Test Levels valid method passing a level over the maximum value, expected: False """
		
		testLevel = 999
		expectedValid = False
		
		self.assertEqual( expectedValid, Levels.valid( testLevel ) )
	
	
	# Status
	
	def test_Status_str(self):
		""" Test Status str method in normal conditions, expected corresponding string representation of the Status """
		
		testNoneStatus = Status.NONE
		expectedNone = "NONE"
		
		testCompletedStatus = Status.COMPLETED
		expectedCompleted = "COMPLETED"
		
		testErrorStatus = Status.ERROR
		expectedError = "ERROR"
		
		testRunningStatus = Status.RUNNING
		expectedRunning = "RUNNING"
		
		self.assertEqual( expectedNone, Status.str(testNoneStatus) )
		self.assertEqual( expectedCompleted, Status.str(testCompletedStatus) )
		self.assertEqual( expectedError, Status.str(testErrorStatus) )
		self.assertEqual( expectedRunning, Status.str(testRunningStatus) )
	
	def test_Status_str_none_level(self):
		""" Test Status str method passing a None status, expected: "UNKNOWN" """
		
		testStatus = None
		expected = "UNKNOWN"
		
		self.assertEqual( expected, Status.str( testStatus ) )
	
	def test_Status_str_not_level(self):
		""" Test Status str method passing not a valid level, expected: "UNKNOWN" """
		
		testStatus = "I am not a valid level"
		expected = "UNKNOWN"
		
		self.assertEqual( expected, Status.str( testStatus ) )
	
	def test_Status_str_negative_level(self):
		""" Test Status str method passing a negative status value, expected: "UNKNOWN" """
		
		testStatus = -999
		expected = "UNKNOWN"
		
		self.assertEqual( expected, Status.str( testStatus ) )
	
	def test_Status_str_overmax_level(self):
		""" Test Status str method passing a status over the maximum value, expected: "UNKNOWN" """
		
		testStatus = 999
		expected = "UNKNOWN"
		
		self.assertEqual( expected, Status.str( testStatus ) )
	
	
	# BusStopFinder

	def test_BusStopFinder_none_points(self):
		""" Test BusStopFinder passing None as points, expected: ValueError Exception """
		testpoints = None
		expected = ValueError
		
		with self.assertRaises(expected):	BusStopFinder(testpoints, geoJson_routes=None).find()
	
	def test_BusStopFinder_not_points(self):
		""" Test BusStopFinder passing "not a geometry" points, expected: ValueError Exception """
		testpoints = "I am not points"
		expected = ValueError
		
		with self.assertRaises(expected):	BusStopFinder(testpoints).find()
	
	def test_BusStopFinder_not_valid_points(self):
		""" Test BusStopFinder passing a not valid geometry points, expected: ValueError Exception """
		testpoints = { "Not a valid": "geometry" }
		expected = ValueError
		
		with self.assertRaises(expected):	BusStopFinder(testpoints).find()
	
	def test_BusStopFinder_no_points(self):
		""" Test BusStopFinder passing empty geometry points, expected: empty geojson {} """
		testpoints = { "features":  [] }
		expected = {}
		
		self.assertEqual( expected, BusStopFinder(testpoints).find() )
	
	def test_BusStopFinder_none_routes(self):
		""" Test BusStopFinder passing None geometryroutes, expected:same outuput as if level=NORMAL """
		testroutes = None
		expected = BusStopFinder({ "features":  [] }).find()
		
		self.assertEquals(expected, BusStopFinder({ "features":  [] }, geoJson_routes=testroutes).find() )
	
	def test_BusStopFinder_not_routes(self):
		""" Test BusStopFinder passing "not a geometry" routes, expected: ValueError Exception """
		testroutes = "I am not routes"
		expected = ValueError
		
		with self.assertRaises(expected):	BusStopFinder({ "features":  [] }, geoJson_routes=testroutes).find()
	
	def test_BusStopFinder_not_valid_routes(self):
		""" Test BusStopFinder passing a not valid geometry points, expected: ValueError Exception """
		testroutes = { "Not a valid": "geometry" }
		expected = ValueError
		
		with self.assertRaises(expected):	BusStopFinder({ "features":  [] }, geoJson_routes=testroutes).find()
	
	def test_BusStopFinder_no_routes(self):
		""" Test BusStopFinder passing empty geometry routes, expected: empty geojson {} """
		testroutes = { "features":  [] }
		expected = {}
		
		self.assertEqual( expected, BusStopFinder({ "features":  [] }, geoJson_routes=testroutes).find() )
	
	def test_BusStopFinder_negative_level(self):
		""" Test BusStopFinder passing negative level, expected: same outuput as if level=NORMAL """
		testlevel = -123
		expected = BusStopFinder({ "features":  [] }).find()
		
		self.assertEqual( expected, BusStopFinder({ "features":  [] }, level=testlevel).find() )
	
	
	def test_BusStopFinder_overmax_level(self):
		""" Test BusStopFinder passing overmax level, expected: same outuput as if level=NORMAL """
		testlevel = 123
		expected = BusStopFinder({ "features":  [] }).find()
		
		self.assertEqual( expected, BusStopFinder({ "features":  [] }, level=testlevel).find() )
	
	
	def test_ActivityFeaturesFilter_none_level(self):
		""" Test BusStopFinder passing None level, expected: same outuput as if level=NORMAL """
		testlevel = None
		expected = BusStopFinder({ "features":  [] }).find()
		
		self.assertEqual( expected, BusStopFinder({ "features":  [] }, level=testlevel).find() )
	
	
	def test_ActivityFeaturesFilter_not_level(self):
		""" Test BusStopFinder passing not valid level, expected: same outuput as if level=NORMAL """
		testlevel = "I am not a level"
		expected = BusStopFinder({ "features":  [] }).find()
		
		self.assertEqual( expected, BusStopFinder({ "features":  [] }, level=testlevel).find() )
	
	

if __name__ == '__main__':
    unittest.main()