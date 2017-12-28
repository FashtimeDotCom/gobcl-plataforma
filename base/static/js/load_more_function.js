function createInifiniteScroll(
  urlTemplate,
  urlTransformation,
  templateName,
  targetSelector,
  postLoadingTransformation
) {

  return function() {

    var url = urlTemplate + '?offset=' + parseInt(document.app.offset);
    var isAlreadySent = false;
    var blockFutureRequests = false;
    $('.loading-indicator').hide();

    document.addEventListener('scroll', function (event) {
      if (isAlreadySent) {
        return;
      }

      var docViewTop = $(window).scrollTop();
      var docViewBottom = docViewTop + $(window).height();

      var elemTop = $('.loading-indicator').parent().offset().top;
      var elemBottom = elemTop + $('.loading-indicator').height();

      var shouldLoadMore = ((elemBottom <= docViewBottom * 0.95 )
        && (elemTop >= docViewTop));

      if(shouldLoadMore && !blockFutureRequests) {
        isAlreadySent = true;
        $('.loading-indicator').show();

        var requestUrl = urlTransformation ? urlTransformation(url) : url;

        $.ajax(requestUrl, {
          success: function(response){
            url = response.next || url;
            var articles = response.results.map(article => {
              return Object.assign({}, article, {
                publishing_date:  moment(article.publishing_date).format('LL')
              });
            });
            var newContent = templates[templateName]({
              articles,
              currentLanguage: response.current_language
            });
            $(targetSelector).append(newContent);
            isAlreadySent = false;
            $('.loading-indicator').hide();

            //post loading transformatiom
            postLoadingTransformation && postLoadingTransformation();

            if (response.results.length === 0) {
              blockFutureRequests = true;
            }
          }
        })
      }
    });
  };
}
