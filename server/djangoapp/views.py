from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate

from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Handle sign out request
def logout_user(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    firstName = data['firstName']
    lastName = data['lastName']
    email = data['email']
    usernameExist = False
    try: # check if user already exists
        User.objects.get(username=username)
        usernameExist = True
    except:
        logger.debug(f"{username} is the new user")
    
    if not usernameExist:   # create user & login
        user = User.objects.create_user(username=username, first_name=firstName, last_name=lastName, email=email, password=password)
        login(request, user)
        data = {"username": username, "status": "Authenticated"}
    else:
        data = {"username": username, "status": "Already registered"}
    return JsonResponse(data)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.all()
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})