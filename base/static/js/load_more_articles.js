/* globals $, document */

$(function () {
  if (App.infiniteScroll === undefined) {
    return;
  } else {
    GobCl.createInifiniteScroll(
      // a link for ajax request
      App.infiniteScroll.url + '?offset=' + parseInt(App.infiniteScroll.offset, 10),
      // a function that adds information about category to a requestUrl
      function (url) {
        var currentLocation = window.location.href;
        var match = currentLocation.match(/category\/([a-z-]+)\//);
        var result = url;
        if (match !== null) {
          result += ('&category_slug=' + match[1]);
        }
        return result;
      },
      // a pug template which will be used to render results from server
      'articles/article_miniature_list',
      // a selector to an existing container
      '.article-miniature-list',
      // postLoadingTransformation
      function () {
        // Setting default images
        $('img.default-image').each(function () {
          $(this).attr('src', $('.article-miniature-list').
            data('default-image-url'));
        });
      }
    )();
  }
});
