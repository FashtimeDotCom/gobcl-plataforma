$(function () {
  // var url = 'api/1.0/articles/';
  var url = '/api/1.0/articles/?limit=12&offset=12';
  var isAlreadySent = false;
  document.addEventListener('scroll', function (event) {
    if (isAlreadySent) {
      return;
    }
    // Fetch variables
    var scrollTop = $(document).scrollTop();
    var windowHeight = $(window).height();
    var bodyHeight = $(document).height() - windowHeight;
    var scrollPercentage = (scrollTop / bodyHeight);

    // if the scroll is more than 90% from the top, load more content.
    if(scrollPercentage > 0.9) {
      isAlreadySent = true;
      currentRequest = $.ajax(url, {
        success: function(response){
          url = response.next;
          var newContent = templates['articles/article_miniature_list'](response.results);
          $('.article-miniature-list').append(newContent);
          isAlreadySent = false;
        }
      })
    }
  });
});
