# Blind SSRF with out-of-band detection
Solution:
- Copy the unique Burp collaborator url to clipboard
- Intercept the request and change the Referer header to that unique collaborator url
- Click `Poll now` on collaborator client and we will see some DNS and HTTP queries to our collaborator server