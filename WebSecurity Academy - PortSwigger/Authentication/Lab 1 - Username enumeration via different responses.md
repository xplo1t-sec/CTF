# Username enumeration via different responses
Solution:
- First brute force username with given username wordlist
- Set grep match as `Invalid username`
- We get a valid username `applications`
- Now set username to `applications` and brute force password with given password wordlist
- Set grep match as `Invalid password`
- `987654321` is the correct password
- Login with these creds 