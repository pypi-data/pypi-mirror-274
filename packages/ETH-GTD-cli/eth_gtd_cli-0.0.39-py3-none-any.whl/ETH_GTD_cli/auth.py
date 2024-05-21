import json
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
import typer

app = typer.Typer()
from .consts import AUTHORIZATION_URL, REDIRECT_URI, SCOPE, API_CLI_CALLBACK_URL, API_URL


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/cli/callback'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            self.server.auth_tokens = {
                'access_token': params.get('access_token')[0],
                'refresh_token': params.get('refresh_token')[0]
            }
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b'Authentication successful. You can close this window.')
            return

def get_auth_tokens():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, OAuthCallbackHandler)
    httpd.handle_request()
    return httpd.auth_tokens

@app.command()
def login():
    print("Opening browser for authentication...")
    webbrowser.open(API_URL + "/auth/google")

    print("Waiting for authentication to complete...")
    auth_tokens = get_auth_tokens()

    if not auth_tokens:
        print("Failed to get authentication tokens.")
        return

    with open('tokens.json', 'w') as token_file:
        json.dump(auth_tokens, token_file)

    print("Authentication complete. Tokens saved to tokens.json.")

@app.command()
def fetch_data():
    try:
        with open('tokens.json', 'r') as token_file:
            token_data = json.load(token_file)
    except FileNotFoundError:
        print("Token file not found. Please run 'login' command first.")
        return

    headers = {'Authorization': f"Bearer {token_data['access_token']}"}
    response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)

    if response.status_code == 401:
        print("Token expired or invalid. Please run 'login' command again.")
    else:
        print("Data fetched successfully!")
        print(response.json())
