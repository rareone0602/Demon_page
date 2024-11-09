window.HELP_IMPROVE_VIDEOJS = false;

$(document).ready(function() {
  // Options for Bulma Carousel
  var carouselOptions = {
    slidesToScroll: 1,
    slidesToShow: 1,
    loop: true,
    infinite: true,
    autoplay: true,
    autoplaySpeed: 5000,
  };

  // Initialize all carousels
  var carousels = bulmaCarousel.attach('.carousel', carouselOptions);

  // Initialize Bulma Slider
  bulmaSlider.attach();
});
