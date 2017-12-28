//This function generates a creator of an infinite scroll
//PARAMETERS:
//urlTemplate - a link for ajax request
//urlTransformation - a function that adds additional parameters to a requestUrl (optional), should accept
//    url as parameter and return a new url. Will be used only at first call, after it we just use what server sends us a 'next'
//templateName - a pug template which will be used to render results from server
//targetSelector - a selector to an existing container
//postLoadingTransformation - a function that is caused in the end of the procedure (optional)
function createInifiniteScroll(
  urlTemplate,
  urlTransformation,
  templateName,
  targetSelector,
  postLoadingTransformation
) {

  return function() {

    //adding additional parameter to a request using a function-parameter
    var requestUrl = urlTransformation ? urlTransformation(urlTemplate) : urlTemplate;

    var isAlreadySent = false;
    var blockFutureRequests = false;
    $('.loading-indicator').hide();

    document.addEventListener('scroll', function (event) {
      //This checks prevent additional request while the already sent one is not resolved
      if (isAlreadySent) {
        return;
      }

      //Here we check if a loading indicator is inside our viewport. If it is true
      //We can call a request
      var docViewTop = $(window).scrollTop();
      var docViewBottom = docViewTop + $(window).height();

      var elemTop = $('.loading-indicator').parent().offset().top;
      var elemBottom = elemTop + $('.loading-indicator').height();

      var shouldLoadMore = ((elemBottom <= docViewBottom * 0.95 )
        && (elemTop >= docViewTop));

      if(shouldLoadMore && !blockFutureRequests) {
        isAlreadySent = true;
        $('.loading-indicator').show();

        $.ajax(requestUrl, {
          success: function(response){
            //Setting a link for a consequent request
            requestUrl = response.next || requestUrl;

            //transforming a publishing date to a readable format for all results
            var articles = response.results.map(article => {
              return Object.assign({}, article, {
                publishing_date:  moment(article.publishing_date).format('LL')
              });
            });

            //Generating DOM using a pug-template
            var newContent = templates[templateName]({
              articles,
              currentLanguage: response.current_language
            });

            //Appending it to a current container
            $(targetSelector).append(newContent);
            isAlreadySent = false;
            $('.loading-indicator').hide();

            //post loading transformatiom
            postLoadingTransformation && postLoadingTransformation();

            //If no more articles is loaded we block this function forever
            if (response.results.length === 0) {
              blockFutureRequests = true;
            }
          }
        })
      }
    });
  };
}
