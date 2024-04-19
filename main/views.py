from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def cart(request):
    return HttpResponse('Home Page')


def checkout(request):
    return HttpResponse('Home Page')


def number(request):
    return HttpResponse('Home Page')