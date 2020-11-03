from django.shortcuts import HttpResponse, render, redirect
from django.http.response import StreamingHttpResponse
# from .forms import location_pv
from django.template import RequestContext

def index(request):
    return render(None, 'index.html')

