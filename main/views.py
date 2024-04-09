from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import Announcement
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, AnnouncementForm, UpdateAnnouncementForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotAllowed, HttpResponse
import json
from .models import UserProfile

@login_required
def get_user_announcement_list(request):
    user_announcements = Announcement.objects.filter(user_profile=request.user)
    return render(request, 'announcement/list_of_user_announcements.html', {'announcements': user_announcements})


def get_public_announcements(request):
    # Фільтруємо анонси за полем access
    announcements = Announcement.objects.filter(access='public')
    return render(request, 'announcement/list_of_public_announcements.html', {'announcements': announcements})

@login_required
def get_local_announcements(request):
    location = request.user.location
    # Fetch local announcements for the user's location
    announcements = Announcement.objects.filter(access='local', location__iexact=location)

    return render(request, 'announcement/list_of_local_announcements.html', {'announcements': announcements, 'location': location})
  

@csrf_exempt
def get_announcement_by_id(request, id):
    announcement = Announcement.objects.get(id=id)

    # Перевіряємо доступ до анонсу
    if announcement.access == 'public' or (request.user.is_authenticated and request.user.location == announcement.location):
        return render(request, 'announcement/announcement.html', {'announcement': announcement})
    else:
        return render(request, '404.html')

@csrf_exempt
@login_required(login_url='login')  # Add this decorator to ensure the user is logged in
def create_announcement(request):

    if request.method == 'POST':
        data = json.loads(request.body)

        subject = data.get('subject')
        title = data.get('title')
        content = data.get('content')
        access = data.get('access')

        if request.user.is_authenticated:
            user_location = request.user.location
        else:
            user_location = None
        data1 = Announcement.objects.create(subject=subject,title=title,content=content,access=access,location=user_location, user_profile = request.user )
        data1.save()
        return JsonResponse({'status': 'success'})
    else:
        form = AnnouncementForm()

    return render(request, 'announcement/create_announcement.html', {'form': form})


@login_required
def update_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id, user_profile=request.user)

    if request.method == 'POST':
        form = UpdateAnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('/announcements/user')
    else:
        form = UpdateAnnouncementForm(instance=announcement)

    return render(request, 'announcement/update_announcement.html', {'form': form, 'announcement': announcement})
    
@login_required 
def delete_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    announcement.delete()
    return redirect('/announcements/user')


def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        password1 = data.get('password1')
        password2 = data.get('password2')
        location = data.get('location')
        username = data.get('username')

        if password1 != password2:
            return JsonResponse({'success': False, 'message': 'Passwords do not match'}, status=400)

        if UserProfile.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username is already taken'}, status=400)
        
        user = UserProfile.objects.create_user(username=username,password=password1, location=location)
        user.save()

        return JsonResponse({'status': 'success'})
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def user_logout(request):
    logout(request)
    return redirect('home')  # Замініть 'home' на шлях, куди ви хочете перенаправити після виходу
