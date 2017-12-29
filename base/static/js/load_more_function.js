/* global $, document, moment, templates */

/**
 * createInifiniteScroll - This function generates a creator of an infinite scroll
 * @param {string} urlTemplate - a link for ajax request
 * @param {function} urlTransformation -  function that adds additional parameters
 * to a requestUrl (optional), should accept url as parameter and return a new url.
 * Will be used only at first call, after it we just use what server sends us a 'next'
 * @param {string} templateName - a pug template which will be used to render results from server
 * @param {string} targetSelector - a selector to an existing container
 * @param {function} postLoadingTransformation - a function that is caused in the end
 * of the procedure (optional)
 * @returns {function} - a function that creates an infinite scroll
 */
document.createInifiniteScroll = function (
  urlTemplate,
  urlTransformation,
  templateName,
  targetSelector,
  postLoadingTransformation
) {
  return function () {
    // adding additional parameter to a request using a function-parameter
    var requestUrl = urlTransformation ? urlTransformation(urlTemplate) : urlTemplate;

    var isAlreadySent = false;
    var blockFutureRequests = false;
    var $loadingIndicator = $('.loading-indicator');
    $loadingIndicator.hide();

    document.addEventListener('scroll', function () {
      // This checks prevent additional request while the already sent one is not resolved
      if (isAlreadySent) {
        return;
      }

      // Here we check if a loading indicator is inside our viewport. If it is true
      // We can call a request
      var docViewTop = $(window).scrollTop();
      var docViewBottom = docViewTop + $(window).height();

      // we use parent of an indicator because hidden elements do not have a height
      // but their container still has
      var elemTop = $loadingIndicator.parent().offset().top;
      var elemBottom = elemTop + $loadingIndicator.height();

      var shouldLoadMore = ((elemBottom <= docViewBottom - 10 )
        && (elemTop >= docViewTop));

      if (shouldLoadMore && !blockFutureRequests) {
        isAlreadySent = true;
        $loadingIndicator.show();

        $.ajax(requestUrl, {
          success: function (response) {
            // Setting a link for a consequent request
            requestUrl = response.next || requestUrl;

            // transforming a publishing date to a readable format for all results
            var articles = response.results.map(function (article) {
              article.publishing_date =  moment(article.publishing_date).format('LL');
              return article;
            });

            // Generating DOM using a pug-template
            var newContent = templates[templateName]({
              articles: articles,
              currentLanguage: response.current_language
            });

            // Appending it to a current container
            $(targetSelector).append(newContent);
            isAlreadySent = false;
            $loadingIndicator.hide();

            // post loading transformatiom
            postLoadingTransformation && postLoadingTransformation();

            // If no more articles is loaded we block this function forever
            if (response.results.length === 0) {
              blockFutureRequests = true;
            }
          }
        });
      }
    });
  };
};
