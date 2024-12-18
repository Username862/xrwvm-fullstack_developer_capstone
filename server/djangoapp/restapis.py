import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for, value in kwargs.items():
            params += key + "=" + value + "&"
    request_url = backend_url + endpoint + "?" + params

    print(f"GET from {request_url}")
    try:
        res = requests.get(request_url)
        return res.json()
    except:
        print("Network exception occurred")

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        res = requests.get(request_url)
        return res.json()
    except:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occured")

def post_review(data_dict):
    req_url = backend_url + "/insert_review"
    try:
        res = requests.post(req_url, json=data_dict)
        print(res.json())
        return res.json()
    except:
        print("Network exception occurred")
