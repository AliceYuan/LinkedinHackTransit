require(["helper/util"], function(util) {
    //This function is called when scripts/helper/util.js is loaded.
    //If util.js calls define(), then this function is not fired until
    //util's dependencies have loaded, and the util argument will hold
    //the module value for "helper/util".
    console.log(util.test);

    function showMap(position) {
      console.log(position);
      // Show a map centered at (position.coords.latitude, position.coords.longitude).
    }

    // One-shot position request.
    navigator.geolocation.getCurrentPosition(showMap);
});