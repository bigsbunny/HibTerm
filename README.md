# HibTerm

HibTerm is a CLI tool for fetching notices from IIIT Bhubaneswar\'s official college portal - M-UMS.

------------
## Module Requirements :
- Click
- Requests
- BeautifulSoup4

## Installation Steps :
1. Clone this repository using `git clone https://github.com/bigsbunny/HibTerm.git`
2. `cd HibTerm`
3. `python3 -m pip install .`

***Note : This will install the package system-wide. In order to avoid dependency conflicts, you can setup HibTerm inside a Virtual Environment.***



## How to use :
After installing **HibTerm** on your system, you can launch it from the terminal by typing `hibterm` after the prompt. Then you will be prompted to enter your **Student ID and Password**. After you provide it with the correct credentials, HibTerm will return an **ordered list** of all the official notices. Then you will be prompted to enter the index number of the notice that you want to view. After typing in the index number of the notice you will be able to view the notice contents. If the respective notice includes an attachment, then it will be **automatically downloaded** to the user\'s `~/Downloads` directory.

## About HibTerm :
*Well, I would say that HibTerm is still a **WIP**, as I plan on extending it\'s functionality to achieve various other stuff too, that cover the various aspects of M-UMS.*