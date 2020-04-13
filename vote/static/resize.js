function resize() {
  const width = $(window).width();

  if (width < 700) {
    $('body').addClass('small-screen');
    $('body').removeClass('medium-screen');
  }
  else if (width < 900) {
    $('body').addClass('medium-screen');
    $('body').removeClass('small-screen');
  }
  else {
    $('body').removeClass('small-screen medium-screen');
  }

  // Resizes the title buffer which pushes content down below the floating title bar
  $('#title-buffer').height($('#title-bar').outerHeight());
}

$(document).ready(resize);
$(window).resize(resize);
$(window).on('orientationchange', resize);

