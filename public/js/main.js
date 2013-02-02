require(["helper/util"], function(util) {
    //This function is called when scripts/helper/util.js is loaded.
    //If util.js calls define(), then this function is not fired until
    //util's dependencies have loaded, and the util argument will hold
    //the module value for "helper/util".
    console.log();

    function showMap(position) {
      var lat = position.coords.latitude;
      var lon = position.coords.longitude;
      var w = 300;
      var h = 300;
      $.ajax({
        method: "GET",
        url: 'get',
        cache: false,
        dataType: "json",
        data: {lat: lat, lon:lon },
        success: function(data){
          var view = {stops:[]};
          for(var d in data.stops){
            var stop = data.stops[d];
            stop.map = (function(lat, lon, w, h){
              return function(){
                return util.makemap(lat, lon, w, h);}})(stop.lat, stop.lon, w, h);
            view.stops.push(stop);
          }
          $('#app').html($.mustache("stops", view)).trigger('create');
        },
        error: function(){
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