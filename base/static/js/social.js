/**
 * Enable social share for .social class elements.
 *
 * attribute data-social=<social network> required.
 */
$(function () {

  var links = {
    facebook: {
      url: 'https://www.facebook.com/sharer/sharer.php?u={link}',
      settings: 'toolbar=0,status=0,width=626,height=436'
    },
    twitter: {
      url: 'https://twitter.com/intent/tweet/?url={link}&text={text}',
      settings: 'toolbar=0,status=0,width=626,height=436'
    },
    messenger: {
      url: 'fb-messenger://share/?link={link}',
      settings: 'toolbar=0,status=0,width=626,height=436'
    }
  };

  $.extend(App.utils, {
    enableSocialShare: function () {
      $('.share').on('click', function (e) {
        e.preventDefault();
        if ($(this).is('[data-social]')) {
          var social = $(this).data('social');
          var link = links[social];

          if (link) {
            window.open(
              link.url
                .replace('{link}', $(this).prop('href'))
                .replace('{text}', $(this).data('text')),
              social + 'share',
              link.settings
            );
          }
        }
      });
    }
  });
});
