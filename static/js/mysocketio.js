$(document).ready(function() {
   // The http vs. https is important. Use http for localhost!
   var socket = io.connect('http://' + document.domain + ':' + location.port);

   // START button was clicked
   $("#start").click(function () {
      socket.emit('start', 'start');
   });

   // HIT button was clicked
   $("#hit").click(function () {
      socket.emit('hit', 'hit');
   });

   // STAND button was clicked
   $("#stand").click(function () {
      socket.emit('stand', 'stand');
   });

   // RESTART button was clicked
   $("#restart").click(function () {
      socket.emit('restart', 'restart');
   });

   // handle 'continue' event sent from server
   socket.on('continue', function(msg) {
      location.reload();
   });

   // handle 'restart' event sent from server
   socket.on('restart', function(msg) {
      window.location.replace("/join");
   });

   // handle 'result page' event sent from server
   socket.on('result', function(msg) {
      window.location.replace("/result")
   });
});