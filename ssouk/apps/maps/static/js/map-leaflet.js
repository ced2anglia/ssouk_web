
SSOUK.namespace('SSOUK.map_handler');

SSOUK.map_handler = function() {
    
    init = function() {
        var y =  52.20005469158063,
            x = 0.12249999999994543,
            zoom = 13;
        var markers = {};
            
        var map = new L.Map('map_canvas');
        var mapquestUrl = 'http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
        subDomains = ['otile1','otile2','otile3','otile4'],
        mapquestAttrib = 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" \ target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.';
                
        var mapquest = new L.TileLayer(mapquestUrl, {maxZoom: 18, attribution: mapquestAttrib, subdomains: subDomains});
        
        map.addLayer(mapquest).setView(new L.LatLng(y, x), zoom);
        
        map.on('dragend', SSOUK.map_handler.updateDisplay);
        map.on('zoomend', SSOUK.map_handler.updateDisplay);
        
        SSOUK.map_handler.map = map;
        SSOUK.map_handler.markers = markers;
   }
   
    updateMarker = function(lat, lng, popup_text, pk) {
        
        var marker = new L.Marker(new L.LatLng(lat, lng));
        marker.bindPopup(popup_text);
        map = SSOUK.map_handler.map;
        map.addLayer(marker);
        SSOUK.map_handler.markers[pk] = marker;
        
    }

   updateDisplay =  function(e) {
        
        bounds = SSOUK.map_handler.map.getBounds();
        var sw = bounds.getSouthWest();
        var ne = bounds.getNorthEast();
        
        // get the items from django
        // and update the items 
        $.get("/inventory/get_items_within_map", {
            'sw_y' : sw.lat,
            'sw_x' : sw.lng,
            'ne_y' : ne.lat,
            'ne_x' : ne.lng
        }, function (html_response) {
            $('#inventory-list').replaceWith(html_response);
        });
   }
   
   
   return {
        init : init,
        updateDisplay : updateDisplay,
        updateMarker : updateMarker, 
   }
}();
 