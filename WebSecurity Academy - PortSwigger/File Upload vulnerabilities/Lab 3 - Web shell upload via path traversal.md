# Web shell upload via path traversal
Solution:
- There is path traversal in the server's file upload feature.
- Files are uploaded at `/files/avatars/`
- In the file upload request, change the filename to `%2e%2e%2fshell.php`
- This will upload the file in the `/files` directory which allows php file execution.