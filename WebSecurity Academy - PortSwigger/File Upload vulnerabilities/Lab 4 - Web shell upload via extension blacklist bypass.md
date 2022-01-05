# Web shell upload via extension blacklist bypass
Solution:
- Uploaded files are stored at `/files/avatars/`
- We can't upload php files directly. We get this error if we try to upload one:
```txt
Sorry, php files are not allowed Sorry, there was an error uploading your file.
```
- We can however upload our own malicious .htaccess file that will map another extension such as .ppt to php. Upload a file named `.htaccess` with contents as follows:
```png
AddType application/x-httpd-php .ppt
```
- This will map .ppt extension to php and will execute .ppt files as if it were a .php file
- Now upload a webshell with name `shell.ppt` to read the contents of the required file.