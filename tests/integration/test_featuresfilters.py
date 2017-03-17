import unittest
from tests.utilities import featuresPropsL
from busstopsfinder.featuresfilters import *

class FeaturesFiltersIntegrationTestCase(unittest.TestCase):
	"""Integration Tests for `featuresfilters.py`."""
	
	# AndFeaturesFilter
	
	def test_NotFeaturesFilter_acceptingAll_StringPropFF_all_accepted(self):
		"""Test NotFeaturesFilter with an "accepting-all" StringPropFeaturesFilter, expected [] """
		expected = []
		testfeatures = featuresPropsL( [ {"testkey": "testvalue"} ] )
		
		self.assertEqual( expected, NotFeaturesFilter( StringPropertyFeaturesFilter("testkey", "testvalue") ).filter(testfeatures) )
	
	def test_NotFeaturesFilter_uneffective_StringPropFF(self):
		"""Test NotFeaturesFilter with uneffective StringPropFeaturesFilter, expected original input list """
		expected = featuresPropsL( [ {"testkey": "not_filterme_testvalue"} ] )
		testfeatures = featuresPropsL( [ {"testkey": "not_filterme_testvalue"} ] )
		
		self.assertEqual( expected, NotFeaturesFilter( StringPropertyFeaturesFilter("testkey", "testvalue") ).filter(testfeatures) )
	
	def test_NotFeaturesFilter_StringPropFF_to_be_filtered(self):
		"""Test NotFeaturesFilter on StringPropFeaturesFilter """
		expected = featuresPropsL( [
											{"testkey": "not_filter_me_testvalue"},
											{"testkey": "not_filter_me_too_testvalue"}
										])
		testfeatures = featuresPropsL( [
												{"testkey": "testvalue"},
												{"testkey": "not_filter_me_testvalue"},
												{"testkey": "not_filter_me_too_testvalue"}
											])
		
		self.assertEqual( expected, NotFeaturesFilter( StringPropertyFeaturesFilter("testkey", "testvalue") ).filter(testfeatures) )
		
	# AndFeaturesFilter
	
	def test_AndFeaturesFilter_uneffective_StringPropFF(self):
		"""Test AndFeaturesFilter with any StringPropFeaturesFilter being uneffective, expected [] """
		uneffective_StringPropFilter = StringPropertyFeaturesFilter("testkey", "uneffective")
		
		testfeatures = featuresPropsL( [
												{
													"testkey": "testvalue",
													"testkey1": "testvalue123"
												},
												{	"testkey": "testvalue123"	}
											] )
		expected = []
		
		self.assertEqual( expected, AndFeaturesFilter( uneffective_StringPropFilter, StringPropertyFeaturesFilter("testkey", "testvalue") ).filter(testfeatures) )
		self.assertEqual( expected, AndFeaturesFilter( StringPropertyFeaturesFilter("testkey", "testvalue"), uneffective_StringPropFilter ).filter(testfeatures) )
		self.assertEqual( expected, AndFeaturesFilter( uneffective_StringPropFilter, uneffective_StringPropFilter ).filter(testfeatures) )
	
	def test_AndFeaturesFilter_acceptingAll_StringPropFF(self):
		"""Test AndFeaturesFilter with only one first or second StringPropFeaturesFilter accepting all the features, expected the same result as the not "accepting-all" StringPropFeaturesFilter of the 2, on the original list  """
		acceptingAll_StringPropFilter = StringPropertyFeaturesFilter("testkey", "accepted")
		not_acceptingAll_StringPropFilter = StringPropertyFeaturesFilter("testkey1", "testvalue123")

		testfeatures = featuresPropsL( [
												{
													"testkey": "accepted",
													"testkey1": "testvalue123",
													"testkey2": "testvalue"
												},
												{	"testkey": "accepted"	}
											] )
		expected = not_acceptingAll_StringPropFilter.filter(testfeatures)
		
		self.assertEqual( expected, AndFeaturesFilter( acceptingAll_StringPropFilter, not_acceptingAll_StringPropFilter ).filter(testfeatures) )
		self.assertEqual( expected, AndFeaturesFilter( not_acceptingAll_StringPropFilter, acceptingAll_StringPropFilter ).filter(testfeatures) )
	
	def test_AndFeaturesFilter_both_acceptingAll_StringPropFF(self):
		"""Test AndFeaturesFilter with 2 StringPropFeaturesFilter accepting all the props, expected the same result as same StringPropFeaturesFilter on the original list """
		testfeatures = featuresPropsL( [
												{
													"testkey": "accepted",
													"testkey1": "testvalue123"
												},
												{	"testkey": "accepted"	}
											] )
		expected = testfeatures
		
		self.assertEqual( expected, AndFeaturesFilter( StringPropertyFeaturesFilter("testkey", "accepted"), StringPropertyFeaturesFilter("testkey", "accepted") ).filter(testfeatures) )
	
	
	def test_AndFeaturesFilter_same_StringPropFF(self):
		"""Test AndFeaturesFilter with 2 same StringPropFeaturesFilter, expected the same result as same StringPropFeaturesFilter on the original list """
		testfeatures = featuresPropsL( [
												{
													"testkey": "testvalue",
													"testkey1": "testvalue123"
												},
												{	"testkey": "testvalue123"	}
											] )
		expected = StringPropertyFeaturesFilter("testkey", "testvalue").filter(testfeatures)

		
		self.assertEqual( expected, AndFeaturesFilter( StringPropertyFeaturesFilter("testkey", "testvalue"), StringPropertyFeaturesFilter("testkey", "testvalue") ).filter(testfeatures) )
	
	def test_AndFeaturesFilter_StringPropFF_to_be_filtered(self):
		"""Test AndFeaturesFilter on StringPropFeaturesFilter """
		expected = featuresPropsL( [ {
													"testkey1": "testvalue1",
													"testkey2": "testvalue2",
													"testkey3": "testvalue3"
												}
										] )
		testfeatures = featuresPropsL( [
												{
													"testkey1": "testvalue1",
													"testkey2": "testvalue2",
													"testkey3": "testvalue3"
												}, 
												{
													"testkey2": "testvalue2"
												},
												{
													"testkey1": "testvalue1",
													"testkey2": "testvalue123"
												}
											] )
		
		self.assertEqual( expected, AndFeaturesFilter( StringPropertyFeaturesFilter("testkey1", "testvalue1"), StringPropertyFeaturesFilter("testkey2", "testvalue2") ).filter(testfeatures) )
	
	
	# OrFeaturesFilter
	
	def test_OrFeaturesFilter_uneffective_StringPropFF(self):
		"""Test OrFeaturesFilter with the first or second StringPropFeaturesFilter being uneffective, expected the same result as the not "uneffective" StringPropFeaturesFilter of the 2, on the original list """
		uneffective_StringPropFilter = StringPropertyFeaturesFilter("testkey", "uneffective")
		effective_StringPropFilter = StringPropertyFeaturesFilter("testkey", "testvalue")
		
		testfeatures = featuresPropsL( [
												{
													"testkey": "testvalue",
													"testkey1": "testvalue123"
												},
												{	"testkey": "testvalue123"	}
											] )
		expected = effective_StringPropFilter.filter(testfeatures)
		
		self.assertEqual( expected, OrFeaturesFilter( uneffective_StringPropFilter, effective_StringPropFilter ).filter(testfeatures) )
		self.assertEqual( expected, OrFeaturesFilter( effective_StringPropFilter, uneffective_StringPropFilter ).filter(testfeatures) )
	
	def test_OrFeaturesFilter_both_uneffective_StringPropFF(self):
		"""Test OrFeaturesFilter with both StringPropFeaturesFilter being uneffective, expected [] """
		uneffective_StringPropFilter = StringPropertyFeaturesFilter("testkey", "uneffective")
		
		testfeatures = featuresPropsL( [
												{
													"testkey": "testvalue",
													"testkey1": "testvalue123"
												},
												{	"testkey": "testvalue123"	}
											] )
		expected = []
		
		self.assertEqual( expected, AndFeaturesFilter( uneffective_StringPropFilter, uneffective_StringPropFilter ).filter(testfeatures) )
	
	
	def test_OrFeaturesFilter_acceptingAll_StringPropFF(self):
		"""Test OrFeaturesFilter with any StringPropFeaturesFilter accepting all the features, expected the original list  """
		
		acceptingAll_StringPropFilter = StringPropertyFeaturesFilter("testkey", "accepted")
		not_acceptingAll_StringPropFilter = StringPropertyFeaturesFilter("testkey1", "testvalue123")

		testfeatures = featuresPropsL( [
												{
													"testkey": "accepted",
													"testkey1": "testvalue123",
													"testkey2": "testvalue"
												},
												{	"testkey": "accepted"	}
											] )
		expected = testfeatures
		
		self.assertEqual( expected, OrFeaturesFilter( acceptingAll_StringPropFilter, not_acceptingAll_StringPropFilter ).filter(testfeatures) )
		self.assertEqual( expected, OrFeaturesFilter( not_acceptingAll_StringPropFilter, acceptingAll_StringPropFilter ).filter(testfeatures) )
		self.assertEqual( expected, OrFeaturesFilter( acceptingAll_StringPropFilter, acceptingAll_StringPropFilter ).filter(testfeatures) )
	
	
	def test_OrFeaturesFilter_same_StringPropFF(self):
		"""Test OrFeaturesFilter with 2 same StringPropFeaturesFilter, expected the same result as same StringPropFeaturesFilter on the original list """
		testfeatures = featuresPropsL( [
												{
													"testkey": "testvalue",
													"testkey1": "testvalue123"
												},
												{	"testkey": "testvalue123"	}
											] )
		expected = StringPropertyFeaturesFilter("testkey", "testvalue").filter(testfeatures)

		
		self.assertEqual( expected, AndFeaturesFilter( StringPropertyFeaturesFilter("testkey", "testvalue"), StringPropertyFeaturesFilter("testkey", "testvalue") ).filter(testfeatures) )
	
	def test_OrFeaturesFilter_StringPropFF_to_be_filtered(self):
		"""Test OrFeaturesFilter on StringPropFeaturesFilter """
		expected = featuresPropsL( [ {
													"testkey1": "testvalue1",
													"testkey2": "testvalue2",
													"testkey3": "testvalue3"
												}, 
												{
													"testkey2": "testvalue2"
												}
										] )
		testfeatures = featuresPropsL( [
												{
													"testkey1": "testvalue1",
													"testkey2": "testvalue2",
													"testkey3": "testvalue3"
												}, 
												{
													"testkey2": "testvalue2"
												},
												{
													"testkey1": "testvalue123",
													"testkey2": "testvalue123"
												}
											] )
		
		self.assertEqual( expected, OrFeaturesFilter( StringPropertyFeaturesFilter("testkey1", "testvalue1"), StringPropertyFeaturesFilter("testkey2", "testvalue2") ).filter(testfeatures) )
		
	
	
if __name__ == '__main__':
    unittest.main()