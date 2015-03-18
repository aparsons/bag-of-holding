$(function () {
  $(".alert-success").delay(3000).slideUp(400, function(){
    $(this).alert('close');
  });

  $('[data-toggle="tooltip"]').tooltip();
})
