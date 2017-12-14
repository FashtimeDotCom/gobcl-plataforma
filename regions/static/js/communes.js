/**
 * Select field for communes.
 *
 * Display info of a commune selected.
 */
$(function () {
  $('#communes')
    .on('select2:select', function () {
      $('.commune').addClass('d-none');
      $('#commune-' + this.value).removeClass('d-none');
    })
    .trigger({ type: 'select2:select' });
});