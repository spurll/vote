document.addEventListener("DOMContentLoaded", function(event) {
  resizeContent()
  resizeBuffer()
});

window.onresize = function() {
  resizeBuffer()
};

function resizeBuffer() {
  // Resizes the title buffer which pushes content down below the floating title bar.
  document.getElementById('title-buffer').style.height = document.getElementById('title-bar').offsetHeight + 'px';
}

function resizeContent() {
  // http://stackoverflow.com/questions/1248081/get-the-browser-viewport-dimensions-with-javascript
  var width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
  if (width < document.getElementById('content').offsetWidth) {
    // Resizes the content window to be smaller if viewed on a small screen.
    document.getElementById('content').style.width = width;

    // Moves and resizes the back button information on a smaller screen.
    document.getElementById('back').style.width = 'auto';
    document.getElementById('back').style.margin = 'auto';
    document.getElementById('back').style.float = 'none';
    document.getElementById('back').style.textAlign = 'center';

    // Moves and resizes the login information on a smaller screen.
    document.getElementById('user').style.width = 'auto';
    document.getElementById('user').style.margin = 'auto';
    document.getElementById('user').style.float = 'none';
    document.getElementById('user').style.textAlign = 'center';
  }
}
