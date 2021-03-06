$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    //var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host  + window.location.pathname);
    alert(window.location.host);
    alert(window.location.pathname);
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<tr></tr>')
	alert(message.data);
	//ele.append($"<th rowspan="3"></th>")
	//ele.append($'<tr>')
        ele.append(
            $("<td></td>").text(data.handle)
        )
	//ele.append($"</tr>")
	ele.append(
            $("<td></td>").text(data.timestamp)
        )
	//ele.append($"</tr>")
        ele.append(
            $("<td></td>").text(data.message)
        )
        /*<tr>
	  <th rowspan="2"></th>
	  	<td><p><b>{{ statement.handle }}</b></td>	
	  </tr>
	  <tr>
	  	<td><i>{{ statement.formatted_timestamp }}</i></td>
	  </tr>
	  <tr>     
                <td>{{ statement.message }}</td>
	  </tr>*/
        chat.append(ele)
    };

    $("#chatform").on("submit", function(event) {
	
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
	alert("inside submit");
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
});
