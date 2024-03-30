let socket = new WebSocket("ws://localhost:6969", "protocolOne");
let image = undefined;

socket.onmessage = function (event) {
  image ??= document.getElementById("frame");
  image.src = "data:image/jpeg;base64," + event.data;
};
