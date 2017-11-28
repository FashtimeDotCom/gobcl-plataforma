/**
 * Set behavior to the gallery cms plugin.
 */
$(function () {
  $('.gallery')
  // enable carousel of images.
    .slick({
      infinite: true,
      slidesToShow: 3,
      slidesToScroll: 3,
      dots: true,
      arrows: false,
      responsive: [
        {
          breakpoint: 768,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2
          }
        },
        {
          breakpoint: 576,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    })
    // enable popup with gallery for images
    .magnificPopup({
      delegate: '.slick-slide:not(.slick-cloned) .gallery-slide .gallery-image',
      type:'image',
      fixedContentPos: true,
      gallery: {
        enabled: true
      },
      tLoading: '',
      image: {
        titleSrc: 'data-text',
        markup: (
          '<div class="row">'+
            // '<div class="mfp-close"></div>'+
            '<div class="col-md-8">' +
              '<div class="mfp-img"></div>' +
            '</div>' +
            '<div class="col-md-4 align-self-end">' +
              '<div class="mfp-title"></div>' +
            '</div>' +
          '</div>'
        )
      }
    });
});