$(document).ready(main);

function main () {
  var $bpmValue = $('.bpm-value');
  var $bpmSlider = $('.bpm-slider');

  $bpmSlider.slider({
    min: 60,
    max: 240,
    value: 120,
    slide: function (event, ui) {
      $bpmValue.text(ui.value);
      put('/bpm/', {bpm: ui.value});
    }
  });
}

function put (path, data) {
  $.ajax({
    url: path,
    data: data,
    method: 'PUT'
  });
}
