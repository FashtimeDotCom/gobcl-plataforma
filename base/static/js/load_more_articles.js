$(function(){
  createInifiniteScroll(
    document.app.url,
    (url) =>  {
      var currentLocation = window.location.href ;
      var match = currentLocation.match(/category\/([a-z-]+)\//);
      var result = url;
      if (match != null) {
       result += ('&category_slug=' + match[1]);
      }
      return result;
    },
    'articles/article_miniature_list',
    '.article-miniature-list',
    () => {
      //Setting default images
      $('img.default-image').each(function() {
        $(this).attr('src', $('.article-miniature-list').
          data('default-image-url'));
      })
    }
  )();
});
