from django.shortcuts import render
from django.http import HttpResponse
from home.models import Coursework
#get user input from django
#https://stackoverflow.com/questions/25028895/very-simple-user-input-in-django
# posts = [
#     {
#         'title': 'course 1',
#         'body': 'assignment 1'
#     },
#     {
#         'title': 'course 2',
#         'body': 'assignment 2'
#     }
# ]

# Create your views here.
def index(request):
    stiUser = None
    if request.method == 'POST':
        user = request.POST.get('userName', '')
        password = request.POST.get('password', '')
        stiUser ={
            'user': user,
            'password': password
        }


    context ={
        'coursework': Coursework.coursework(stiUser)
    }

    return render(request, 'home/index.html', context)

def login(request):
    return render(request, "home/login.html")
