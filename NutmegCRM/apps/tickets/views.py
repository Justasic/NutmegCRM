__author__ = 'justasic'
from django.shortcuts import render_to_response, render
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello world from tickets! :D')