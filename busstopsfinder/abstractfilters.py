from abc import ABCMeta, abstractmethod

class AbstractFilter():
	""" Abstract Class modelling a generic filter """
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def filter(self, data):
		pass

class AbstractGeometriesFilter(AbstractFilter):
	""" Abstract Class modelling a geometry filter, operating on shapes """
	__metaclass__ = ABCMeta

class AbstractFeaturesFilter(AbstractFilter):
	""" Abstract Class modelling a features filter, based on its properties """
	__metaclass__ = ABCMeta

class AbstractConverterFilter(AbstractFilter):
	""" Abstract Class modelling a converter filter, transforming from/to different formats """
	__metaclass__ = ABCMeta
