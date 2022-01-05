# SSRF with blacklist-based input filter
Solution:
- The filter blocks two things
	- The localhost IP address 127.0.0.1
	- The word admin
- I used the decimal IP notation `2130706433` and the word `Admin` to access the admin panel