 var player = document.getElementById('player');

  var handleSuccess = function(stream) {
    console.log(stream);
    player.srcObject = stream;
    player.play()
  };

  navigator.mediaDevices.getUserMedia({ audio: false, video: true })
      .then(handleSuccess)

