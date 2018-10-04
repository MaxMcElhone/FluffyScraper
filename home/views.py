from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'title': 'course 1',
        'body': 'assignment 1'
    },
    {
        'title': 'course 2',
        'body': 'assignment 2'
    }
]

# Create your views here.
def index(request):
    context = {
        'posts': posts
    }
    return render(request, 'home/index.html', context)
