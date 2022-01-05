##### Challenge name: Terrapin
##### Category: Misc
---

1. Unzip the Terrapin.zip zipfile to get the pdf file named Terrapin.pdf 
2. Contents of the pdf:
    - Instructions:
    
        ```
        ▷ btw I love snakes
        ▷ F means Forward
        ▷ R means ?
        ▷ L means?
        ▷ PU means Penup
        ▷ PD means?
        ▷ C means cricle
        ▷ Do you know one thing? Pastebin is cool
        ````
    - Terrapin code:
    
        ```
        PU,L(180),F(300),PD,R(90),F(50),R(90),F(20),R(180),C(12,-180),R(180),F(20),R(180),F(20),R(180),C(12,-180),R(180),F(20),PU,R(180),F(50),L(90),PD,F(50),R(90),F(30),R(180),F(30),L(90),F(20),L(90),F(20),PU,F(20),L(90),PD,F(20),R(90),F(20),R(180),C(10,-180),R(180),F(20),L(90),F(30),R(180),F(30),R(135),F(45),L(45),PU,F(20),PD,L(90),F(30),L(180),F(15),L(45),F(25),L(180),F(25),R(90),F(25),PU,R(45),F(10),PD,L(90),F(20),R(90),F(30),L(180),F(30),L(90),F(35),C(17,-270),R(180),F(17),PU,R(180),F(50),L(90),PD,F(35),R(180),F(12),C(11,-180),R(180),F(30),PU,L(90),F(30),PD,C(30,170),C(20,360),PU,L(188),F(30),R(47),PD,F(35),L(98),F(35),L(180),F(35),L(42),F(30)
        ```
3. First I searched for "Pen Up Pen Down python" in Google to search for any python module that could help me with this code. I found some references to "turtle". And after some searching, I came across Turtle Graphics. Here is the documentation for this: https://docs.python.org/3/library/turtle.html
This GeeksforGeeks link will also help you familiarize with Turtle Graphics: https://www.geeksforgeeks.org/turtle-programming-python/
4. Now we need to convert the given commands in the PDF into the turtle commands.

    ```
    F -> turtle.fd()
    R -> turtle.rt()
    L -> turtle.lt()
    PU -> turtle.pu
    PD -> turtle.pd
    C -> turtle.circle()
    ```
    
5. Now time to write the script:
    
    ```py
    #!/usr/bin/env python3

    import turtle

    turtle.pu
    turtle.lt(180)
    turtle.fd(300)
    turtle.pd
    turtle.rt(90)
    turtle.fd(50)
    turtle.rt(90)
    turtle.fd(20)
    turtle.rt(180)
    turtle.circle(12,-180)
    turtle.rt(180)
    turtle.fd(20)
    turtle.rt(180)
    turtle.fd(20)
    turtle.rt(180)
    turtle.circle(12,-180)
    turtle.rt(180)
    turtle.fd(20)
    turtle.pu
    turtle.rt(180)
    turtle.fd(50)
    turtle.lt(90)
    turtle.pd
    turtle.fd(50)
    turtle.rt(90)
    turtle.fd(30)
    turtle.rt(180)
    turtle.fd(30)
    turtle.lt(90)
    turtle.fd(20)
    turtle.lt(90)
    turtle.fd(20)
    turtle.pu
    turtle.fd(20)
    turtle.lt(90)
    turtle.pd
    turtle.fd(20)
    turtle.rt(90)
    turtle.fd(20)
    turtle.rt(180)
    turtle.circle(10,-180)
    turtle.rt(180)
    turtle.fd(20)
    turtle.lt(90)
    turtle.fd(30)
    turtle.rt(180)
    turtle.fd(30)
    turtle.rt(135)
    turtle.fd(45)
    turtle.lt(45)
    turtle.pu
    turtle.fd(20)
    turtle.pd
    turtle.lt(90)
    turtle.fd(30)
    turtle.lt(180)
    turtle.fd(15)
    turtle.lt(45)
    turtle.fd(25)
    turtle.lt(180)
    turtle.fd(25)
    turtle.rt(90)
    turtle.fd(25)
    turtle.pu
    turtle.rt(45)
    turtle.fd(10)
    turtle.pd
    turtle.lt(90)
    turtle.fd(20)
    turtle.rt(90)
    turtle.fd(30)
    turtle.lt(180)
    turtle.fd(30)
    turtle.lt(90)
    turtle.fd(35)
    turtle.circle(17,-270)
    turtle.rt(180)
    turtle.fd(17)
    turtle.pu
    turtle.rt(180)
    turtle.fd(50)
    turtle.lt(90)
    turtle.pd
    turtle.fd(35)
    turtle.rt(180)
    turtle.fd(12)
    turtle.circle(11,-180)
    turtle.rt(180)
    turtle.fd(30)
    turtle.pu
    turtle.lt(90)
    turtle.fd(30)
    turtle.pd
    turtle.circle(30,170)
    turtle.circle(20,360)
    turtle.pu
    turtle.lt(188)
    turtle.fd(30)
    turtle.rt(47)
    turtle.pd
    turtle.fd(35)
    turtle.lt(98)
    turtle.fd(35)
    turtle.lt(180)
    turtle.fd(35)
    turtle.lt(42)
    turtle.fd(30)
    turtle.done()
    ```
    
6. Run the script and the output will be of a string consisting of random characters: `BFRk5n9Y`
![image](https://user-images.githubusercontent.com/29172095/135710071-0bca5533-acb0-40c7-aaae-c112dcf15a3d.png)

7. I was not sure what to do with this string. Tried base64 decoding but that gave me junk output. My teammate suggested me to check for pastebins of that ID https://pastebin.com/BFRk5n9Y and we have our flag in that pastebin.

Flag: **TamilCTF{7urtl3s_4r3_veRrrRyy_sl0ww}**
