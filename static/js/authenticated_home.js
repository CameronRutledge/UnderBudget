$(document).ready(function(){
  var els = document.getElementsByClassName("hacky");
  for (i = 0; i < els.length; i++) {
    els[i].value = els[i].getAttribute('value');
  }
});
