$(function(){
  if (!document.app) {
    document.app = {};
    document.app.offset = 8;
  }

  createInifiniteScroll(
    '/api/1.0/search',
    (url) => {
      var currentLocation = window.location.href ;
      var match = currentLocation.match(/q=([^&]+)/);
      var result = url;
      if (match != null) {
       result += ('&q=' + match[1]);
      }
      return result;
    },
    'search/list',
    '.row-results',
    () => {
      var headerText = $('.heading-medium').text().replace(/\d+/, $('.result').length);
      $('.heading-medium').text(headerText);
    }
  )();
});
