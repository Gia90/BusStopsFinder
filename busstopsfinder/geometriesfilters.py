from abstractfilters import AbstractGeometriesFilter
from shapely.geometry import MultiPoint
import numpy as np
from sklearn.cluster import DBSCAN

class BufferGeomFilter(AbstractGeometriesFilter):
	"""  BufferGeomFilter dilates or erodes a shapely.geometry """
	_buffer_dist = 0
	
	def __init__(self, buffer_dist):
		""" buffer_dist: int representing the distance to dilate or erode the shapely.geometry """
		self._buffer_dist = buffer_dist
	
	def filter(self, geometry_to_buffer):
		""" Buffers the passed shapely.geometry """		
		try:
			return geometry_to_buffer.buffer( float(self._buffer_dist) )
		except (AttributeError, TypeError, ValueError):
			return None

class IntersectGeomFilter(AbstractGeometriesFilter):
	""" IntersectGeomFilter intersect 2 geometries, returning the intersection as shapely.geometry """
	_geom_to_intersect = None
	_buffer_filter = None
	
	def __init__(self, geom_to_intersect, buffer_filter=None):
		"""  geom_to_intersect:			shapely.geometry to intersect
			  buffer_filter (optional):	BufferGeomFilter to use to buffer the geom_to_intersect
		"""
		self._geom_to_intersect = geom_to_intersect
		self._buffer_filter = buffer_filter
	
	def filter(self, data_to_filter):
		""" Intersect the shapely.geometry "data_to_filter" with the (buffered?) geom passed in the constructor """
		if data_to_filter is None:
			return None
		
		try:
			data_to_filter.geom_type					#	Check if data_to_filter is a shapely.geometry
			
			if self._buffer_filter :
				self._geom_to_intersect = self._buffer_filter.filter(self._geom_to_intersect)
				
			self._geom_to_intersect.geom_type	#	Check if _geom_to_intersect is not None and is a shapely.geometry
		except AttributeError:
			return None
		
		return data_to_filter.intersection(self._geom_to_intersect)


class ClusteringGeomFilter(AbstractGeometriesFilter):
	""" ClusteringGeomFilter clusters a shapely.geometry.MultiPoint or a list of shapely.geometry.Point using DBS clustering and haversine as distance function. Eventually creates a list of representative shapely.geometry.Point for each cluster """
	_epsilon = 0
	_min_samples = 0
	
	def __init__(self, epsilon, min_samples):
		"""  epsilon:				int representing the maximum distance between points in the same cluster
			  min_samples:		int representing the minimum number of Points in a cluster
		"""
		self._epsilon = epsilon
		self._min_samples = min_samples
	
	def filter(self, multipoint_geometry):
		""" Clusterize the points in multipoint_geometry and returns a shapely.geometry.MultiPoint of representative shapely.geometry.Point for each cluster 
				multipoint_geometry:		 shapely.geometry.MultiPoint or list of shapely.geometry.Point
			"""
		try:
			# Create numpy matrix with inverted coordinates of the points in the _bus_stops MultiPoint shape
			points_matrix = np.array( [  point.coords[0][::-1] for point in multipoint_geometry ] )		# geojson standard stores coordinates as (lon, lat), we need (lat, lon)
		except (AttributeError, TypeError):
			return None

		try:
			# Compute the DBS clustering
			db = DBSCAN(eps=self._epsilon, min_samples=self._min_samples, algorithm='ball_tree', metric='haversine').fit( np.radians(points_matrix) )
		except ValueError:
			return None

		labels = db.labels_
		n_clusters = len(set(labels))
		
		# Create list of point cluster
		clustered_points = [ list() for i in range(n_clusters) ]
		for label, point in zip(labels, points_matrix):
			clustered_points[ label ].append( point[::-1] )	# re-invert (lat,lon) into (lon,lat)
		
		# Convert the clustered points list into a list of cluster representative points
		return MultiPoint([ MultiPoint(cluster).representative_point() for cluster in clustered_points ])