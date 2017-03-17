
var map = L.map('mapid').setView([-6.8274, 39.2744], 12);

// BaseLayer OSM
var osmBase = L.tileLayer('http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {attribution: '<a href="http://openstreetmap.org">OpenStreetMap</a>'}).addTo(map);

// Activity Points Layer
var activityPointsStyle = {
    radius: 8,
    fillColor: "#66ff66",
    color: "#333333",
    weight: 2,
    fillOpacity: 0.8,
    opacity: 1,
};
var activityPoints =  new L.GeoJSON.AJAX("data/activity_points.geojson" , {
    pointToLayer: function (feature, latlng) {
		return L.circleMarker(latlng, activityPointsStyle);
	},
	onEachFeature: function (feature, layer) {
		layer.bindPopup('<h2>Activity point</h2>'+gejsonPropsToList(feature.properties));
	}
}).addTo(map);

// Routes layer
var routesStyle = {
    color: "#000000",
    weight: 2,
    opacity: 1,
    fillOpacity: 0.8
};
var routes = new L.GeoJSON.AJAX("data/routes.geojson");

// OSM Bus Stops layer
var osmBusStopsStyle = {
    radius: 8,
    fillColor: "#6666ff",
    color: "#333333",
    weight: 2,
    fillOpacity: 0.8,
    opacity: 1,
};
var osmBusStops =  new L.GeoJSON.AJAX("data/osm_bus_stops.geojson" , {
    pointToLayer: function (feature, latlng) {
		return L.circleMarker(latlng, osmBusStopsStyle);
	},
	onEachFeature: function (feature, layer) {
		layer.bindPopup('<h2>OSM BusStop</h2>'+gejsonPropsToList(feature.properties));
	}
});

// OSM Bus Stations layer
var osmBusStationStyle = {
    radius: 8,
    fillColor: "#ff6666",
    color: "#333333",
    weight: 2,
    opacity: 1,
    fillOpacity: 0.8
};
var osmBusStations = new L.GeoJSON.AJAX("data/osm_bus_stations.geojson" , {
    pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, osmBusStationStyle);
	},
	onEachFeature: function (feature, layer) {
		layer.bindPopup('<h2>OSM BusStation</h2>'+gejsonPropsToList(feature.properties));
	}
});


var myBusStopIcon = L.icon({
    iconUrl: 'style/busstop.png',
    iconSize: [42, 42],
    iconAnchor: [21, 42],
    popupAnchor: [21, 0],
	opacity: 0.7
});

// Identified Bus Stops layer
var myBusStops = new L.GeoJSON.AJAX("data/bus_stops.geojson", {
            pointToLayer: function (feature, latlng) {
                return L.marker(latlng, {icon: myBusStopIcon});
            }
        }).addTo(map);

var baseLayers = {
    "OpenStreetMap": osmBase
};
var overlays = {
	"Detected Bus Stops": myBusStops,
	"Activity Points": activityPoints,
	"Routes": routes,
	"OSM Bus Stations": osmBusStations,
	"OSM Bus Stops": osmBusStops
};
L.control.layers(baseLayers, overlays).addTo(map);
