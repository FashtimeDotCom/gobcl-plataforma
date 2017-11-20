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
      gallery: {
        enabled: true
      }
    });
});