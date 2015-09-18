'use strict';

$(function () {
  // Initialize Bootstrap Tooltips
  $('[data-toggle="tooltip"]').tooltip();

  // Initialize Select2
  $('select').select2();

  // Auto-Close Success Alerts
  $(".alert-success").delay(4000).slideUp(500, function(){
    $(this).alert('close');
  });
});
