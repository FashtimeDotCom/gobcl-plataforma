
$(function () {
  $('#search')
    .find('.search-form_input').on('input', function () {
      const value = this.value;
      $('.filterable').each(function (index, element) {
        const $element = $(element);
        $element.removeClass('d-none');

        if ($element.data('value').search(new RegExp(value, 'gi')) === -1) {
          $element.addClass('d-none');
        }
      })
    })
    .end()
    .find('.search-form_button--cancel').on('click', function () {
      console.log('aca');
      $('.filterable').each(function (index, element) {
        $(element).removeClass('d-none');
      });
    });
});