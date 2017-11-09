/**
 * Send the A- A+ a11y setting to the server
 */
$(function () {

  $('.toolbar').on('change.gl.toolbar', function (e, value) {
    $.ajax(App.paths.fontSize, {
      data: JSON.stringify({ font_size: value }),
      method: 'POST',
      contentType: 'application/json'
    });
  });

});
