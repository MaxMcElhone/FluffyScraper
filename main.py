#Created by Max and Sam
#go_to() for redirecting
#https://webbot.readthedocs.io/en/latest/webbot.html reference
from bs4 import BeautifulSoup
import requests
from webbot import Browser
import getpass

root_url='https://stinet.southeasttech.edu/'

print('Enter your sti username:')
username = input()

print('Enter your sti password:')
password = getpass.getpass('password:')

web = Browser()
web.go_to(root_url)
web.type(username, id="userName")
web.type(password, id="password")
web.click(id="siteNavBar_btnLogin")
soup = BeautifulSoup(web.get_page_source())
for link in soup.find_all('a'):
    print(link.get('href'))
