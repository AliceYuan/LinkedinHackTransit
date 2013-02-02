require(["helper/util"], function(util) {
    //This function is called when scripts/helper/util.js is loaded.
    //If util.js calls define(), then this function is not fired until
    //util's dependencies have loaded, and the util argument will hold
    //the module value for "helper/util".
    console.log(util.test);

    function showMap(position) {
      $.get('data.json', {lat: position.coords.latitude, lon:position.coords.longitude }, function(){
        console.log('got data');
      });

      var location = {lat: position.coords.latitude, lon:position.coords.longitude};
      console.log(location);
      $('#app').html($.mustache("hello", location));
    }

    // One-shot position request.
    navigator.geolocation.getCurrentPosition(showMap);
});