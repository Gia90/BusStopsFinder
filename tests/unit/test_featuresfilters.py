import unittest
from tests.utilities import featuresPropsL
from busstopsfinder.featuresfilters import *

class FeaturesFiltersUnitTestCase(unittest.TestCase):
	"""Unit Tests for `featuresfilters.py`."""
	
	def test_StringPropertyFF_none_as_propkey(self):
		"""Test StringPropertyFeaturesFilter with "None" as prop key, expected value: [] """
		
		testfeatures = featuresPropsL( [ 
												{"random_testkey": "random_testvalue1"},
												{"random_testvalue2": "random_testvalue3"}
											])
		
		self.assertEqual( [], StringPropertyFeaturesFilter(None, "testvalue").filter(testfeatures) )
	
	
	def test_StringPropertyFF_none_as_propvalue(self):
		"""Test StringPropertyFeaturesFilter with "None" as prop value, expected value: expected """
		
		testfeatures = featuresPropsL( [
												{"testkey": "random_testvalue1"},
												{"testkey": None},
												{"testkey": "random_testvalue3"}
											])
		
		expected = featuresPropsL( [{"testkey": None}] )
		self.assertEqual( expected, StringPropertyFeaturesFilter("testkey", None).filter(testfeatures) )
	
	def test_StringPropertyFF_none_as_features(self):
		"""Test StringPropertyFeaturesFilter on "None" features list, expected value: "None" """
		
		self.assertEqual( None, StringPropertyFeaturesFilter("testkey", "testvalue").filter(None) )
	
	def test_StringPropertyFF_no_features(self):
		"""Test StringPropertyFeaturesFilter on empty features list, expected value: empy list"""
		
		self.assertEqual( [], StringPropertyFeaturesFilter("testkey", "testvalue").filter([]) )

	def test_StringPropertyFF_already_filtered(self):
		"""Test StringPropertyFeaturesFilter on features list containing all accepted properties, expected value: imput list"""
		
		expected = testfeatures = featuresPropsL( [{"testkey": "testvalue"}] )
		self.assertEqual( testfeatures, StringPropertyFeaturesFilter("testkey", "testvalue").filter(testfeatures) )

	def test_StringPropertyFF_to_be_filtered_same_keys(self):
		"""Test StringPropertyFeaturesFilter on features list containing properties to be filtered all with same keys"""
		
		expected = featuresPropsL( [{"testkey": "testvalue"}] )
		testfeatures = featuresPropsL( [
												{"testkey": "testvalue"},
												{"testkey": "filter_me_testvalue"},
												{"testkey": "filter_me_too_testvalue"}
											])
		self.assertEqual( expected, StringPropertyFeaturesFilter("testkey", "testvalue").filter(testfeatures) )
	
	def test_StringPropertyFF_to_be_filtered_different_keys(self):
		"""Test StringPropertyFeaturesFilter on features list containing properties to be filtered with different keys"""
		
		expected = featuresPropsL( [{"testkey": "testvalue"}] )
		testfeatures = featuresPropsL( [
												{"testkey": "testvalue"},
												{"testkey2": "filter_me_testvalue"},
												{"testkey3": "filter_me_too_testvalue"}
											])
		
		self.assertEqual( expected, StringPropertyFeaturesFilter("testkey", "testvalue").filter(testfeatures) )
	
	
	# NotFeaturesFilter
	
	def test_NotFeaturesFilter_none_filter(self):
		"""Test NotFeaturesFilter with None filter, expected: None"""
		
		testfeatures = featuresPropsL( [{"testkey": "testvalue"}])
		self.assertEqual( None, NotFeaturesFilter(None).filter(testfeatures) )
	
	def test_NotFeaturesFilter_no_features(self):
		"""Test NotFeaturesFilter with empty features list, expected [] """
		expected = []
		testfeatures = []
		
		self.assertEqual( expected, NotFeaturesFilter( StringPropertyFeaturesFilter("testkey", "testvalue") ).filter(testfeatures) )
	
	def test_NotFeaturesFilter_none_features(self):
		"""Test NotFeaturesFilter with None features list, expected None """
		expected = None
		testfeatures = None
		
		self.assertEqual( expected, NotFeaturesFilter( StringPropertyFeaturesFilter("testkey", "testvalue") ).filter(testfeatures) )
	
	
	# AndFeaturesFilter
	
	def test_AndFeaturesFilter_none_filter(self):
		"""Test AndFeaturesFilter with None filter, expected: None"""
		
		testfeatures = featuresPropsL( [{"testkey": "testvalue"}])
		self.assertEqual( None, AndFeaturesFilter(None, None).filter(testfeatures) )
	
	def test_AndFeaturesFilter_none_features(self):
		"""Test AndFeaturesFilter with None features list, expected None """
		expected = None
		testfeatures = None
		
		self.assertEqual( expected, AndFeaturesFilter( StringPropertyFeaturesFilter("testkey1", "testvalue1"), StringPropertyFeaturesFilter("testkey2", "testvalue2") ).filter(testfeatures) )
	
	def test_AndFeaturesFilter_no_features(self):
		"""Test AndFeaturesFilter with empty features list, expected [] """
		expected = []
		testfeatures = []
		
		self.assertEqual( expected, AndFeaturesFilter( StringPropertyFeaturesFilter("testkey1", "testvalue1"), StringPropertyFeaturesFilter("testkey2", "testvalue2") ).filter(testfeatures) )
	
	
	
	# OrFeaturesFilter
	
	def test_OrFeaturesFilter_none_filter(self):
		"""Test OrFeaturesFilter with None filter, expected: None"""
		
		testfeatures = featuresPropsL( [{"testkey": "testvalue"}])
		self.assertEqual( None, OrFeaturesFilter(None, None).filter(testfeatures) )
	
	def test_OrFeaturesFilter_none_features(self):
		"""Test OrFeaturesFilter with None features list, expected None """
		expected = None
		testfeatures = None
		
		self.assertEqual( expected, OrFeaturesFilter( StringPropertyFeaturesFilter("testkey1", "testvalue1"), StringPropertyFeaturesFilter("testkey2", "testvalue2") ).filter(testfeatures) )
	
	def test_OrFeaturesFilter_no_features(self):
		"""Test OrFeaturesFilter with empty features list, expected [] """
		expected = []
		testfeatures = []
		
		self.assertEqual( expected, AndFeaturesFilter( StringPropertyFeaturesFilter("testkey1", "testvalue1"), StringPropertyFeaturesFilter("testkey2", "testvalue2") ).filter(testfeatures) )
	
	
	
if __name__ == '__main__':
    unittest.main()