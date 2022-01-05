# Broken brute-force protection, IP block
Solution:
- Too many incorrect logins give us this message
```
You have made too many incorrect login attempts. Please try again in 1 minute(s).
```
- The application has a broken logic that allows us to reset the timeout if we correctly login to the application.
- Every 3 incorrect login attempts start the timeout
- Brute force the login with pitchfork containing correct credentials after every 1 incorrect request. Also in the Resource Pool, set concurrent requests to max of 2