/**
 * Script for submit search on change tag filter.
 */
$(function () {

  $('.tags')
    .on('change.gl.tags', function (value) {
      $('#search').closest('form').submit();
    })
    .on('cancel.gl.tags', function () {
      $('#search').closest('form').submit();
    });

});