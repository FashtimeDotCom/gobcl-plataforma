$(function () {
  var url = '/api/1.0/articles/?limit=12&offset=12';
  var isAlreadySent = false;
  $('.loading-indicator').hide();

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
      $('.loading-indicator').show();

      currentRequest = $.ajax(url, {
        success: function(response){
          url = response.next;
          var articles = response.results.map(article => {
            return Object.assign({}, article, {
              publishing_date:  moment(article.publishing_date).format('LL')
            });
          });
          var newContent = templates['articles/article_miniature_list'](articles);
          $('.article-miniature-list').append(newContent);
          isAlreadySent = false;
          $('.loading-indicator').hide();

          //Setting default images
          $('img.default-image').each(function() {
            $(this).attr('src', $('.article-miniature-list').data('default-image-url'));
          })
        }
      })
    }
  });
});
