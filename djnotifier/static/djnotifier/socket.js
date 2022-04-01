var protocol = (window.location.protocol == 'http:') ? 'ws://' : 'wss://';
var endpoint = "djnotifier"
var webSocketEndpoint =  protocol + window.location.host + '/' + endpoint + '/';
var socket = new ReconnectingWebSocket(webSocketEndpoint);

socket.onmessage = function(e){
  let data = JSON.parse(e.data);
  DJNotifier(style=data.type || 'info', text=data.message, audio=true)
}

// Socket Connet Functionality
socket.onopen = function(e){
    // more logic here...
}

// Socket Error Functionality
socket.onerror = function(e){
  // more logic here...
}

// Socket close Functionality
socket.onclose = function(e){
  console.log('Disconnected from djnotifier')
}