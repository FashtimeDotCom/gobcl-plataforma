/**
 * Search field for institutions list.
 *
 * Search over data-value attribute in tags with class .filterable and hide
 * elements * w/o match.
 */
$(function () {

  const accentFold = App.utils.accentFold;

  $('#search')
    .find('.search-form_input').on('input', function () {
      const value = accentFold(this.value);
      $('.filterable').each(function (index, element) {
        const $element = $(element);
        $element.removeClass('d-none');

        if (accentFold($element.data('value')).search(new RegExp(value, 'gi')) === -1) {
          $element.addClass('d-none');
        }
      })
    })
    .end()
    .find('.search-form_button--cancel').on('click', function () {
      $('.filterable').each(function (index, element) {
        $(element).removeClass('d-none');
      });
    });
});