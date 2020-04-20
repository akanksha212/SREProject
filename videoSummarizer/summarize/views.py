from django.shortcuts import render
from summarize.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from .models import Video
from .forms import VideoForm
from django.template import RequestContext

global user_context
# Create your views here.
def home(request):
	return render(request, 'index.html')


def register(request):
	if request.method == 'POST':
		
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			context = {'form' : form}
			username = request.POST['username']
			request.session['username'] = username
			password = request.POST['password1']
			user = authenticate(username=username, password=password)
			user_context = {'user' : username}
			user_obj = User(Username = username, Password = password)
			user_obj.save()
			login(request, user)
			print("exiting from register ---------")
			return render(request, 'registration/userpage.html')
	else:
		print("is it first?")
		form = UserCreationForm()
		context = {'form' : form}
		return render(request, 'registration/register.html', context)

def userpage(request):
	print("Entering userpage------------")
	return render(request, 'registration/userpage.html')

def video_upload(request):
	print("Entering video upload -------------")
	if request.method == 'POST':
		form = VideoForm(request.POST, request.FILES)
		print("FORM: ",form)
		if form.is_valid():
			form.save()
			video_obj = Video(VideoPath=request.FILES['VideoPath'])
			print("Video Obj: ",video_obj)
			print("Username: ", request.user.get_username())
			video_obj.save()
			c = {}
			c['name'] = request.FILES['VideoPath']
			return render(request, 'registration/thanks.html',c)
		else:
			print("Invalid form====")
			form = VideoForm()
		return render(request, 'registration/userpage.html', {'form':form} )








