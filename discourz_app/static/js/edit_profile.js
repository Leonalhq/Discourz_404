$(function() {
  $('[data-toggle="tooltip"]').tooltip();
});

$(function() {
  $('[data-toggle="popover"]').popover();
});

function readURL(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
          $('#myimg').attr('src', e.target.result);
      }

      reader.readAsDataURL(input.files[0]);
  }
}

$(function () { //document ready call
  $("#photoinput").change(function(){
      readURL(this);
  });
});

