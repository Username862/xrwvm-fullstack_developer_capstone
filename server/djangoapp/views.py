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
from .restapis import get_request, analyze_review_sentiments, post_review

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

def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200, "dealers":dealerships})

def get_dealer_reviews(request,dealer_id):
    if dealer_id:
        reviews = get_request("/fetchReviews/" + str(dealer_id))
        for review in reviews:
            res = analyze_review_sentiments(review['review'])
            print(res)
            review['sentiment'] = res['sentiment']
        return JsonResponse({"status":200, "reviews": reviews})
    return JsonResponse({"status":400, "message": "Bad request"})

def get_dealer_details(request, dealer_id):
    if dealer_id:
        dealership = get_request("/fetchDealer/" + str(dealer_id))
        return JsonResponse({"status":200, "dealer":dealership})
    return JsonResponse({"status":400, "message": "Bad request"})
    
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            res = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    return JsonResponse({"status":403,"message":"Unauthorized"})

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