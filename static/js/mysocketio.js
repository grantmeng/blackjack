$(document).ready(function() {
   // The http vs. https is important. Use http for localhost!
   var socket = io.connect('http://' + document.domain + ':' + location.port);

   // timeout if no user action, pass to next user
   var timeout = setTimeout(function () {
      socket.emit('next', 'next');
   }, 10000);

   // START button was clicked
   $("#start").click(function () {
      socket.emit('start', 'start');
   });

   // HIT button was clicked
   $("#hit").click(function () {
      clearTimeout(timeout);
      socket.emit('hit', 'hit');
   });

   // STAND button was clicked
   $("#stand").click(function () {
      clearTimeout(timeout);
      socket.emit('stand', 'stand');
   });

   // RESTART button was clicked
   $("#restart").click(function () {
      socket.emit('restart', 'restart');
   });

   // RESET button was clicked
   $("#reset").click(function () {
      socket.emit('reset', 'reset');
   });

   // handle 'continue' event sent from server
   socket.on('continue', function(msg) {
      location.reload();
   });

   // handle 'result page' event sent from server
   socket.on('result', function(msg) {
      window.location.replace("/result")
   });

   // handle 'restart' event sent from server
   socket.on('restart', function(msg) {
      window.location.replace("/join");
   });

   // handle 'reset' event sent from server
   socket.on('reset', function(msg) {
      window.location.replace("/");
   });
});