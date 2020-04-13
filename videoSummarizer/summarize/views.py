from django.shortcuts import render
from summarize.models import *

# Create your views here.
def home(request):
	return render(request, 'index.html')