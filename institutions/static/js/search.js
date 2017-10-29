/**
 * Search field for institutions list.
 *
 * Search over data-value attribute in tags with class .filterable and hide
 * elements * w/o match.
 */
$(function() {

  String.prototype.removeAccents = function() {
     return this
           .replace(/[áàãâä]/gi, 'a')
           .replace(/[éè¨ê]/gi, 'e')
           .replace(/[íìïî]/gi, 'i')
           .replace(/[óòöôõ]/gi, 'o')
           .replace(/[úùüû]/gi, 'u')
           .replace(/[ç]/gi, 'c')
           .replace(/[ñ]/gi, 'n')
           .replace(/[^a-zA-Z0-9]/g, ' ');
  };

  $('#search')
    .find('.search-form_input').on('input', function() {
      const value = this.value.removeAccents();
      $('.filterable').each(function(
          index, element) {
        const $element = $(element);
        $element.removeClass('d-none');

        if ($element.data('value').search(new RegExp(value, 'gi')) === -1) {
          $element.addClass('d-none');
        }
      });
    })
    .end()
    .find('.search-form_button--cancel').on('click', function() {
      $('.filterable').each(function(index, element) {
        $(element).removeClass('d-none');
      });
    });

    $('.filterable').each(function() {
      $(this).data('value', $(this).data('value').removeAccents());
    });
});
