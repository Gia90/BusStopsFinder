from featuresfilters import *
from geometriesfilters import *
from converterfilters import *

class Levels:
	""" Class containing the "Aggressivity" level for the filters 
			CAUTIOUS:		Less false positives, but maybe ignores some possible bus stops
			NORMAL:			Normal level, the default one
			AGGRESSIVE:	More false negatives, but more propability to detect wrong points
		"""
	CAUTIOUS = 0
	NORMAL = 1
	AGGRESSIVE = 2
	
	__levelsstr = ("CAUTIOUS","NORMAL","AGGRESSIVE")
	@classmethod
	def str(cls, level):
		""" Get string representation of the passed level """
		try:
			level_str = cls.__levelsstr[level]
		except (IndexError, TypeError):
			return "UNKNOWN"
		
		return level_str
	
	@classmethod
	def valid(cls, level):
		""" Is the passed level valid? """
		try:
			cls.__levelsstr[level]
		except (IndexError, TypeError):	
			return False
		
		return True


class _ActivityFeaturesFilter(AbstractFeaturesFilter):
	""" _ActivityFeaturesFilter is a custom FeaturesFilter to filter activity points features based on their Dominating Activity properties, trying to detect people waiting for, getting in or out of a bus """
	_filter = None
	
	# geoJson_data activity keys
	_prev_activity_key = "previous_dominating_activity"
	_cur_activity_key = "current_dominating_activity"
	
	# Create filters for needed "Current Dominating Activity"
	_prev_activity_still = StringPropertyFeaturesFilter(_prev_activity_key, "still")
	#_prev_activity_onfoot = StringPropertyFeaturesFilter(_prev_activity_key, "on_foot")
	#_prev_activity_onbicycle = StringPropertyFeaturesFilter(_prev_activity_key, "on_bicycle")
	_prev_activity_invehicle = StringPropertyFeaturesFilter(_prev_activity_key, "in_vehicle")
	_prev_activity_none = StringPropertyFeaturesFilter(_prev_activity_key, None)

	# Create filters for needed "Previous Dominating Activity"
	#_cur_activity_still = StringPropertyFeaturesFilter(_cur_activity_key, "still")
	#_cur_activity_onfoot = StringPropertyFeaturesFilter(_cur_activity_key, "on_foot")
	#_cur_activity_onbicycle = StringPropertyFeaturesFilter(_cur_activity_key, "on_bicycle")
	_cur_activity_invehicle = StringPropertyFeaturesFilter(_cur_activity_key, "in_vehicle")
	_cur_activity_none = StringPropertyFeaturesFilter(_cur_activity_key, None)
		
	
	def __init__(self, level=Levels.NORMAL):
		""" level:	(optional) Aggresivity level (see Levels class docs) """
		level = level if ( (level is not None) and (Levels.valid(level)) ) else Levels.NORMAL
		
		# if( level >= Levels.CAUTIOUS):
		# People getting into or out of a vehicle (bus?)
		into_vehicle = AndFeaturesFilter( NotFeaturesFilter(self._prev_activity_invehicle), self._cur_activity_invehicle)
		outof_vehicle = AndFeaturesFilter( self._prev_activity_invehicle, NotFeaturesFilter( self._cur_activity_invehicle ) )
		filter =  OrFeaturesFilter( into_vehicle, outof_vehicle )
		
		if( level >= Levels.NORMAL ):	
			# People who are "still" and then become "None" (maybe they were waiting still and are in a vehicle now?)
			still2none = AndFeaturesFilter( self._prev_activity_still, self._cur_activity_none)
			# Merge (OR) this filter to the "NORMAL" one
			filter = OrFeaturesFilter( filter, still2none )
		
		if( level >= Levels.AGGRESSIVE ):	
			# People who were not in a vehicle (and not None) and now are "None" (maybe they are in a vehicle now?)
			notinvehicle2none = AndFeaturesFilter( AndFeaturesFilter( NotFeaturesFilter( self._prev_activity_invehicle), NotFeaturesFilter( self._prev_activity_none)) , self._cur_activity_none)
			# People who were "None" (maybe they were in a vehicle?) and now they got out of a vehicle  (and are not None)
			none2notinvehicle = AndFeaturesFilter( self._prev_activity_none, AndFeaturesFilter( NotFeaturesFilter( self._cur_activity_invehicle ), NotFeaturesFilter( self._cur_activity_none ) ) )
			
			filter = OrFeaturesFilter( filter, OrFeaturesFilter( notinvehicle2none, none2notinvehicle)  )
		
		self._filter = filter
	
	def filter(self, features_list):
		""" Apply the filter and returns a features list """
		return self._filter.filter( features_list )


class Status:
	""" Status class containing the possible status of the processing (NONE, COMPLETED, ERROR, RUNNING) """
	NONE = -1
	COMPLETED = 0
	ERROR = 1
	RUNNING = 2
	
	__statusstr = ("NONE","COMPLETED","ERROR","RUNNING")
	@classmethod
	def str(cls, status):
		""" Get string representation of the passed status """
		try:
			status_str = cls.__statusstr[status+1]
		except (IndexError, TypeError):
			return "UNKNOWN"
		
		return status_str

class BusStopFinder():
	""" BusStopFinder class to solve the gis-code-challenge """
	
	# Aggressivity Level to use to detect bus stops
	_level = Levels.NORMAL
	_status = Status.NONE
	_logmsg = None
	
	# Mapping  "Aggressivity" level to Geom Buffering configuration
	_level_buffer_mapping = {
												Levels.CAUTIOUS: 0.001,		#	100 meters buffer
												Levels.NORMAL: 0.002,			#	200 meters buffer
												Levels.AGGRESSIVE: 0.005	#	500 meters buffer
											}
	
	# Mapping  "Aggressivity" level to clustering options (epsilon, min_samples)
	_kms_per_radian = 6371.0088
	_level_clustering_opts_mapping = {
															Levels.CAUTIOUS: 	(0.5/_kms_per_radian, 3),		#	500 meters and min 3 point
															Levels.NORMAL: 		( 0.3/_kms_per_radian, 1),	#	300 meters and min 1 point
															Levels.AGGRESSIVE: ( 0.1/_kms_per_radian, 1)		#	100 meters and min 1 point
														}

	# List of filters to be applied to derive bus stops
	__filters_list = []
	# Point data from which derive bus stops
	__points_data = None
	
	def __init__(self, geoJson_points, geoJson_routes=None, level=Levels.NORMAL):
		""" geoJson_points:	loaded geojson (pydict) containing the activity points
			 geoJson_routes:	(optional) loaded geojson (pydict) containing routes to better filter the points
			 level:					(optional) Aggressivity level of the detection. (See Levels class docs)
		"""
		
		# Check geoJson_points validity
		try:
			self.__points_data = geoJson_points["features"]
		except (TypeError, KeyError):
			raise ValueError('Input geoJson_points is not valid')
		
		# Check geoJson_routes validity
		if geoJson_routes:
			try:
				geoJson_routes["features"]
			except (TypeError, KeyError):
				raise ValueError('Input geoJson_routes is not valid')
		
		self.__level = level if ( (level is not None) and (level >= Levels.CAUTIOUS and level <= Levels.CAUTIOUS) ) else Levels.NORMAL
		
		self.__filters_list.append( _ActivityFeaturesFilter( level=self.__level ) )
		self.__filters_list.append( Features2GeomFilter() )

		if geoJson_routes:
			# Convert the routes geojson to geometry
			routes_geom = Features2GeomFilter().filter( geoJson_routes["features"] )
			# Choose buffer distance according to the aggressivity level parameter
			buffer_dist = self._level_buffer_mapping[ self._level ]
			# Buffer the routes 
			self.__filters_list.append( IntersectGeomFilter( routes_geom, buffer_filter=BufferGeomFilter( buffer_dist ) ) )
		
		
		# Choose clustering options according to the aggressivity level parameter
		kmseps, min = self._level_clustering_opts_mapping[ self.__level ]
		self.__filters_list.append( ClusteringGeomFilter( kmseps, min ) )
		self.__filters_list.append( Geom2GeoJsonFilter() )
			
	def getStatus(self):
		""" Retrieve the current status of the processing """
		return self._status
	
	def getLogMessage(self):
		""" Retrieve the last log message from the processing """
		return self._logmsg
	
	def getCurrentPoints(self):
		""" Retrieve current (filtered or not) points """
		return self.__points_data
		
	def find(self):
		""" Method to start the processing on the input data passed to the constructor, returning found bus stops in a geoJson ready format """
		self.__status = Status.RUNNING
		for filter in self.__filters_list:
			
			# If previous filter returned None, some errors occurred
			if self.__points_data is None:
				self._logmsg = "Error while applying %s filter" % filter.__class__.__name__
				self._status = Status.ERROR
				return None
			
			# If already no points, apply the last filter to obtain the output in the expected format
			if len( self.__points_data ) == 0:
				return {}
			
			self._logmsg = "Processing %d points using %s" %( len(self.__points_data), filter.__class__.__name__)
			self.__points_data = filter.filter( self.__points_data)

		self._status = "Process completed with a final output of %d points" %( len(self.__points_data))
		self._status = Status.COMPLETED
		return self.__points_data