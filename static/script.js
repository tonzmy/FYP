var intervals = [];
function getImage(cameraId) {
  var message = {
    'cameraId': cameraId
  };
  $.post('/image', JSON.stringify(message)).done( function(response) {
      if (response == 'error') {
        $('#img').attr('src', "static/black_loading.png");
      }
      else {
       $('#img').attr('src', "data:image/jpeg;base64, " + response.content);
       // tiny yolov2
       $('.tiny-yolov2-bus').text(response.numbers[0].tinyv2_bus);
       $('.tiny-yolov2-car').text(response.numbers[0].tinyv2_car);
       $('.tiny-yolov2-motorbike').text(response.numbers[0].tinyv2_motorbike);
       $('.tiny-yolov2-truck').text(response.numbers[0].tinyv2_truck);
       $('.tiny-yolov2-level').text(response.numbers[0].tinyv2_level);

       // yolov2
       $('.yolov2-bus').text(response.numbers[1].fullv2_bus);
       $('.yolov2-car').text(response.numbers[1].fullv2_car);
       $('.yolov2-motorbike').text(response.numbers[1].fullv2_motorbike);
       $('.yolov2-truck').text(response.numbers[1].fullv2_truck);
       $('.yolov2-level').text(response.numbers[1].fullv2_level);

       //v3
       $('.yolov3-bus').text(response.numbers[2].v3_bus);
       $('.yolov3-car').text(response.numbers[2].v3_car);
       $('.yolov3-motorbike').text(response.numbers[2].v3_motorbike);
       $('.yolov3-truck').text(response.numbers[2].v3_truck);
       $('.yolov3-level').text(response.numbers[2].v3_level);
     }
    }).fail(function() {
      $('#img').attr('src', "static/black_loading.png");
    });
}

$('#name-button').click(function() {
 var mess1 = $('#name-input').val();
 var message = {
   'name': mess1
 };
 $.post('/hello', JSON.stringify(message), function(response) {
   $('#greeting').text(response.greeting);
 });
});


$('.image-button').click(function(event) {
 if (intervals.length != 0) {
   for (val of intervals) {
     window.clearInterval(val);
   }
   intervals = [];
 }
 var cameraId = event.target.value;
 var location = event.target.name;
 $('.location').text('');
 $('.location').text(location);
 $('table td').text('');
 $('table td').text('Loading...');
 $('#img').attr('src', "static/black_loading.png");
  var i = setInterval(function() {getImage(cameraId); }, 10000);
  intervals.push(i);
});
