$(document).bind('pageshow', function(e) {
  $('#'+e.target.id).trigger('create');
  if(e.target.id == 'page-routes'){
  }
});
$(document).bind('pageinit', function() {
  function makemap(locs, lat, lon, w, h) {
    var str = '';
    for(var l in locs) {
      str += "&markers=color:" + locs[l].color + "%7Clabel:" + locs[l].letter + "%7C" + locs[l].lat + "," + locs[l].lon;
    }
    return "http://maps.googleapis.com/maps/api/staticmap?sensor=false&center=" + lat + "," + lon + "&zoom=10&size=" + w + "x" + h + "&maptype=roadmap" + str;
  }

  //This function is called when scripts/helper/util.js is loaded.
  //If util.js calls define(), then this function is not fired until
  //util's dependencies have loaded, and the util argument will hold
  //the module value for "helper/util".
  function d2h(d) {
    return d > 9 ? d.toString(16) : '0' + d.toString(16);
  }

  function rndColor() {
    var col1 = [Math.min(Math.round(Math.random() * 255) + 50, 255), Math.min(Math.round(Math.random() * 255) + 50, 255), Math.min(Math.round(Math.random() * 255) + 50, 255)];
    col1 = d2h(col1[0]) + '' + d2h(col1[1]) + '' + d2h(col1[2]);
    return col1;
  }

  function showMap(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    var w = Math.round($(window).width() * 0.9);
    var h = $(window).height();
    $.ajax({
      method: "GET",
      url: 'get',
      cache: false,
      dataType: "json",
      data: {
        lat: lat,
        lon: lon
      },
      success: function(data) {

        var view = {
          stops: []
        };
        var locs = [];
        for(var d in data.stops) {
          var colors = rndColor();
          var stop = data.stops[d];
          stop.letter = String.fromCharCode(65 + Number(d));
          stop.color_fg = "#" + colors;
          stop.color_bg = "#000000";
          locs.push({
            lat: stop.lat,
            lon: stop.lon,
            color: "0x" + colors,
            letter: String.fromCharCode(65 + Number(d))
          });
          var new_routes = [];
          for(var r in stop.routes){
            var new_route = {};
            new_route = stop.routes[r]
            stop.routes[r].json = JSON.stringify(stop);
            stop.routes[r].json = JSON.stringify(stop);
          }
          view.stops.push(stop);
        }
        view.map = makemap(locs, lat, lon, w, h);
        $('#page-stops .app').html($.mustache("stops", view)).trigger('create');


        $('#page-stops .app li').click(function() {
          var json = JSON.parse($(this).attr('data-json'));
          $('#page-routes .app').html($.mustache("times", json));
          $.mobile.changePage( "#page-routes", { transition: "slide"} );
        });
      },
      error: function() {
        console.log("ERROR");
        console.log(arguments);
      }
    });

    // var location = {lat: position.coords.latitude, lon:position.coords.longitude};
    // console.log(location);
  }

  // One-shot position request.
  navigator.geolocation.getCurrentPosition(showMap);
});