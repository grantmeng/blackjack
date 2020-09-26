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

   // handle 'server done' event sent from server
   socket.on('server done', function(msg) {
      location.reload();
   });

   // handle 'result page' event sent from server
   socket.on('result', function(msg) {
      alert("didnt work");
      window.location.replace("/result")
   });
});