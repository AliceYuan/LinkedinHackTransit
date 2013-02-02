define(function(){
  function makemap(locs, lat, lon, w, h){
    var str = '';
    for (var l in locs){
      str += "&markers=color:"+locs[l].color+"%7Clabel:"+locs[l].letter+"%7C"+locs[l].lat+","+locs[l].lon;
    }
    return "http://maps.googleapis.com/maps/api/staticmap?sensor=false&center="+
    lat+","+lon+"&zoom=10&size="+w+"x"+h+
    "&maptype=roadmap"+str;
  }

  return {"test": 1, makemap: makemap};
});