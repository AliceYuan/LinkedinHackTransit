$(document).bind('pageshow', function(e) {
  $('#'+e.target.id).trigger('create');
  if(e.target.id == 'page-routes'){
    console.log(arguments);
    console.log("routes page loaded");
  }
});

$(document).on( "mobileinit", function() {
    $.mobile.defaultPageTransition = "slide";
});

// $( document ).on( "pageinit", "[data-role='page']", function() {
        // $.mobile.loadPage( "test.html" );
        // $( document ).on( "swipeleft", page, function() {
        //     $.mobile.changePage("test.html" );
        // });



//     // var page = "#" + $( this ).attr( "id" ),
//     //     // Get the filename of the next page that we stored in the data-next attribute
//     //     next = $( this ).jqmData( "next" ),
//     //     // Get the filename of the previous page that we stored in the data-prev attribute
//     //     prev = $( this ).jqmData( "prev" );
//     // // Check if we did set the data-next attribute
//     // if ( next ) {
//     //     // Prefetch the next page
//     //     $.mobile.loadPage( next + ".html" );
//     //     // Navigate to next page on swipe left
//     //     $( document ).on( "swipeleft", page, function() {
//     //         $.mobile.changePage( next + ".html" );
//     //     });
//     //     // Navigate to next page when the "next" button is clicked
//     //     $( ".control .next", page ).on( "click", function() {
//     //         $.mobile.changePage( next + ".html" );
//     //     });
//     // }
//     // // Disable the "next" button if there is no next page
//     // else {
//     //     $( ".control .next", page ).addClass( "ui-disabled" );
//     // }
//     // // The same for the previous page (we set data-dom-cache="true" so there is no need to prefetch)
//     // if ( prev ) {
//     //     $( document ).on( "swiperight", page, function() {
//     //         $.mobile.changePage( prev + ".html", { reverse: true } );
//     //     });
//     //     $( ".control .prev", page ).on( "click", function() {
//     //         $.mobile.changePage( prev + ".html", { reverse: true } );
//     //     });
//     // }
//     // else {
//     //     $( ".control .prev", page ).addClass( "ui-disabled" );
//     // }
// });





$(document).bind('pageinit', "[data-role='page']", function() {
  function makemap(locs, lat, lon, w, h) {
    var str = '';
    for(var l in locs) {
      str += "&markers=color:" + locs[l].color + "%7Clabel:" + locs[l].letter + "%7C" + locs[l].lat + "," + locs[l].lon;
    }
    return "http://maps.googleapis.com/maps/api/staticmap?sensor=false&center=" + lat + "," + lon + "&zoom=14&size=" + w + "x" + h + "&maptype=roadmap" + str;
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


        $('#page-stops .app li.bus').click(function() {
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

          // $.mobile.loadPage( "test.html" );
      var page = "#" + $( this ).attr( "id" ),
          prev = $( this ).jqmData( "prev" ),
          next = $( this ).jqmData( "next" );
          console.log(page);
      if ( next ) {
        // Prefetch the next page
        $.mobile.loadPage( next + ".html" );
        // Navigate to next page on swipe left
        $( document ).on( "swipeleft", page, function() {
            $.mobile.changePage( next + ".html" );
        });
      }
      if ( prev ) {
        console.log(prev);
        $.mobile.loadPage( prev + ".html" );
        $( document ).on( "swiperight", page, function() {
            $.mobile.changePage( prev + ".html", { reverse: true } );
        });
      }


});