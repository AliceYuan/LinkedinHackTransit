require(["helper/util"], function(util) {
    //This function is called when scripts/helper/util.js is loaded.
    //If util.js calls define(), then this function is not fired until
    //util's dependencies have loaded, and the util argument will hold
    //the module value for "helper/util".
    console.log(util.test);

    function showMap(position) {
      $.ajax({
        method: "GET",
        url: 'get',
        cache: false,
        dataType: "json",
        data: {lat: position.coords.latitude, lon:position.coords.longitude },
        success: function(data){
          $('#app').html($.mustache("stops", data)).trigger('create');
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