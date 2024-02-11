import base64
import hashlib
import os
import re
import redis
import json
import requests
from requests.auth import AuthBase, HTTPBasicAuth
from requests_oauthlib import OAuth2Session, TokenUpdated
from flask import Flask, request, redirect, session, url_for, render_template
import time

r = redis.from_url(os.environ.get("REDIS_URL"))

app = Flask(__name__)
app.secret_key = os.urandom(50)

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
redirect_uri = os.environ.get("REDIRECT_URI")

scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

def fetch_data_with_retry(url, params=None, max_retries=3, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, params=params, verify=False)
            response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
            if response.text.strip():  # Check if response is not empty
                return response.json()  # Return JSON response
            else:
                print("Empty response received. Retrying...")
                retries += 1
                time.sleep(retry_delay)  # Wait before retrying
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            retries += 1
            time.sleep(retry_delay)  # Wait before retrying
    print(f"Max retries reached. Unable to fetch data from {url}.")
    return None

def make_token():
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

def parse_quote():
    url = "https://api.quotable.io/quotes/random"
    params = {'maxLength': 260}
    response_raw = fetch_data_with_retry(url, params=params)
    response = [response_raw[0]["content"], response_raw[0]["author"]]
    return response



def post_tweet(payload, token):
    print("Tweeting!")
    return requests.request(
        "POST",
        "https://api.twitter.com/2/tweets",
        json=payload,
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json",
            },
        )

def post_image(author, token):
    print("Uploading Image!")
    response = requests.request(
        "POST",
        "https://upload.twitter.com/1.1/media/upload.json?",
        headers={
            "Authorization": "Bearer {}".format(token["access_token"]),
        },
        files={
            "media": open(f'dataset/{author}/Image_1.jpg', 'rb')
        },
        params={
            "media_category": "tweet_image",
        }
    )
    print(response.status_code)
    return response.json()

@app.route("/")
def demo():
    global x
    x = make_token()
    authorization_url, state = x.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
        )
    session["oauth_state"] = state
    return redirect(authorization_url)

@app.route("/oauth/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    token  = x.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code_verifier=code_verifier,
        code=code,
        )
    st_token = '"{}"'.format(token)
    j_token = json.loads(st_token)
    r.set("token", j_token)
    quote = parse_quote()
    payload = {"text": "{}\n- {}".format(quote[0], quote[1])}
    response = post_tweet(payload, token).json()
    return response

#if __name__ == "__main__":
#    app.run()
