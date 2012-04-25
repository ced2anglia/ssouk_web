/**
 * @author Michele Mattioni
 */

var MapHandler = Backbone.Model.extend({
    
    defaults: {
        y : 52.20005469158063,
        x : 0.12249999999994543,
        zoom: 13,
        leaflet_map : null,
        items: null,
    },
    
    initialize: function() {
        
        var map = new L.Map('map');
        var mapquestUrl = 'http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
        subDomains = ['otile1','otile2','otile3','otile4'],
        mapquestAttrib = 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" \ target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors.';
        
        var mapquest = new L.TileLayer(mapquestUrl, {maxZoom: 18, attribution: mapquestAttrib, subdomains: subDomains});
        
        // add the CloudMade layer to the map set the view to a given center and zoom
        map.addLayer(mapquest).setView(new L.LatLng(this.get('y'), this.get('x')), this.get('zoom'));
        this.set({ leaflet_map : map});   
    }, 
    
    updateMarker: function(lat, lng) {
        var marker = new L.Marker(new L.LatLng(lat, lng));
        map = this.get("leaflet_map");
        map.addLayer(marker);
    },

   updateDisplay: function(bounds) {
        var sw = bounds.getSouthWest();
        var ne = bounds.getNorthEast();
        
        // get the items from django
        // and update the items 
        $.get("/inventory/get_items_within_map", {
            'sw_y' : sw.lat(),
            'sw_x' : sw.lng(),
            'ne_y' : ne.lat(),
            'ne_x' : ne.lng()
        }, function (html_response) {
            $('#inventory-list').replaceWith(html_response);
        });
   }
});







