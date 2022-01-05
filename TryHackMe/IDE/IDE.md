##### Room Name: [IDE](https://tryhackme.com/room/ide)
##### Difficulty: Easy
##### Room Description: An easy box to polish your enumeration skills!
---

## Enumeration

### Nmap
```js
PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.3
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.14.14.78
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 e2:be:d3:3c:e8:76:81:ef:47:7e:d0:43:d4:28:14:28 (RSA)
|   256 a8:82:e9:61:e4:bb:61:af:9f:3a:19:3b:64:bc:de:87 (ECDSA)
|_  256 24:46:75:a7:63:39:b6:3c:e9:f1:fc:a4:13:51:63:20 (ED25519)
80/tcp    open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
62337/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: B4A327D2242C42CF2EE89C623279665F
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Codiad 2.8.4
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

```

### FTP
Anonymous login is allowed according to the nmap scan. Login with the following creds: <span style="color:lightgreen">**anonymous**</span> : <span style="color:lightgreen">**anonymous**</span>.

After logging in, we have to traverse to the `...` directory and then download the file named `-`. To download that file, simply use `get ./-` command.

I have renamed it to ftp-file after downloading for convenience.
Contents of ftp-file:
```sh
$ cat ftp-file          
Hey john,
I have reset the password as you have asked. Please use the default password to login. 
Also, please take care of the image file ;)
- drac.
```

It hints us about two things:
1. There are atleast two different users named `drac` and `john`.
2. The password of the user `john` is a default password (which will be easy to crack because of it)

### The web server
* Port <span style="color:lightgreen">80</span>: It has the default apache webpage. After directory busting, there we couldn't find anything useful.
* Port <span style="color:lightgreen">62337</span>: We get a login page of Codiad (version: 2.8.4). Codiad is a web-based IDE and code editor. 
   
 ![codiad-login](https://raw.githubusercontent.com/Manash404/CTF/main/TryHackMe/IDE/images/codiad-login.png)

From above, we know that the user `john` has default password. I tried some passwords and was able to login with the creds: <span style="color:lightgreen">**john**</span> : <span style="color:lightgreen">**password**</span>.

While exploring the website, I created a project with the absolute path `/var/www/html/codiad/xplo1t`
### Searching for exploits:
I used searchsploit to search for any known exploits in Codiad.


```sh
$ searchsploit codiad
--------------------------------------------------------- ---------
 Exploit Title                                           |  Path
--------------------------------------------------------- ---------
Codiad 2.4.3 - Multiple Vulnerabilities                  | php/webapps/35585.txt
Codiad 2.5.3 - Local File Inclusion                      | php/webapps/36371.txt
Codiad 2.8.4 - Remote Code Execution (Authenticated)     | multiple/webapps/49705.py
Codiad 2.8.4 - Remote Code Execution (Authenticated) (2) | multiple/webapps/49902.py
Codiad 2.8.4 - Remote Code Execution (Authenticated) (3) | multiple/webapps/49907.py
--------------------------------------------------------- ---------
Shellcodes: No Results

```

For me, the last exploit worked after some tweaking.
![modify-exploit](https://raw.githubusercontent.com/Manash404/CTF/main/TryHackMe/IDE/images/modify-exploit.png)

Run the exploit:
![exploit](https://raw.githubusercontent.com/Manash404/CTF/main/TryHackMe/IDE/images/exploit.png)
Set the path for Codiad as `/` and the name of the actual project as `xplo1t` (we have already created a project of this name earlier. Remember?)
This will upload a webshell `shell.php` in `/xplo1t/shell.php`

![webshell](https://raw.githubusercontent.com/Manash404/CTF/main/TryHackMe/IDE/images/webshell.png)

We now have a shell as `www-data`
To get a proper shell, I used one of the reverse shells from [Revshells](https://www.revshells.com/)
In the `.bash_history` file of the user `drac` , I found the password.
![creds-drac](https://raw.githubusercontent.com/Manash404/CTF/main/TryHackMe/IDE/images/creds-drac.png)

Switch to drac with this password (Password reuse).
User drac can run as sudo the following:
![drac-sudo](https://raw.githubusercontent.com/Manash404/CTF/main/TryHackMe/IDE/images/drac-sudo.png)

Check for files related to the vsftpd service:
![vsftpd-service](https://raw.githubusercontent.com/Manash404/CTF/main/TryHackMe/IDE/images/vsftpd-service.png)
The file `/lib/systemd/system/vsftpd.service` is writable by drac. Let's change the service file and make `/bin/bash` a SUID so that we can get root.

This is how we can do it:
![root](https://raw.githubusercontent.com/Manash404/CTF/main/TryHackMe/IDE/images/root.png)
