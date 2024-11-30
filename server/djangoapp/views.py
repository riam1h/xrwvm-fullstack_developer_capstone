from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
import logging
import json 
 
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Login view to handle sign-in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            # Ensure required fields are provided
            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)

            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)


# Logout view to handle sign-out request
@csrf_exempt
def logout_request(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"userName": "", "status": "Logged out"})
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)


# Registration view to handle sign-up request
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            # Parse the request body as JSON
            data = json.loads(request.body)
            required_fields = ["userName", "password", "firstName", "lastName", "email"]
            
            # Validate required fields
            if not all(field in data for field in required_fields):
                return JsonResponse({"error": "All fields are required"}, status=400)

            username = data['userName']
            password = data['password']
            first_name = data['firstName']
            last_name = data['lastName']
            email = data['email']

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=409)

            # Create a new user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            # Automatically log in the user after registration
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)
