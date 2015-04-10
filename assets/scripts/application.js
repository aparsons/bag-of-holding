$(function () {
  $(".alert-success").delay(4000).slideUp(500, function(){
    $(this).alert('close');
  });

  $('[data-toggle="tooltip"]').tooltip();

  $('select').select2();

  $(".markdown").markdown({
    iconlibrary: "fa",
    resize: "vertical",
    hiddenButtons: ["cmdCode"],
    reorderButtonGroups: ["groupFont", "groupLink", "groupMisc", "groupCustom", "groupUtil"],
    additionalButtons: [
      [{
        name: "groupCustom",
        data: [{
          name: "codeHighlight",
          title: "Highlight Code",
          icon: { glyph: 'glyphicon glyphicon-asterisk', fa: 'fa fa-code' },
          callback: function(e) {
            // Prepend/Give - surround the selection
            var chunk, cursor, selected = e.getSelection(),content = e.getContent();
            // transform selection and set the cursor into chunked text
            if (selected.length === 0) {
              // Give extra word
              chunk = e.__localize('code here');
              e.replaceSelection('    ' + chunk);
              // Set the cursor
              cursor = selected.start + 4;
            } else {
              if (selected.text.indexOf('\n') < 0) {
                chunk = selected.text;
                e.replaceSelection('    ' + chunk);
                // Set the cursor
                cursor = selected.start + 6;
              } else {
                var list = [];
                list = selected.text.split('\n');
                chunk = list[0];
                $.each(list, function(k, v) {
                  list[k] = '    ' + v;
                });
                e.replaceSelection('' + list.join('\n'));
                // Set the cursor
                cursor = selected.start + 4;
              }
            }
            // Set the cursor
            e.setSelection(cursor, cursor + chunk.length);
          }
        }, {
          name: "toc",
          title: "Table of Contents",
          icon: { glyph: 'glyphicon glyphicon-book', fa: 'fa fa-book' },
          callback: function(e) {
            var selected = e.getSelection();
            e.replaceSelection('\n[TOC]\n');
            e.setSelection(selected.start,selected.start+8);
          }
        }]
      }]
    ],
    footer: '<div class="btn-group" role="group"><a class="btn btn-default btn-xs" href="http://daringfireball.net/projects/markdown/basics" role="button" target="_blank">Markdown Help</a><a class="btn btn-default btn-xs" href="http://pythonhosted.org//Markdown/extensions/code_hilite.html#syntax" role="button" target="_blank">Code Highlighting Help</a></div>'
  });

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

});
