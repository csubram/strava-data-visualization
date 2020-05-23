import requests
import webbrowser
import http.server
import socketserver
import threading
from authorization.auth_utils import *
from authorization.tcp_request_handler import TCPRequestHandler


DOMAIN = 'localhost'
PORT = 8000
CLIENT_INFO_FILE = 'authorization/client_info.json'
TOKENS_OUTPUT_FILE = 'authorization/access_tokens.json'


class AccessTokenHandler():

    def __init__(self):
        self.client_info = read_from_json_file_named(CLIENT_INFO_FILE)

    def _get_authorization_request_url(self, client_id):
        query = 'https://www.strava.com/oauth/authorize'
        params = {
            'client_id': self.client_info['client_id'],
            'redirect_uri': 'http://{0}:{1}'.format(DOMAIN, PORT),
            'response_type': 'code',
            'approval_prompt': 'auto',
            'scope': 'activity:read_all'
        }

        auth_request = requests.Request('GET', query, params=params).prepare()
        return auth_request.url

    def _open_web_browser_to_page(self, url):
        chrome_path = '/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path), 1)
        webbrowser.get('chrome').open(url)

    def _start_local_server(self):
        my_server = socketserver.TCPServer((DOMAIN, PORT), TCPRequestHandler)
        my_server.handle_request()

    def _request_to_refresh_token(self, refresh_token):
        query = 'https://www.strava.com/oauth/token'
        params = {
            'client_id': self.client_info['client_id'],
            'client_secret': self.client_info['client_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        response = requests.post(query, params=params)
        return response.json()

    def get_new_access_token(self):
        daemon_localhost_thread = threading.Thread(target=self._start_local_server)
        daemon_localhost_thread.start()

        auth_request_url = self._get_authorization_request_url(
            self.client_info['client_id'])
        self._open_web_browser_to_page(auth_request_url)

    def refresh_existing_access_token(self):
        access_token_info = read_from_json_file_named(TOKENS_OUTPUT_FILE)
        auth_response = self._request_to_refresh_token(access_token_info['refresh_token'])
        write_data_to_json_file(
            data=auth_response, filename=TOKENS_OUTPUT_FILE)
