window.HELP_IMPROVE_VIDEOJS = false;

// Define your subdirectories
var subdirs = ["cabin", "cityscape", "desert", "forest", "galaxy", "island", "library", "temple", "underwater", "waterfall"];

// Initialize selected images array per subdir
var selectedIndices = {}; // Key: subdir, Value: array of selected indices

$(document).ready(function() {
  var $container = $('#sections-container');

  // Array to hold all AJAX requests
  var requests = subdirs.map(function(subdir) {
      return $.getJSON(`static/images/html_demo/${subdir}/config.json`);
  });

  // Wait for all AJAX requests to complete
  $.when.apply($, requests).done(function() {
      var categories = [];

      // Handle single and multiple responses
      if (subdirs.length === 1) {
          categories.push(arguments[0]);
      } else {
          for (var i = 0; i < arguments.length; i++) {
              categories.push(arguments[i][0]);
          }
      }

      // Create one section with one title
      var $section = $(`
          <section class="section">
              <div class="hero">
                  <div class="hero-body">
                      <div class="container is-max-desktop">
                          <h2 class="title has-text-centered">
                              Click images to <span style="color:red">select</span>/<span style="color:blue">deselect</span>
                          </h2>
                          <div id="playboxes-container">
                              <!-- Playboxes will be appended here -->
                          </div>
                          <div class="footnotes">
                            <hr>
                            <p> Precomputed results are shown for two methods: 
                              <ol>
                                <li> The ODE baseline </li>
                                <li> Applying one Demon step, using the selected images, followed by ODE steps.</li>
                              </ol> 
                            </p>  
                          </div>
                      </div>
                  </div>
              </div>
          </section>
      `);

      $container.append($section);

      var $playboxesContainer = $section.find('#playboxes-container');

      // Generate playboxes and append to the playboxes container
      categories.forEach(function(data) {
          var $playbox = $(`
              <div class="playbox" data-subdir="${data.subdir}">
                  <p class="has-text-centered">"${data.prompt}", \\( \\beta = ${data.beta} \\), \\( t = ${data.t} \\), \\( t - \\Delta = ${data.t - data.delta} \\)</p>
                  <br>
                  <div class="columns is-centered">
                      <div class="column has-text-centered">
                          <h3 class="subtitle">ODE result of \\( \\mathbf{x}_t \\)</h3>
                          <figure class="image">
                              <img src="static/images/html_demo/${data.subdir}/baseline.jpg" alt="PF-ODE">
                          </figure>
                      </div>
                      <div class="column has-text-centered">
                          <div class="columns is-multiline is-mobile">
                              ${generateImageColumns(data.subdir)}
                          </div>
                      </div>
                      <div class="column has-text-centered">
                          <h3 class="subtitle">\\( \\mathbf{x}_{t} \\to \\mathbf{x}_{t - \\Delta} \\) with Demon</h3>
                          <figure class="image">
                              <img class="result-image" src="static/images/html_demo/${data.subdir}/0.jpg" alt="Result Image">
                          </figure>
                      </div>
                  </div>
              </div>
          `);

          $playboxesContainer.append($playbox);
      });

      // Re-render MathJax after inserting new content
      MathJax.typesetPromise();
  });

  // Function to generate image columns
  function generateImageColumns(subdir) {
      var columns = '';
      for (let i = 0; i < 9; i++) {
          columns += `
              <div class="column is-one-third">
                  <figure class="image is-square">
                      <img src="static/images/html_demo/${subdir}/candidate_${i}.jpg" alt="Generated Image ${i}" class="selectable-image" data-index="${i}" data-subdir="${subdir}">
                  </figure>
              </div>
          `;
      }
      return columns;
  }

  // Event handler for image clicks (using event delegation)
  $(document).on('click', '.selectable-image', function() {
      const $img = $(this);
      const index = parseInt($img.data('index'));
      const subdir = $img.data('subdir');

      // Toggle 'selected' class
      $img.toggleClass('selected');

      // Initialize the selectedIndices array for this subdir if not already
      if (!selectedIndices[subdir]) {
          selectedIndices[subdir] = [];
      }

      // Update selected indices
      if ($img.hasClass('selected')) {
          // Add index to selectedIndices
          selectedIndices[subdir].push(index);
      } else {
          // Remove index from selectedIndices
          selectedIndices[subdir] = selectedIndices[subdir].filter(i => i !== index);
      }

      // Update the result image
      updateResultImage(subdir, selectedIndices[subdir]);
  });

  function updateResultImage(subdir, indices) {
      // Compute the target image index based on selected images
      let targetIndex = 0;
      indices.forEach(i => {
          targetIndex += Math.pow(2, i);
      });

      // Build the image filename
      const resultImageSrc = `static/images/html_demo/${subdir}/${targetIndex}.jpg`;

      // Update the result image in the corresponding playbox
      $(`.playbox[data-subdir="${subdir}"] .result-image`).attr('src', resultImageSrc);
  }

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