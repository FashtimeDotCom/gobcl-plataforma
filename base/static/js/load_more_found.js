$(function(){
  doument.createInifiniteScroll(
    // a link for ajax request
    '/api/1.0/search' + '?offset=' + parseInt(document.app.offset),
    // a function that adds information about category and query string to a requestUrl
    function(url) {
      var currentLocation = window.location.href ;
      var qMatch = currentLocation.match(/q=([^&]+)/);
      var result = url;
      if (qMatch != null) {
       result += ('&q=' + qMatch[1]);
      }

      var categoryMatch = currentLocation.match(/category_slug=([a-z-]+)/);
      if (categoryMatch != null) {
       result += ('&category_slug=' + categoryMatch[1]);
      }

      return result;
    },
    //a pug template which will be used to render results from server
    'search/list',
    // a selector to an existing container
    '.row-results',
    // postLoadingTransformation
    function() {
      //Changing the displayed number of total results
      var headerText = $('.search-results-counts').text().replace(/\d+/, $('.result').length);
      $('.search-results-counts').text(headerText);
    }
  )();
});
