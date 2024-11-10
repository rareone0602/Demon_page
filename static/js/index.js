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


$(document).ready(function() {
  // Existing code...

  // Initialize selected images array
  let selectedIndices = [];

  // Event handler for image clicks
  $('.selectable-image').on('click', function() {
    const $img = $(this);
    const index = parseInt($img.data('index'));

    // Toggle 'selected' class
    $img.toggleClass('selected');

    // Update selected indices
    if ($img.hasClass('selected')) {
      // Add index to selectedIndices
      selectedIndices.push(index);
    } else {
      // Remove index from selectedIndices
      selectedIndices = selectedIndices.filter(i => i !== index);
    }

    // Update the result image
    updateResultImage(selectedIndices);
  });

  function updateResultImage(selectedIndices) {
    // Compute the target image index based on selected images
    let targetIndex = 0;
    selectedIndices.forEach(i => {
      targetIndex += Math.pow(2, i);
    });

    // Build the image filename
    const resultImageSrc = `static/images/html_demo/${targetIndex}.jpg`;

    // Update the result image
    $('#result-image').attr('src', resultImageSrc);
  }
});
