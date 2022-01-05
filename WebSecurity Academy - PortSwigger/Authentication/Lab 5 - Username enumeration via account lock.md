# Username enumeration via account lock
Solution:
- Do a clusterbomb attack with the usernames and 5 of the passwords
- For incorrect login attempts, we get error `Invalid username or password.`
- For a certain username, we get a different error message:
	```
	You have made too many incorrect login attempts. Please try again in 1 minute(s).
	```
- Make a note of this username and do a Sniper attack with that username and all the other passwords.
- Make a Grep Extract for the error message. Notice that for a particular password, there is no error message.
- Wait for 1 minute for the account lock to reset.
- Login with this username & password