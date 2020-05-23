from authorization.access_token_handler import AccessTokenHandler

if __name__ == '__main__':
    token_handler = AccessTokenHandler()
    token_handler.get_new_access_token()
