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
    document.getElementById('back').style.padding = '2px';
    document.getElementById('back').style.float = 'none';
    document.getElementById('back').style.textAlign = 'center';

    // Moves and resizes the login information on a smaller screen.
    document.getElementById('user').style.width = 'auto';
    document.getElementById('user').style.margin = 'auto';
    document.getElementById('user').style.padding = '2px';
    document.getElementById('user').style.float = 'none';
    document.getElementById('user').style.textAlign = 'center';

    document.getElementById('title').style.padding = '2px';

    // Resizes the voting columns on a smaller screen.
    var containers = document.getElementsByClassName('sortable-container');
    for (var i = 0; i < containers.length; i += 1) {
      containers[i].style.width = '90%';
      containers[i].style.margin = 'auto';
      containers[i].style.float = 'none';
    }

    // Resizes the results column on a smaller screen.
    var containers = document.getElementsByClassName('results-list');
    for (var i = 0; i < containers.length; i += 1) {
      containers[i].style.width = '90%';
    }
  }
}
