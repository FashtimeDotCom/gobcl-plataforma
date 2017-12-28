/**
 * Script for submit search on change tag filter.
 */
$(function () {

  $('.result-search .tags')
    .on('change.gl.tags', function () {
      $('#search').closest('form').submit();
    })
    .on('cancel.gl.tags', function () {
      $('#search').closest('form').submit();
    });

});