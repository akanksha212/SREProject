from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from summarize.models import *
from summarize.forms import SignUpForm
from summarize.forms import VideoForm


from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from summarize.tokens import account_activation_token
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import json
import urllib
from django.http import HttpResponseBadRequest, HttpResponse
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def homepage(request):
    return render(request, 'summarize/home.html')


def valitate_recaptcha(recaptcha_response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    return result


def mail_user(user, current_site):
    subject = 'Activate Your Account'
    message = render_to_string('summarize/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    # send_mail(subject, message, sender_email, recipient_list)
    user.email_user(subject, message)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            result = valitate_recaptcha(request.POST.get('g-recaptcha-response'))
            
            if result['success']:
                user = form.save()
                user.refresh_from_db()  # load the profile instance created by the signal
                user.profile.email = form.cleaned_data.get('email')
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_user(user, current_site)
                return render(request, 'summarize/account_activation_sent.html')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            
    else:   
        form = SignUpForm()
    return render(request, 'summarize/signup.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, 'summarize/home.html')
    else:
        return render(request, 'summarize/account_activation_invalid.html')



def account_activation_sent(request):
    return render(request, 'summarize/account_activation_sent.html')


@login_required
def video_new(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.UserID = request.user
            video.save()
            return redirect('video_detail', pk=video.pk)
    else:
        form = VideoForm()
    return render(request, 'summarize/video_new.html', {'form':form} )


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    print(video)
    return render(request, 'summarize/video_detail.html', {'video' : video})

@login_required
def video_list(request):
    videos = Video.objects.filter(UserID = request.user)
    paginator = Paginator(videos, 5)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request, 'summarize/video_list.html', {'videos': videos})