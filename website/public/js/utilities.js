
function gejsonPropsToList(geojsonProps)
{
	var arrayProps = Object.keys(geojsonProps).map(function(k) { console.log(k); return "<li><b>"+k+":</b>"+geojsonProps[k]+"</li>"});
	return "<ul>" + arrayProps.join("\n") + "</ul>"
}