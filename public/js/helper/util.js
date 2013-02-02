define(function(){
  function makemap(lat, lon, w, h){
    return "http://maps.googleapis.com/maps/api/staticmap?sensor=false&center="+
    lat+","+lon+"&zoom=13&size="+w+"x"+h+
    "&maptype=roadmap&markers=color:blue%7Clabel:S%7C"+lat+","+lon;
  }

  return {"test": 1, makemap: makemap};
});