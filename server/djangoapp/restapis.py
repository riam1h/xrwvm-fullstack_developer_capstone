# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv
import urllib.parse  # For URL encoding

# Load environment variables
load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# Define the function for GET requests
def get_request(endpoint, **kwargs): 
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += key + "=" + value + "&"  # Construct query parameters
    request_url = backend_url + endpoint + "?" + params.rstrip("&")  # Ensure no trailing "&"
    print("GET from {} ".format(request_url))
    try:
        # Call GET method of requests library with URL and parameters
        response = requests.get(request_url)
        response.raise_for_status()  # Raise an error for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle exceptions related to network or HTTP
        print(f"Network exception occurred: {e}")
        return None

def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")

# Define the function to analyze review sentiments
def analyze_review_sentiments(text):
    # Ensure the text is URL-encoded to handle special characters
    encoded_text = urllib.parse.quote(text)
    request_url = f"{sentiment_analyzer_url}analyze/{encoded_text}"
    print(f"Making GET request to: {request_url}")

    try:
        # Send the GET request to the sentiment analyzer service
        response = requests.get(request_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as err:
        # Handle network-related exceptions
        print(f"An error occurred: {err}")
        return None
    except Exception as err:
        # Handle other unexpected exceptions
        print(f"Unexpected error: {err}, Type: {type(err)}")
        return None
