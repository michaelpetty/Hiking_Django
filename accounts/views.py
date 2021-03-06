from django.shortcuts import render, redirect

# IMPORT DJANGO AUTH
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# IMPORT DJANGO USER MODEL
from django.contrib.auth.models import User
from .forms import ProfileForm
from .models import Profile
from hike.models import Hike, Comments, HikeGroup

# Create your views here.


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check if username exists
            if User.objects.filter(username=username).exists():
                return render(request, 'accounts/register.html', {'error': 'That username has already been registered. Please try a different username'})
            else:
                # Check if email exists
                if User.objects.filter(email=email).exists():
                    return render(request, 'accounts/register.html', {'error': 'That email has already been registered'})
                else:
                    # Register User
                    user = User.objects.create_user(
                        username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    if user is not None:
                        auth.login(request, user)
                        return redirect('profile_create')
        else:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        # profile = Profile.objects.get(user=user.pk)
        if user is not None:
            auth.login(request, user)
            return redirect('landing')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid Credentials...'})

    else:
        return render(request, 'accounts/login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('landing')


@login_required
def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('landing')
    else:
        form = ProfileForm()
    return render(request, 'accounts/profile_form.html', {'form': form})


@login_required
def profile(request, user_id):
    profile = Profile.objects.get(user=user_id)
    if request.user.is_authenticated:
        user = request.user
        hikes = Hike.objects.filter(profile=profile.pk)
        comments = Comments.objects.filter(profile=profile.pk)
        hike_groups = HikeGroup.objects.filter(profile=profile.pk)
    return render(request, 'accounts/profile.html', {'profile': profile,'hikes':hikes, 'comments': comments, 'hike_groups': hike_groups, 'user': user})


@login_required
def profile_edit(request, user_id):
    profile = Profile.objects.get(user=user_id)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            return redirect('profile', user_id=user_id)
    else:
        form = ProfileForm(instance=profile)
        return render(request, 'accounts/profile_form.html', {'form':form})