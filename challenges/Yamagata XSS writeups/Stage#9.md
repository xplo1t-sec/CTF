It requires us to change the charset to utf-7 in the request and send a payload such as `+ADw-script+AD4-alert(document.domain)+ADw-+AC8-script+AD4-`
But latest browsers do not support UTF-7. 
Just use alert(document.domain) in the console and pass the lab

Reading materials:
* http://michaelthelin.se/security/2014/06/08/web-security-cross-site-scripting-attacks-using-utf-7.html
* https://nedbatchelder.com/blog/200704/xss_with_utf7.html

Online UTF-7 encoder:
* https://www.novel.tools/encode/UTF-7