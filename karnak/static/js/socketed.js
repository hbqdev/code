
// Depends on jquery.js

function setupMuxSocket() {

  var wsuri;
  
  if (window.location.protocol === "file:") {
    wsuri = "ws://localhost:9000";
  } else {
    wsuri = "ws://" + window.location.hostname + ":9000";
  }
  
  if ("WebSocket" in window) {
    sock = new WebSocket(wsuri);
  } else if ("MozWebSocket" in window) {
    sock = new MozWebSocket(wsuri);
  } else {
    log("Browser does not support WebSocket!");
    window.location = "/error";
  }
  
  if (sock) {
    sock.onopen = function() {
      log("Connected to " + wsuri);
    }
    
    sock.onclose = function(e) {
      log("Connection closed (wasClean = " + e.wasClean + ", code = " + e.code + ", reason = '" + e.reason + "')");
      sock = null;
    }
    
    sock.onmessage = function(e) {
      content = JSON.parse(e.data);
      // document.getElementById("snapshot").src = content["snapshot:src"];
      log(content["msg:html"]);
      for (var key in content) {
	request = key.split(':');
	log(request)
	  switch (request[1]){
	  case "replaceWith": // DANGEROUS!
	    $("#"+request[0]).replaceWith(content[key]);
	    break;
	  case "append": // LESS DANGEROUS!
	    $("#"+request[0]).append(content[key]);
	    break;
	  case "html":
	    $("#"+request[0]).html(content[key]);
	    break;
	  case "retile":
	    // call the masonry re-do
	    break;
	  default:
	    $("#"+request[0]).attr(request[1],content[key]);
	  }
      }
    }
  }
};

function broadcast() {
  var msg = document.getElementById('message').value;
  if (sock) {
    sock.send(msg);
    log("Sent: " + msg);
  } else {
    log("Not connected.");
  }
};

function log(m) {
  $('#log').innerHTML += m + '\n';
  $('#log').scrollTop = ellog.scrollHeight;
};
