#Created by Max and Sam
#go_to() for redirecting
#https://webbot.readthedocs.io/en/latest/webbot.html reference
from bs4 import BeautifulSoup
import requests
from webbot import Browser
import getpass

root_url='https://stinet.southeasttech.edu'
coursework_pages=[]

print('Enter your sti username:')
username = input()

print('Enter your sti password:')
password = getpass.getpass('password:')

web = Browser()
web.fullscreen_window()

web.go_to(root_url)

#login
web.type(username, id="userName")
web.type(password, id="password")
web.click(id="siteNavBar_btnLogin")

#get the html and add it to the parser
soup = BeautifulSoup(web.get_page_source(), "html5lib")
for link in soup.find_all('a'):
    if "/ICS/Academics/CIS" in link.get('href'):
        coursework_pages.append(link.get('href'))

#first attempt at getting getting assignments
for page in coursework_pages:
    web.go_to(root_url + page + "Coursework.jnz")
    soup = BeautifulSoup(web.get_page_source(), "html5lib")
    print(soup.find(id='pg0_V__dueNext__rptDueNext_ctl00__hypAssign'))
    print(soup.find(id='pg0_V__dueNext__rptDueNext_ctl01__hypAssign'))
