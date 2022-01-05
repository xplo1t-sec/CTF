# Remote code execution via polyglot web shell upload
Solution:
- Files are uploaded at `/files/avatars/`
- Webserver accepts files based on it's magic bytes
- I tried uploading an image file that had the following hex bytes it's header:
```js
52 49 46 46  44 43 00 00   57 45 42 50  56 50 38 20
```
- Add these to the php webshell and the webserver will accept it.