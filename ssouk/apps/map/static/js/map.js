//map.js Used for all the function relative to the map

SSOUK.namespace('SSOUK.map_handler');

SSOUK.map_handler = function() {

    // private vars
    var site_media_static_url = '/site_media/static/'; //defined in settings.py
    var markerIcons = {
        base: 'http://google-maps-icons.googlecode.com/files/home.png',
    };
    var map = undefined;
        
    // initialiazation 
    init = function() {
        var self = this;
        if (map === undefined) {
            var cambridge = new google.maps.LatLng(52.208056, 0.1225);
            var mapDefaultOpts = {
                center: cambridge,
                zoom: 15,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                draggableCursor: 'default'
            };
            var mapDiv = document.getElementById('map_canvas');
            map = new google.maps.Map(mapDiv, mapDefaultOpts);
            
            // listeners
            google.maps.event.addListener(map, 'dragend', function() {
                SSOUK.map_handler.updateDisplay(map.getBounds());
            });
            google.maps.event.addListener(map, 'zoom_changed', function() {
                SSOUK.map_handler.updateDisplay(map.getBounds());
            });
            
            // synch the map with the db
            self.updateDisplay(map.getBounds());
        }
    }
    
    var updateDisplay = function(bounds) {
        sw = bounds.getSouthWest();
        ne = bounds.getNorthEast();
        
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
    
    var updateMarker = function(lat, lng) {
        baseMarker = new google.maps.Marker({
            map: map,
            position: new google.maps.LatLng(lat, lng),
            icon: markerIcons.base
        });
    }
    
    // public methods
    return {
        init : init,
        updateDisplay : updateDisplay,
        updateMarker : updateMarker
    }
}();