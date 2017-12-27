$(function () {
  var url = '/api/1.0/articles/?limit=12&offset=12';
  var isAlreadySent = false;
  $('.loading-indicator').hide();

  document.addEventListener('scroll', function (event) {
    if (isAlreadySent) {
      return;
    }

    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $('.loading-indicator').parent().offset().top;
    var elemBottom = elemTop + $('.loading-indicator').height();

    var shouldLoadMore = ((elemBottom <= docViewBottom * 0.95) && (elemTop >= docViewTop));

    if(shouldLoadMore) {
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
