/*
  May 2011 Markus Hsi-Yang Fritz

  - parts adapted from http://demos.geojason.info/google-maps-api-v3-geometry-library.php
  - ray-casting code ("point in polygon") from https://github.com/tparkin/Google-Maps-Point-in-Polygon
*/

$(document).ready(function() {

  var map;
  var cambridge = new google.maps.LatLng(52.208056, 0.1225);
  var mapDefaultOpts = {
    center: cambridge,
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    draggableCursor: 'default'
  };

  var site_media_static_url = '/site_media/static/' //defined in settings.py
  var markerIcons = {
    base: 'http://google-maps-icons.googlecode.com/files/home.png',
    friend: 'http://google-maps-icons.googlecode.com/files/vegetarian.png',
    polyFirst: site_media_static_url + 'img/mapIcons/pin_green_No1_alt2.png',
    polyOther: site_media_static_url + 'img/mapIcons/pin_green.png',
    polyLocked: site_media_static_url + 'img/mapIcons/pin_red.png'
  };
  var infowindow = new google.maps.InfoWindow();

  function initMap(){
    var mapDiv = document.getElementById('map');
    map = new google.maps.Map(mapDiv, mapDefaultOpts);
    google.maps.event.addListener(map, 'dragend', function() {
        updateDisplay(map.getBounds());
    });
    google.maps.event.addListener(map, 'zoom_changed', function() {
        updateDisplay(map.getBounds());
    });
  }
  initMap();


  function updateDisplay(bounds) {
    sw = bounds.getSouthWest()
    ne = bounds.getNorthEast()
    
    //get the items from django
    $.get("/map/get_markers_on_map", {
       'sw_y' : sw.lat(),
       'sw_x' : sw.lng(),
       'ne_y' : ne.lat(),
       'ne_x' : ne.lng() 
    }, 
        function (locations) {
              if (locations.length != 0) {
                // building the list
                var inventory_list = ''
                $.each(locations, function(idx, location) {
                    $.each(location.items, function(idx2, item) {
                      var html_item = '<li id=' + location.pk + '><a href=' + 
                                      item.username + '/' + item.pk + '> ' + 
                                      item.name + '</a> ' + item.username + ' ' + 
                                      item.price + ' ' + item.quantity + '</li>';
                      inventory_list += html_item;
                      updateMarker(location.lat, location.lng)
                    })
                });
                var new_html = '<div id="inventory-list"><ul>' + inventory_list + 
                                '</ul><div>';
                $('#inventory-list').replaceWith(new_html);
              } else {
                var html = '<div id="inventory-list"><p>No Items available at these latitude</p></div>'
                $('#inventory-list').replaceWith(html);
              }
      }, 'json');   
 }

  function updateMarker(lat, lng) {
    baseMarker = new google.maps.Marker({
    map: map,
    position: new google.maps.LatLng(lat, lng),
    icon: markerIcons.base
   });
  }
});
