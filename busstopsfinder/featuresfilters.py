from abstractfilters import AbstractFeaturesFilter

class StringPropertyFeaturesFilter(AbstractFeaturesFilter):
	""" StringPropertyFeaturesFilter class filtering features list based on its properties string values """
	_propkey = None
	_propvalue = None
	
	def __init__(self, property_key, property_value):
		""" property_key:		string representing the property key whose value should be checked to apply the filter 
			 property_value:	string representing the value of the property to check to apply the filter
		"""
		self._propkey = property_key
		self._propvalue = property_value
	
	def filter(self, feature_list):
		""" Apply the filter to the passed feature_list and return the fitered features list """
		if self._propkey is None:
			return []
		
		try:
			filtered_features = list()
			for feature in feature_list:
				try:
					if feature['properties'][self._propkey] == self._propvalue:
						filtered_features.append( feature )
				except KeyError:
					pass
		except TypeError:
			return None
		
		return filtered_features


class NotFeaturesFilter(AbstractFeaturesFilter):
	""" NotFeaturesFilter class implemeting the NOT logic on features filters (AbstractFeaturesFilter instances) """
	_featurefilter = None

	def __init__(self, featurefilter):
		""" featurefilter1:	the feature filter (AbstractFeaturesFilter) to which apply the NOT logic """
		self._featurefilter = featurefilter
	
	def filter(self, feature_list):
		""" Apply the filter to the passed feature_list and return the fitered features list """
		try:
			filtered_features = self._featurefilter.filter(feature_list)
			not_filtered_features = list(feature_list)
			for elem in filtered_features:
				not_filtered_features.remove(elem)
		except (AttributeError, TypeError):
			return None
		
		return not_filtered_features


class AndFeaturesFilter(AbstractFeaturesFilter):
	""" AndFeaturesFilter class implemeting the AND logic between features filters (AbstractFeaturesFilter instances) """
	_featurefilter1 = None
	_featurefilter2 = None

	def __init__(self, featurefilter1, featurefilter2):
		""" featurefilter1, featurefilter2:	the 2 feature filters (AbstractFeaturesFilter) to merge using aND logic """
		self._featurefilter1 = featurefilter1
		self._featurefilter2 = featurefilter2
	
	def filter(self, feature_list):
		""" Apply the filter to the passed feature_list and return the fitered features list """
		try:
			and_filtered_features = self._featurefilter1.filter(feature_list)
			and_filtered_features = self._featurefilter2.filter(and_filtered_features)
		except AttributeError:
			return None
		
		return and_filtered_features


class OrFeaturesFilter(AbstractFeaturesFilter):
	""" OrFeaturesFilter class implemeting the OR logic between features filters (AbstractFeaturesFilter instances) """
	_featurefilter1 = None
	_featurefilter2 = None

	def __init__(self, featurefilter1, featurefilter2):
		""" featurefilter1, featurefilter2:	the 2 feature filters (AbstractFeaturesFilter) to merge using OR logic """
		self._featurefilter1 = featurefilter1
		self._featurefilter2 = featurefilter2
	
	def filter(self, feature_list):
		""" Apply the filter to the passed feature_list and return the fitered features list """
		try:
			or_filtered_features = self._featurefilter1.filter(feature_list)
			filtered2_list = self._featurefilter2.filter(feature_list)
			
			for feature in filtered2_list:
				if not feature in or_filtered_features:
					or_filtered_features.append(feature)
		except (AttributeError, TypeError):
			return None
		
		return or_filtered_features