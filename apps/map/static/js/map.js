$(document).ready(function() {
  var locs = [];
  var markers = [];
  var radius = undefined;
  var map = undefined;
  var cambridge = new google.maps.LatLng(52.208056, 0.1225);
  var home;
  var directionsDisplay = new google.maps.DirectionsRenderer();
  var directionsService = new google.maps.DirectionsService();
  var geocoder = new google.maps.Geocoder();
  
  var browserSupportFlag =  new Boolean();
  // Try W3C Geolocation (Preferred)
  if(navigator.geolocation) {
    browserSupportFlag = true;
    navigator.geolocation.getCurrentPosition(function(position) {
      home = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
      setupMap();
    }, function() {
      handleNoGeolocation(browserSupportFlag);
    });
  // Try Google Gears Geolocation
  } else if (google.gears) {
    browserSupportFlag = true;
    var geo = google.gears.factory.create('beta.geolocation');
    geo.getCurrentPosition(function(position) {
      home = new google.maps.LatLng(position.latitude,position.longitude);
      setupMap();
    }, function() {
      handleNoGeoLocation(browserSupportFlag);
    });
  // Browser doesn't support Geolocation
  } else {
    browserSupportFlag = false;
    handleNoGeolocation(browserSupportFlag);
  }
  
  function handleNoGeolocation(errorFlag) {
    if (errorFlag == true) {
      alert("Geolocation service failed.");
    } else {
      alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
    }
    home = cambridge;
    setupMap();
  }

  var setupMap = function() {
    var mapDiv = document.getElementById('map');
    var mapOptions = {
      center: home,
      zoom: 14,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(mapDiv, mapOptions);
    directionsDisplay.setMap(map);

    markers.push(new google.maps.Marker({
      position: home,
      map: map,
      title: 'Home',
      icon: 'http://gmaps-samples.googlecode.com/svn/trunk/markers/blue/blank.png'
    }));

    radius = new google.maps.Circle({
	  center : home,
	  radius : 0,
	  fillOpacity : 0.1,
	  strokeOpacity : 0.2,
	  map : map,
    });

    var homeLat = home.lat();
    var homeLng = home.lng();

    for(var off1 = 0.01; off1 <= 0.02; off1 += 0.005) {
      for(var off2 = 0.01; off2 <= 0.02; off2 += 0.005) {
        locs.push(new google.maps.LatLng(homeLat-off1, homeLng-off2));
        locs.push(new google.maps.LatLng(homeLat-off1, homeLng));
        locs.push(new google.maps.LatLng(homeLat-off1, homeLng+off2));
        locs.push(new google.maps.LatLng(homeLat, homeLng-off2));
        locs.push(new google.maps.LatLng(homeLat, homeLng+off2));
        locs.push(new google.maps.LatLng(homeLat+off1, homeLng-off2));
        locs.push(new google.maps.LatLng(homeLat+off1, homeLng));
        locs.push(new google.maps.LatLng(homeLat+off1, homeLng+off2));
      }
    }

    $.each(locs, function(idx, loc) {
      var m = new google.maps.Marker({
            position: loc,
            map: map,
            visible: false,
            title: loc.toString()
          })
      markers.push(m);

      google.maps.event.addListener(m, 'click', function() {
        $('#infoArea').html('Hello, I am a marker.<br>My Lat/Lng Position is: ' + m.getPosition().toString());
        var request = {
          origin:markers[0].getPosition(), 
          destination:m.getPosition(),
          travelMode: google.maps.DirectionsTravelMode.WALKING
        };
        directionsService.route(request, function(result, status) {
          if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(result);
            var rev_geocode_address;
            var latLng = m.getPosition();
            geocoder.geocode({'latLng': latLng}, function (results, status) {
              if (status == google.maps.GeocoderStatus.OK) {
                if (results[1]) {
                  rev_geocode_address = results[1].formatted_address;
                  //infowindow.setContent(results[1].formatted_address);
                  //infowindow.open(map, marker);
                  var html = '<br>Reverse Geocoding translates to address: ' + rev_geocode_address
                             + '<br>The distance from the Home marker is ' + result.routes[0].legs[0].distance.text
                             + '<br>Walking will take you approx. ' + result.routes[0].legs[0].duration.text
                  $('#infoArea').append(html);
                }
              } else {
                alert("Geocoder failed due to: " + status);
              }
            });
            
          }
        });
      });
    });
  }
  var showingAll = false;
  showAll =  function() {
    showingAll = showingAll ? false : true;
    $.each(markers.slice(1), function(idx, m) {
      if(showingAll && !m.visible) {
        m.setVisible(true);
      } else if (!showingAll && m.visible) {
        m.setVisible(false);
      }
    });
    radius.setRadius(0);
  };

  showRadius = function() {
    radius.setRadius(+$('#radiusInput').val());
    $.each(markers.slice(1), function(idx, m) {
      if(radius.getBounds().contains(m.getPosition())) {
        m.setVisible(true);
      } else if (m.visible) {
        m.setVisible(false);
      }
    });
  };

  geocodeAddress = function() {
    var newAddress = $('#addressInput').val();
    geocoder.geocode( { 'address': newAddress}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        var m = new google.maps.Marker({
          position: results[0].geometry.location,
          map: map
        });
        markers.push(m);
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
  };
});
