from django.shortcuts import render, redirect
from .models import Hike, Comments, HikeGroup
from django.contrib.auth.decorators import login_required
from .forms import HikeForm

# Create your views here.
# HIKE VIEWS

# landing page.
# Missing functionality - hike list and google calender
def landing(request):
  return render(request, 'hike/landing.html')

# show user details about a selected hike.
# Missing functionality - selected hike with map)
def hike_detail(request):
  return render(request, 'hike/hike_detail.html')

#add a new hike
# create a form to add a new hike

@login_required
def hike_new(request):
  if request.method == 'POST':
    form = HikeForm(request.POST)
    if form.is_valid():
      hike = form.save(commit=False)
      hike.user = request.user
      hike.save()
      return redirect('hike_detail', pk=hike.pk)
  else:
      form = HikeForm()
  return render(request, 'hike/hike_form.html', {'form': form})

# show all hikes on a calendar
def hike_calendar(request):
    return render(request, 'hike/hike_calendar.html')

# USER / PROFILE VIEWS
