from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from booking.models import Book, Room, Guest, Hostel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from booking.forms import UserForm, LoginForm, BookingForm, SignUpForm
from booking.serializers import HostelSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

class HostelViewSet(viewsets.ViewSet):
    """
    API endpoint that allows hostels to be viewed
    """
    http_method_names = ['get']
    queryset = Hostel.objects.all()

    @silk_profile(name='Hostels list')
    def list(self, request):
        name = request.GET.get('name')
        qs = self.queryset
        if name:
            qs = qs.filter(name__icontains=name)
        
        serializer = HostelSerializer(qs, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)



def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            Guest.objects.create(user=new_user)
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Account created successfully')
                    return redirect('login/edit/')
                else:
                    messages.error(request, 'Your account is not active')
                    return redirect('register/')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('register/')
    else:
        form = UserForm()
        return render(request, 'registration/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Logged in successfully')
                    return redirect('home/')
                else:
                    messages.error(request, 'Your account is not active')
                    return redirect('login/')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login/')
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

def logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login/')

def hostel_detail_view(request):
    pass

def edit(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, instance=request.user.guest)
        if form.is_valid():
            form.save()
            return redirect('home/')
    else:
        form = SignUpForm(instance=request.user.guest)
        return render(request, 'edit.html', {'form': form})

def select(request):
    if request.user.guest.room:
        room_id_old = request.user.guest.room.id
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=request.user.guest)
        if form.is_valid():
            if request.user.guest.room_id:
                request.user.guest.room_alloted = True
                room_id_after = request.user.guest.room_id
                room = Room.objects.get(id=room_id_after)
                room.vacant = False
                room.save()
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            else:
                request.user.guest.room_alloted = False

                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            form.save()
            return redirect('home/')
    else:
        form = BookingForm(instance=request.user.guest)
        guest_gender = request.user.guest.gender
        guest_book = request.user.guest.book
        guest_room_type = request.user.guest.book.room_type
        hostel = Hostel.objects.filter(gender=guest_gender, book=guest_book)
        x = Room.objects.none()
        if guest_room_type == 'B':
            for i in range(len(hostel)):
                h_id = hostel[i].id
                a = Room.objects.filter(
                    hostel_id=h_id,
                    room_type=['S','B'],
                    vacant=True
                )
                x = x | a
        else:
            for i in range(len(hostel)):
                h_id = hostel[i].id
                a = Room.objects.filter(
                    hostel_id=h_id,
                    room_type=guest_room_type,
                    vacant=True
                )
                x = x | a
        form.fields['room'].queryset = x
        return render(request, 'select.html', {'form': form})

def home(request):
    return render(request, 'home.html')

