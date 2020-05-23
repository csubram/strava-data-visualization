import requests
import webbrowser
import http.server
import socketserver
import os
import threading
import json

DOMAIN = 'localhost'
PORT = 8000
CLIENT_INFO_FILE = 'client_info.json'
TOKENS_OUTPUT_FILE = 'access_tokens.json'


class AccessTokenHandler():

    def __init__(self):
        self.client_info = self._get_client_info()

    def _get_client_info(self):
        with open(CLIENT_INFO_FILE, 'r') as in_file:
            client_info = json.load(in_file)

        return client_info

    def _get_authorization_request_url(self, client_id):
        query = 'https://www.strava.com/oauth/authorize'

        auth_request = requests.Request(
            'GET',
            query,
            params={
                'client_id': int(client_id),
                'redirect_uri': 'http://{0}:{1}'.format(DOMAIN, PORT),
                'response_type': 'code',
                'approval_prompt': 'auto',
                'scope': 'activity:read_all'
            }
        ).prepare()

        return auth_request.url

    def _open_web_browser_to_page(self, url):
        chrome_path = '/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path), 1)
        webbrowser.get('chrome').open(url)

    def start_local_server(self):
        my_server = socketserver.TCPServer((DOMAIN, PORT), TCPRequestHandler)
        my_server.handle_request()

    def get_new_access_token(self):
        daemon_localhost_thread = threading.Thread(target=self.start_local_server)
        daemon_localhost_thread.start()

        auth_request_url = self._get_authorization_request_url(
            self.client_info['client_id'])
        self._open_web_browser_to_page(auth_request_url)


class TCPRequestHandler(socketserver.StreamRequestHandler):

    def _get_client_info(self):
        with open(CLIENT_INFO_FILE, 'r') as in_file:
            client_info = json.load(in_file)

        return client_info

    def _get_auth_code_from_msg(self, msg):
        auth_code_query_parameter = msg.decode().split('&')[1]
        auth_code = auth_code_query_parameter.split('=')[1]
        return auth_code

    def _post_authorization_code(self, client_info, auth_code):
        query = 'https://www.strava.com/oauth/token'
        params = {
            'client_id': int(client_info['client_id']),
            'client_secret': client_info['client_secret'],
            'code': auth_code,
            'grant_type': 'authorization_code'
        }

        response = requests.post(query, params=params)
        return response.json()

    def _write_access_tokens(self, authorization_response):
        with open(TOKENS_OUTPUT_FILE, 'w+') as out_file:
            out_file.write(json.dumps(authorization_response, indent=2))

    def handle(self):
        msg = self.rfile.readline().strip()
        authorization_code = self._get_auth_code_from_msg(msg)
        client_info = self._get_client_info()

        authorization_response = self._post_authorization_code(
            client_info, authorization_code)
        self._write_access_tokens(authorization_response)


if __name__ == '__main__':
    ath = AccessTokenHandler()
    ath.get_new_access_token()
