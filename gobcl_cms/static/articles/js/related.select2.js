$(function() {
    $('select#id_related').select2({
      width: '100%',
      ajax: {
        url: '/api/1.0/articles/',
        dataType: 'json',
        delay: 250,
        cache: true,
  
        processResults: function(data) {
          var i;
          var article;
          var results = [];
          var text;
          var currentLanguage = data['current_language'];

          for (i = 0; i < data.results.length; i += 1) {
            article = data.results[i];

            if(currentLanguage == 'en' && article.translations.en != null){
                text = article.translations.en.title
            } else {
                text = article.translations.es.title
            }

            results.push({
              id: article.id,
              text: text
            });
          }
  
          return {
            results: results
          };
        }
      }
    });
  
  });