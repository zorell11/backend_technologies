from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.


def hello(request):
    return HttpResponse('Hello Zoltan')



def hello1(request, s):
    return HttpResponse(f'hello {s}')


def hello2(request):
    print(10*'*')
    print(request)
    print()
    print(request.GET)
    s = request.GET.get('s', '')
    return HttpResponse(f'Hello {s}')

