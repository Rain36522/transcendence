from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def members(request):
  mymembers = ["apple", "banana", "cherry"]
  template = loader.get_template('test.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))


def members2(request):
  template = loader.get_template('test2.html')
  return HttpResponse(template.render())