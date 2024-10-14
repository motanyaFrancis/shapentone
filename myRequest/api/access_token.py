import requests
from django.conf import settings as config
from requests.auth import HTTPBasicAuth


def generate_access_token():
    consumer_key = config.MPESA_CONSUMER_KEY
    consumer_secret = config.MPESA_CONSUMER_SECRET
    api_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    try:
        r = requests.get(api_URL, auth=HTTPBasicAuth(
            consumer_key, consumer_secret))
        r.raise_for_status()
        json_response = r.json()
        my_access_token = json_response["access_token"]
        return my_access_token
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


access_token = generate_access_token()

if access_token:
    print(f"Access Token: {access_token}")
else:
    print("Failed to retrieve access token.")
