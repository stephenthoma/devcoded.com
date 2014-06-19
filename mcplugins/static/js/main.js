// Sticky header
$(document).ready(function() {
  $('.main-nav-list').onePageNav({
    scrollThreshold: 0.2, // Adjust if Navigation highlights too early or too late
    scrollOffset: 75 //Height of Navigation Bar
  });

  // Sticky Header - http://jqueryfordesigners.com/fixed-floating-elements/
  var top = $('#main-nav').offset().top - parseFloat($('#main-nav').css('margin-top').replace(/auto/, 0));

  $(window).scroll(function (event) {
    // what the y position of the scroll is
    var y = $(this).scrollTop();

    // whether that's below the form
    if (y >= top) {
      // if so, add the fixed class
      $('#main-nav').addClass('fixed');
    } else {
      // otherwise remove it
      $('#main-nav').removeClass('fixed');
    }
  });
});

// Parallax
$(document).ready(function(){
  var $window = $(window);
  $('div[data-type="background"], header[data-type="background"], section[data-type="background"]').each(function(){
    var $bgobj = $(this);
    $(window).scroll(function() {
      var yPos = -($window.scrollTop() / $bgobj.data('speed'));
      var coords = '50% '+ yPos + 'px';
      $bgobj.css({
        backgroundPosition: coords
      });
    });
  });
});
