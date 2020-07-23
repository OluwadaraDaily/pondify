from django.http import HttpResponse, Http404
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import requests
import json

# Create your views here.

def register(request):
	if request.method == "POST":
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		email = request.POST["email"]
		username = request.POST["username"]
		password = request.POST["password"]
		
		User.objects.create_user(first_name = first_name, last_name = last_name, 
			email = email, username = username, password = password)
	
		context = {
			'first_name': first_name
		}
		return redirect("/login")

	return render(request, "pond/register.html")

def signin(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username = username, password = password)

		context = {
			'user': user
		}

		if user is not None:
			auth_login(request, user)
			return redirect("/", context)
		else:
			return redirect("/login")

	return render(request, "pond/login.html")

# @login_required(login_url='/login')
def index(request):
	if not request.user.is_authenticated:
		return redirect("login")

	user = request.user.username
	ponds = Pond.objects.filter (owner = request.user)
	context = {
		'user': user,
		'ponds': ponds
	}
	return render(request, "pond/index.html", context)


# @login_required(login_url='/login')
def add_pond(request):
	return render(request, "pond/add_pond.html")

# @login_required(login_url='/login')
def each_pond(request, pond_id):
	response = requests.get(f"https://api.thingspeak.com/channels/{pond_id}/feeds.json",
		params={"api_key": "61KHV0MWBSNBE4G2", "results": "1"}).json()

	context = {
		'response': response
	}

	return render(request, "pond/each_pond.html", context)

def signout(request):
	auth_logout(request)
	return redirect("login")