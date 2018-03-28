# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'first_app/index.html')
def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(index)
    else:
        new_user = User.objects.create(
            name = request.POST['name'], 
            alias = request.POST['alias'], 
            email = request.POST['email'], 
            password = request.POST['password'], 
            conf_password = request.POST['confirm']
        )
        request.session['user_id'] = new_user.id
        return redirect(success)
        
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(index)
    else:
        request.session['user_id'] = User.objects.get(alias = request.POST['alias']).id
        return redirect(success)

def logout(request):
    request.session.clear()
    return redirect('/main')

def success(request):
    if 'user_id' not in request.session:
        return redirect(index)
    else:
        context =  {
            'user': User.objects.get(id = request.session['user_id']),
            'all_trips': Trip.objects.all().exclude(joined_by = request.session['user_id']),
            'your_trips': Trip.objects.filter(joined_by = request.session['user_id'])
        }
        return render(request, 'first_app/success.html', context)

def add(request):
    return render(request, 'first_app/new.html')

def create(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(add)
    else:
        new_trip = Trip.objects.create(
            destination = request.POST['country'],
            description = request.POST['description'],
            start = request.POST['start'],
            end = request.POST['end'],
            created_by = User.objects.get(id = request.session['user_id'])
        )
        User.objects.get(id=request.session['user_id']).joined_trips.add(new_trip)
        return redirect(success)

def join(request, id):
   User.objects.get(id=request.session['user_id']).joined_trips.add(Trip.objects.get(id = id))
   return redirect(success)

def show(request, id):
    context = {
        'trip': Trip.objects.get(id=id),
        'all_joined_users': User.objects.all().filter(joined_trips = Trip.objects.get(id=id))
    }
    return render(request, 'first_app/show.html', context)