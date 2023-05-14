$(document).ready(function() {
    // When the pop-up trigger is clicked
    $('#popup-trigger').click(function(e) {
      // Prevent the default link behavior
      e.preventDefault();
  
      // Show the pop-up container
      $('#popup-container').show();
    });
  
    // When the pop-up close button is clicked
    $('#popup-container .close-button').click(function() {
      // Hide the pop-up container
      $('#popup-container').hide();
    });
  });