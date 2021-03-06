#Created by Max and Sam
#https://webbot.readthedocs.io/en/latest/webbot.html reference
from django.db import models
from bs4 import BeautifulSoup
from webbot import Browser
import getpass

# Coursework model for pulling due next assignments
# from stinet
class Coursework:
    @staticmethod
    def coursework(user):
        root_url='https://stinet.southeasttech.edu'
        coursework_pages=[]
        coursework = []

        userName = user.get('user')
        password = user.get('password')
        web = Browser()
        web.fullscreen_window()

        web.go_to(root_url)

        #login
        web.type(userName, id="userName")
        web.type(password, id="password")
        web.click(id="siteNavBar_btnLogin")

        #get the html and add it to the parser
        soup = BeautifulSoup(web.get_page_source(), "html5lib")
        mycourses = soup.find(id='myCourses')
        for link in mycourses.find_all('a'):
            if "/ICS/Academics/" in link.get('href'):
                coursework_pages.append(link.get('href'))

        #first attempt at getting getting assignments
        for page in coursework_pages:
            className = None
            web.go_to(root_url + page + "Coursework.jnz")
            soup = BeautifulSoup(web.get_page_source(), "html5lib")
            for data in soup.select('.sidebar-link-title a'):
                className = data.text
            #assignment1 = soup.find(id='pg0_V__dueNext__rptDueNext_ctl00__hypAssign')
            #assignment2 = soup.find(id='pg0_V__dueNext__rptDueNext_ctl01__hypAssign')
            assignment1 = try_find(soup, 'pg0_V__dueNext__rptDueNext_ctl00__hypAssign')
            assignment2 = try_find(soup,'pg0_V__dueNext__rptDueNext_ctl01__hypAssign')
            course = {
                'courseName': className,
                'courseUrl': root_url + page + "Coursework.jnz",
            }



            # course = {
            #     'courseName': className,
            #     'courseUrl': root_url + page + "Coursework.jnz",

            if assignment1 is not None:
                course['assignment1'] = assignment1.text
                course['assignment1Desc'] = assignment1.get('aria-label')
                course['assignment1Link'] = root_url + assignment1.get('href')
                course['assignment1Progress'] = soup.find(id='pg0_V__dueNext__rptDueNext_ctl00__lblInfo').text
            else:
                course['assignment1'] = ''
                course['assignment1Desc'] = ''
                course['assignment1Link'] = ''
                course['assignment1Progress'] = ''
            if assignment2 is not None:
                course['assignment2'] = assignment2.text
                course['assignment2Desc'] = assignment2.get('aria-label')
                course['assignment2Link'] = root_url + assignment2.get('href')
                course['assignment2Progress'] = soup.find(id='pg0_V__dueNext__rptDueNext_ctl01__lblInfo').text
            else:
                course['assignment2'] = ''
                course['assignment2Desc'] = ''
                course['assignment2Link'] = ''
                course['assignment2Progress'] = ''
            # }

            coursework.append(course.copy())

        web.close_current_tag()
        return coursework;

def try_find(soup, idIn):
    try:
        return soup.find(id=idIn)
    except:
        return None
