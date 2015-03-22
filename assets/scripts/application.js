$(function () {
  $(".alert-success").delay(4000).slideUp(500, function(){
    $(this).alert('close');
  });

  $('[data-toggle="tooltip"]').tooltip();

  $(".threadfix-process").click(function(event) {
    var $this = $(this);
    $this.hide()
    $this.parent().append('<span class="fa fa-spinner fa-pulse"></span>');
  });

  $(window).on('unload', function() {
    $(".fa-spinner").hide(function() {
      $(".threadfix-process").show();
    });
  });
})
