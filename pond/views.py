from django.http import HttpResponse, Http404
from .models import Pond
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import requests
import json

# Create your views here.

def register(request):
	# When form is submitted
	if request.method == "POST":
		first_name = request.POST["first_name"]
		last_name = request.POST["last_name"]
		email = request.POST["email"]
		username = request.POST["username"]
		password = request.POST["password"]

		user = authenticate(request, username = username, password = password)

		# Check if the user does not exist. If not, go ahead to the login page
		if user is None:
			User.objects.create_user(first_name = first_name, last_name = last_name, 
			email = email, username = username, password = password)
	
			context = {
				'first_name': first_name
			}
			message = "Congratulations. Registration Successful! You can now Login!"
			messages.add_message(request, messages.SUCCESS, message)
			return redirect("/login")
		# If user exists already, return back to the Registration page
		else:
			message = "Registration was not successful! Try different parameters!"
			messages.add_message(request, messages.ERROR, message)
			return redirect("/register")

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
			message = "Invalid Login Parameters! Try Again!"
			messages.add_message(request, messages.ERROR, message)
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


def add_pond(request):
	if request.method == "POST":
		#get data from the front end
		pond_name = request.POST["pond_name"]
		channel_id = request.POST["channel_id"]
		owner = request.user
		
		#check DB for similar entries
		check = Pond.check_pond(pond_name, channel_id)
		
		if (check):
		
			single_pond = Pond.objects.create(owner = owner, pond_name = pond_name, channel_id = channel_id)	
		
			
			context = {
				"pond": single_pond,
				"message": "Pond added successfully"
			}

			return render(request, "pond/success.html", context)
		
		else:
			context = {
				"message": "Channel or Pond name already exists. Try again!"
			}
			return render(request, "pond/error.html", context)
	
	return render(request, "pond/add_pond.html")

def each_pond(request, pond_id):
	response = requests.get(f"https://api.thingspeak.com/channels/{pond_id}/feeds.json",
		params={"api_key": "Z7POUDWMQBPRKQU1", "results": "1"}).json()
	# if(response.feeds.0.field4 == 0)

	context = {
		'response': response,
		'pond_id': pond_id
	}

	return render(request, "pond/each_pond.html", context)

def delete_pond(request, pond_id):
	pond = Pond.objects.get(id = pond_id)
	pond.delete()

	return redirect("/")

def about(request):
	return render(request, "pond/about.html")

def signout(request):
	auth_logout(request)
	return redirect("login")