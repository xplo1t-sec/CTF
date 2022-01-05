# Username enumeration via subtly different responses
Solution:
- Use burp intruder and brute force usernames
- Set grep extract on the `Invalid username or password` line (along with the HTML tags)
- After running intruder, we can see that one of the results miss the full stop `.` in the error message.
- ![[Pasted image 20211120180846.png]]
- This is our valid username
- Now brute force password with this username and login.