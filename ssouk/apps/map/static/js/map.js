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
  var searchArea = {
    points: new google.maps.MVCArray(),
    markers: [],
    poly: null
  };
  var baseAddrId, baseMarker;
  var geocoder = new google.maps.Geocoder();
  var directionsDisplay = new google.maps.DirectionsRenderer();
  var directionsService = new google.maps.DirectionsService();
  var infowindow = new google.maps.InfoWindow();

  /*
    alias google.maps.Polygon.prototype.containsLatLng to
    google.maps.Polygon.prototype.contains:
    like this we can use it as a google.maps.LatLngBounds-like object
    in updateDisplay()
  */
  google.maps.Polygon.prototype.contains = google.maps.Polygon.prototype.containsLatLng;

  $('#postCodeSubmit').click(function() { 
    var pc = $('#postCodeBox').val();
    if (pc) {
      geocodeAddress('Cambridge ' + pc);
    }
  });

  $('#geolocateButton').click(function() {  
    geolocate();
  });

  $('#clearDirections').click(function() {  
    directionsDisplay.setMap(null);
    infowindow.close();
  });

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

  $('#xhr_get').mouseover(function() {
      
      $.get("/map/xhr_test", {
        message: 'Hi from JS',
        },
        function(data) {
          var message = data['message']
          
          alert(message);
        $('#xhr_result').replaceWith(message)
        });
  });

  /*
    bounds object needs to expose a 'contains' method that takes latLng as arg
    excludes is an object holding addrIds which not to update; the default is to
    exclude the base marker if any is active
  */
  function updateDisplay(bounds) {
    // var message = bounds + " SW " + bounds.getSouthWest() + " NE " + 
                  // bounds.getNorthEast();
    // alert(message);
    // s, w, n, e = bounds
    
    sw = bounds.getSouthWest()
    ne = bounds.getNorthEast()
    
    //get the items from django
    $.get("/map/get_markers_on_map", {
       's' : sw.lat(),
       'w' : sw.lng(),
       'n' : ne.lat(),
       'e' : ne.lng() 
    }, 
        function (items) {
              // getting the list out in JS world
              
              if (items.length != 0) {
                // building the list
                var inventory_list = []
                
                $.each(items, function(idx, item) {
                    var html_item = '<li id=' + item.pk + '><a href=' + 
                        item.fields.user + '/' + item.pk + '>' + 
                        item.fields.name + '</a></li>'; 
                    inventory_list.push(html_item);
                  
                });
                var new_html = '<div id="inventory-list"><ul>' + inventory_list + 
                                '</ul><div>';
                
                $('#inventory-list').replaceWith(new_html);
                
              } else {
                alert('items empty!!!')
                $('#inventory-list').replaceWith("<p>No Items available at these latitude</p>");
              }
      }, 'json');
    
       
 
    // $.each(items , function() {
        // items.push('<li id="' + key + '">' + val + '</li>');
      // });
// 
      // $('<ul/>', {
        // 'class': 'my-new-list',
        // html: items.join('')
      // }).appendTo('body');
    // });
//   
// 
    // $.each(users, function(uIdx, user) {
      // $.each(user.addresses, function(aIdx, addr) {
        // var addrId = uIdx.toString() + '.' + aIdx.toString();
        // var addrLoc = new google.maps.LatLng(addr.lat, addr.lng);
        // /*
          // if user location is contained in search polygon and is not currently
          // being displayed, then add marker to register
        // */
        // if (bounds && bounds.contains(addrLoc)) {
          // if (!addrIdToMarker.hasOwnProperty(addrId) && !excludes.hasOwnProperty(addrId)) {
            // var m = new google.maps.Marker({
              // map: map,
              // position: addrLoc,
              // icon: markerIcons.friend,
              // title: users[uIdx].name + ' ' + users[uIdx].addresses[aIdx].tag
            // });
            // google.maps.event.addListener(m, 'click', function() {
              // if(baseMarker) {
                // directionsDisplay.setMap(map);
                // destPos = m.getPosition();
                // var req = {
                  // origin: baseMarker.getPosition(),
                  // destination: destPos,
                  // travelMode: google.maps.TravelMode.WALKING
                // };
                // directionsService.route(req, function(result, status) {
                  // if (status == google.maps.DirectionsStatus.OK) {
                    // directionsDisplay.setDirections(result);
                    // var route = result.routes[0];
                    // var infoContent = '<div style="float: left;"><center><img src="img/walk.png"></center></div>'
                    // infoContent += '<b>distance: ' + route.legs[0].distance.text + '</b><br>';
                    // infoContent += '<b>duration: ' + route.legs[0].duration.text + '</b>';
                    // infowindow.setContent(infoContent);
                    // infowindow.setPosition(destPos);
                    // infowindow.open(map); 
                  // }
                // });
              // }
            // });
            // addrIdToMarker[addrId] = m;
          // }
        // /*
          // if user location is not contained in search bound, but is being displayed,
          // remove it from marker register
        // */
        // } else if (addrIdToMarker.hasOwnProperty(addrId)) {
          // addrIdToMarker[addrId].setMap(null);
          // delete addrIdToMarker[addrId];
        // }
      // });
    // });
  }

  // function updateBaseMarker() {
    // var uIdx = parseInt($('#userSelect option:selected').val());
    // var aIdx = parseInt($('#addrSelect option:selected').val());
// 
    // if (uIdx === -1 || aIdx === -1) {
      // if (baseMarker) {
        // baseAddrId = null;
        // baseMarker.setMap(null);
        // baseMarker = null;
      // }
    // } else {
      // var addr = users[uIdx].addresses[aIdx];
      // baseAddrId = uIdx.toString() + '.' + aIdx.toString();
      // if (addrIdToMarker.hasOwnProperty(baseAddrId)) {
        // addrIdToMarker[baseAddrId].setMap(null);
        // delete addrIdToMarker[baseAddrId];
      // }
      // if (baseMarker) {
        // baseMarker.setMap(null);
      // }
      // baseMarker = new google.maps.Marker({
        // map: map,
        // position: new google.maps.LatLng(addr.lat, addr.lng),
        // icon: markerIcons.base
      // });
      // map.setCenter(baseMarker.getPosition());
    // }
  // }

  function geolocate() {
    try {
      if(typeof(navigator.geolocation) == 'undefined'){
        gl = google.gears.factory.create('beta.geolocation');
      } else {
        gl = navigator.geolocation;
      }
    } catch(e) {}    

    if (gl) {
      gl.getCurrentPosition(function(pos) {
        var curLoc = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
        map.setCenter(curLoc);
        updateDisplay(map.getBounds());
      }, function() {
        alert("Geolocation failed.");
      });
    } else {
      alert("Your Browser does not support geolocation.");
    }
  }

  function geocodeAddress(addr) {
    geocoder.geocode({'address': addr}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        var loc = results[0].geometry.location;
        map.setCenter(loc);
        updateDisplay(map.getBounds());
      } else {
        alert("Geocoding failed: " + status);
      }
    });
  }

  var polyAddListener = null;
  $('#drawPoly').click(function() {
    if (polyAddListener) {
      clearPoly();
    }
    polyAddListener = google.maps.event.addListener(map, 'click', function(e) {
      polyAdd(e.latLng);
    });
    map.setOptions({draggableCursor: 'crosshair'});
  });

  $('#clearPoly').click(function() {
    clearPoly();   
  });

  function polyAdd(pos) {
    var numPoints = searchArea.points.push(pos);
    var m = new google.maps.Marker({
      map: map,
      position: pos,
      draggable: true,
      raiseOnDrag: false,
      title: 'Drag to change search area',
      animation: google.maps.Animation.DROP,
      icon: numPoints === 1 ? markerIcons.polyFirst : markerIcons.polyOther
    });   
    google.maps.event.addListener(m, 'drag', function(e) {
      searchArea.points.setAt(numPoints-1, e.latLng);
    });
    google.maps.event.addListener(m, 'dragend', function(e) {
      if (searchArea.points.length > 2) {
        updateDisplay(searchArea.poly);
      }
    });
    // if the first point gets clicked again, destroy listener to add additional nodes
    if (numPoints === 1) {
      google.maps.event.addListener(m, 'click', function(e) {
        google.maps.event.removeListener(polyAddListener);
        polyAddListener = null;
        $.each(searchArea.markers, function(mIdx, m) {
          m.setIcon(markerIcons.polyLocked);
        });
        map.setOptions({draggableCursor: 'default'});
      });
    }
    searchArea.markers.push(m);
    if (numPoints > 2) {
      if (!searchArea.poly) {
        searchArea.poly = new google.maps.Polygon({
          clickable: false,
          map: map,
          fillOpacity: 0.08,
          strokeOpacity: 0.12,
          paths: searchArea.points
        });      
      }
      updateDisplay(searchArea.poly);
    }
  }

  function clearPoly() {
    if (searchArea.poly) {
      var numPoints = searchArea.points.getLength();
      for (var i=0; i<numPoints; i++) {      
         searchArea.points.pop();
      }
      while (searchArea.markers.length > 0) {
        var m = searchArea.markers.pop();
        m.setMap(null); 
      }
      if (searchArea.poly) {
        searchArea.poly.setMap(null);
        searchArea.poly = null;
      }
      if (polyAddListener) {
        google.maps.event.removeListener(polyAddListener);
        polyAddListener = null;
      }
      map.setOptions({draggableCursor: 'default'});
      updateDisplay(searchArea.poly);
    }
  }
});
