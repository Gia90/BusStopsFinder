import os, json
from busstopsfinder.core import *
import threading

# Configure input data and options
activity_point_path = "data/activity_points.geojson"
routes_path = "data/routes.geojson"
aggressivity_level = Levels.NORMAL
bus_stop_output = "website/public/data/bus_stops.geojson"


print "Loading activity points from %s ..." % activity_point_path
with open(activity_point_path) as json_file:
	activity_points = json.load(json_file)
print "	Loaded ", len(activity_points["features"]), "points"
print
print "Loading routes from %s ..." % routes_path
with open(routes_path) as json_file:
	routes = json.load(json_file)
print "	Loaded ", len(routes["features"]), "geoms"

print
print "Identifying bus stops using a %s aggressivity level ..." % Levels.str(aggressivity_level)

busstopfinder = BusStopFinder(activity_points, geoJson_routes=routes, level=aggressivity_level)
t = threading.Thread(target=busstopfinder.find)
t.start()

lastLog = None
while( True ):
	status = busstopfinder.getStatus()
	log = busstopfinder.getLogMessage()
	
	if lastLog != log:
		lastLog = log
		print "	", log
	
	if (status == Status.COMPLETED) or (status == Status.ERROR):
		break

print
if status == Status.COMPLETED:
	bus_stops_json = busstopfinder.getCurrentPoints()
	print "Processing completed. Found", len(bus_stops_json["coordinates"]), "bus stops"

	with open(bus_stop_output, "w") as json_file:
		json.dump(bus_stops_json, json_file)

	print "Bus stops exported to %s" % bus_stop_output
else:
	print "Processing ended with error (%s)" % log	 
