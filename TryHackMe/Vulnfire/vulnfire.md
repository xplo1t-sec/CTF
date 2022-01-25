# Nmap Scan
```js
PORT   STATE  SERVICE  VERSION
20/tcp closed ftp-data
21/tcp open   ftp      vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.9.2.79
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
22/tcp open   ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 5a:a7:bb:e0:71:4d:a6:de:b1:4a:33:99:08:64:8c:e1 (RSA)
|   256 1d:01:1f:df:79:84:47:f3:20:fb:72:c3:d6:20:71:03 (ECDSA)
|_  256 ef:10:bb:ea:d7:44:88:5b:ef:57:03:8c:45:20:1a:8e (ED25519)
80/tcp open   http     Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

# Enumerating FTP
- FTP has `anonymous` login **enabled**
- We can login with anonymous:anonymous credentials
- Listing the files using `ls -la` we see there are two files `confidential.zip` and `note.txt`
- Download the files to local system using `mget *` command
 
 ![ftp.png](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Vulnfire/images/ftp.png)

- Contents of note.txt file:
```txt
1) Enumerate your webserver to find a file 
2) PHP is easy!
3) I bet you can't look deep inside an image
```
Let's enumerate the webserver first. After that we will look into the `confidential.zip` file.
# Enumerating the web server
On visiting the website at http://IP we are presented the default Apache web page. Let's fuzz for files and directories and files. We will include the `.php` extension because of the hint and add a few other extensions such as `.txt` and `.html`.
We find two interesting results:
* security.php
	* Upon visiting this page, we are taken to `/op_security.php?cmd=`
* somerandomhiddenfilethatyoucantfind48685475814.txt
```txt
	Steganography is super awesome and l337 techinque. 

	Xp********************37
```
Okay, so we need to do some form of steganography based on the hint above. Let's save this weird string somewhere accessible. We might need it later.

Let's check whats up with `/op_security.php` file.
The source of the page contains the following message:

![params.png](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Vulnfire/images/params.png)

So these are possibly parameters where one of them is an actual parameter vulnerable to command injection. Download the parameters from the webpage and save it to a file. I used some grep and regex magic to save it with this one liner. Change the IP address accordingly:
```bash
curl -s http://10.10.250.99/op_security.php | grep -v '<\|>\|!\|^$' > params.txt
```
The `grep` will filter out all lines except the required ones.
Now, lets fuzz these parameters with ffuf. I will filter out normal responses with this filter: `-fs 602`
```bash
ffuf -u http://10.10.250.99/op_security.php?FUZZ=id -w ./params.txt -fs 602
```
The malicious parameter is the correct parameter

![param-fuzz.png](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Vulnfire/images/param-fuzz.png)


At this point, we can get a shell on the system.  Let's first check 
what's inside `confidential.zip` 

![confidential-zip.png](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Vulnfire/images/confidential-zip.png)

# Unravelling the data!
* So we have to do steganography on this `fire.jpg` file
* When using steghide to extract from the image, we are asked a passphrase. Try using the weird string `Xp********************37` we found in string.txt on the web server.

![steghide.png](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Vulnfire/images/steghide.png)

* We get credentials in the form of ciphertext. Check the note and it hints towards some vi... cipher. Try with Vigenere cipher. Let's use CyberChef to do this. CyberChef is a handy tool made for things just like these.
* But we need a key to decode the cipher. If you notice, the word 'Think' is quoted in creds.txt. Use this as key and we now have a password `***********************`
* Let's use this password to login as `hellfire` user.

# Get into the system!
* Logging into the system as hellfire user, we get our cookie (user flag)
* There is an interesting file we can find: `xploit_msg.txt` :
```txt
Hey hellfire, have you seen this vulnfire1337 user? He's posting stuffs about our company, Vulnfire.Inc on social media. Please look into it ASAP!!
```
It says there is someone named vulnfire1337 posting about Vulnfire.Inc on social media. Let's do some OSINT!

# OSINT ftw!
There is a user with this name on Twitter. Visit the profile at https://twitter.com/vulnfire1337. There is a post about a password hash dump that links to pastebin at https://pastebin.com/TKRLXK8u
If at the time you're solving this room, the twitter account gets deleted, you can check https://web.archive.org for past snapshots :)

![vulnfire1337-twitter.png](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Vulnfire/images/vulnfire1337-twitter.png)

It mentions that the passwords are 25 characters long. But don't worry. Long passwords don't always mean strong passwords. If these passwords belong to password dictionaries such as rockyou.txt, it's a kids game to crack them. We can use hashcat to crack the hashes. If you have problems identifying the hash type, you can use tools like [Search-That-Hash](https://github.com/HashPals/Search-That-Hash)
It identifies the hash as SHA-256. Use mode 1400 for this hash type on hashcat.
```bash
hashcat -a 0 -m 1400 ./hashes /home/rockyou.txt
```
After cracking, store the passwords in a text file. I have used the `cut` linux command to split the lines by colon `:` and only take the cracked passwords (and not their corresponding hashes)
```bash
hashcat -a 0 -m 1400 hashes /home/rockyou.txt --show | cut -d ':' -f 2 > passwords.txt
```
We will now use hydra to brute force these passwords and login as xploit user.

![hydra-brute.png](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Vulnfire/images/hydra-brute.png)

Login as xploit with the found password. Now its time to enumerate.
There is a hidden folder `.bak` in `/var/backups`. This directory is not present by default. There is a compressed file inside of it.
```bash
xploit@vulnfire:/var/backups/.bak$ ls -la
total 2856
drwxr-x---+ 2 xploit xploit    4096 Jan 13 09:38 .
drwxr-xr-x  3 root   root      4096 Jan 24 09:09 ..
-rw-r--r--  1 root   root   2914458 Jan 13 09:14 secret.tar
xploit@vulnfire:/var/backups/.bak$ 
```
Download it locally and extract it to find its contents. We should always try to have as little footprint on our target!
Use the scp command to download the file using the SSH protocol. Files will be transferred to your device securely.
```bash
scp xploit@10.10.156.56:/var/backups/.bak/secret.tar ./secret.tar
```
Extract the file and we now have four PCAP files. A PCAP file is a packet capture containing network traffic data. It can be used to analyse and monitor network traffic. Data transmitted in certain protocols such as HTTP and FTP can be viewed in cleartext. This means if there was any sensitive data (such as credentials) saved in the capture, we will be able to view it.
If you look closely among the pcap files, the file `secret4.pcap` contains a login brute force attempt on HTTP at /login.php. Let's use this wireshark filter to check if there is any correct password here:
```txt
http.response.code!=200
```
With correct credentials, the website redirects the user to `dashboard.php` . With the above filter, there will be only one result. Follow the HTTP stream of that packet:

![follow-http.png](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/TryHackMe/Vulnfire/images/follow-http.png)


We have the password
```txt
username=root&password=<SNIP>
```
Before using the password, we first have to URL decode it. This is because of the Content-Type header set as `application/x-www-form-urlencoded`. Any non alphanumeric character is URL encoded when using this Content-Type. Check out https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST for more info.

Login as root with the now decoded password and complete the room 🎉