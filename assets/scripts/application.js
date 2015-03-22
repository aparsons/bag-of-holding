$(function () {
  $(".alert-success").delay(4000).slideUp(500, function(){
    $(this).alert('close');
  });

  $('[data-toggle="tooltip"]').tooltip();

  $(".threadfix-test").click(function(event) {
    var $this = $(this);
    $this.hide()
    $this.parent().append('<span class="fa fa-spinner fa-pulse"></span>');
  });
})
