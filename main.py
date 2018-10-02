#Created by Max and Sam

from bs4 import BeautifulSoup
import requests
from webbot import Browser

print('Enter your sti username:')
username = input()

print('Enter your sti password:')
password = input()

web = Browser()
web.go_to('https://stinet.southeasttech.edu/ics/')
web.type(username, id="userName")
web.type(password, id="password")
web.click(id="siteNavBar_btnLogin")

