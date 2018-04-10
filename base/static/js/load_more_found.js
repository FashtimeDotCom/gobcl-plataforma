/* global $, document */

$(function() {

  function isMobileDevice() {

    // Data from bootstrap mobile devices
    if (screen.width <= 991) {
      return true;
    }

    return false;
  }

  if (!isMobileDevice()) {
    return;
  }

  var limit = parseInt(App.infiniteScroll.offset, 25)

  GobCl.createInifiniteScroll(

    // a link for ajax request
    '/api/1.0/search' + '?offset=' + limit,
    // a function that adds information about category and query string to a requestUrl
    function(url) {

      var currentLocation = window.location.href;
      var qMatch = currentLocation.match(/q=([^&]+)/);
      var result = url;
      if (qMatch !== null) {
        result += ('&q=' + qMatch[1]);
      }

      var categoryMatch = currentLocation.match(/category_slug=([a-z-]+)/);
      if (categoryMatch !== null) {
        result += ('&category_slug=' + categoryMatch[1]);
      }

      return result;
    },

    // a pug template which will be used to render results from server
    'search/list',

    // a selector to an existing container
    '.row-results',

    // postLoadingTransformation
    function() {
      // Changing the displayed number of total results
      // var $searchResultCounts = $('.search-results-counts');
      // var headerText = $searchResultCounts.text().replace(/\d+/, $('.result').length);
      // $searchResultCounts.text(headerText);
    }
  )();
});
