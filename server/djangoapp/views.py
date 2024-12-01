from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
from .restapis import get_request, analyze_review_sentiments, post_review
from .models import CarMake, CarModel
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_request` view to handle sign-in requests
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            # Parse JSON request data
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            # Attempt to authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                # If user is valid, log them in
                login(request, user)
                response_data = {"userName": username, "status": "Authenticated"}
            else:
                response_data = {"userName": username, "status": "Authentication Failed"}
        except Exception as e:
            logger.error(f"Error during login: {e}")
            response_data = {"error": "Invalid request or server error"}
        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({"error": "GET method not allowed"}, status=405)

# Create a `logout_request` view to handle sign-out requests
@csrf_exempt
def logout_request(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"userName": "", "status": "Logged out"}, status=200)
    else:
        return JsonResponse({"error": "GET method not allowed"}, status=405)

# Create a `registration` view to handle sign-up requests
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            # Parse JSON request data
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            email = data.get('email')

            # Ensure username and password are provided
            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "User already exists"}, status=400)

            # Create and save the new user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return JsonResponse({"userName": username, "status": "Registration successful"}, status=201)
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return JsonResponse({"error": "Invalid request or server error"}, status=500)
    else:
        return JsonResponse({"error": "GET method not allowed"}, status=405)

# Placeholder for `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})
    pass

# Placeholder for `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})    
        pass

# Placeholder for `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})
    pass

# Placeholder for `add_review` view to submit a review
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
    pass

# Function to get cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})
