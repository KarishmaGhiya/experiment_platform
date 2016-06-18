$(function() {
    // When we're using HTTPS, use WSS too.
	alert("in function");
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    
    var waitsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host  + window.location.pathname);
    alert(window.location.host);
    alert(window.location.pathname);
    var message = {
        	  message: "Hello..Welcome YOU'LL BE REDIRECTED TO THIS URL: http://127.0.0.1:8000/chat/quiet-sun-7662/",
		  //handle: "myname",
           };
   //handle=nickname or workerid 
   alert("inside event function");
   waitsock.send(JSON.stringify(message));
   

 waitsock.onmessage = function(message) {
        
	alert("inside onmessage");        
	alert(message.data);
	var m = JSON.parse(message.data);
	alert(m.message);
	
	window.location.replace(m.message);
        
              
    };

	
    
});

