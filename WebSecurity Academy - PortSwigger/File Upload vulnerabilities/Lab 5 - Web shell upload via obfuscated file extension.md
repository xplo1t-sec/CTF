# Web shell upload via obfuscated file extension
Solution:
- Files are uploaded at `/files/avatars/`
- Certain file extensions are blacklisted so we can't simply upload a php webshell
- Files containing extensions jpg and png are accepted.
- Use the following name `shell.php%00.jpg`.
-