import copy

__feature_template = {
									"type": "Feature",
									"properties": {},
									"geometry": {}
								}

def __featuresL( fieldkey, values_list ):
	features_list = []
	for values in values_list:
		feature = copy.deepcopy(__feature_template)
		feature[fieldkey] = values
		features_list.append( feature )
	return features_list

def featuresPropsL( props_list ):
	""" Create Features List with the specified properties  """
	return __featuresL( "properties", props_list)

def featuresGeomsL( geoms_list ):
	""" Create Features List with the specified geometries """
	return __featuresL( "geometry", geoms_list)

