function run(wsUri){
  var output;
  var websocket;

  function writeToScreen(message) {
    var pre = document.createElement("p");
    pre.style.wordWrap = "break-word";
    pre.innerHTML = message;
    output.appendChild(pre);
  }

  function doSend(message) {
    writeToScreen("SENT: " + message);
    websocket.send(message);
  }

  function onOpen(evt) {
    writeToScreen("CONNECTED");
    doSend("websocket echo test.");
  }

  function onClose(evt) {
    writeToScreen("DISCONNECTED");
  }

  function onMessage(evt) {
    writeToScreen('<span style="color: blue;">RESPONSE: ' + evt.data+'</span>');
    websocket.close();
  }

  function onError(evt) {
    writeToScreen('<span style="color: red;">ERROR:</span> ' + evt.data);
  }

  function testWebSocket() {
    websocket = new WebSocket(wsUri);
    websocket.onopen = function(evt) {
      onOpen(evt);
    };
    websocket.onclose = function(evt) {
      onClose(evt);
    };
    websocket.onmessage = function(evt) {
      onMessage(evt);
    };
    websocket.onerror = function(evt) {
      onError(evt);
    };
  }

  function init() {
    output = document.getElementById("output");
    testWebSocket();
  }

  window.addEventListener("load", init, false);
}

