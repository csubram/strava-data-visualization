# strava-data-visualization

### Description
A tool to retrieve Strava data from one's profile and filter by activity type.

### Local setup

1. Create a developer account: https://www.strava.com/settings/api
2. Enable activity read access for your developer account. 
  - You can use curl or paste the first request into a browser, and read the "code" parameter from the response. 
  ```
  https://www.strava.com/oauth/authorize?
    client_id=<CLIENT_ID>&
    redirect_uri=<CALLBACK_DOMAIN>&
    response_type=code&
    scope=activity:read
  ```
  - The request above should return an authorization code. Use this authorization code to fill in the POST request below. Send this request, and read the "access_code" from that response.
    
  ```
  curl -X POST https://www.strava.com/oauth/token?
    client_id=<CLIENT_ID>&
    client_secret=<CLIENT_SECRET>&
    code=<AUTHORIZATION_CODE>&
    grant_type=authorization_code
  ```
3. Paste the access code found in the previous step into a file called "secrets.py" as follows:
  ```python
  access_token = 'code goes here'
  ```
  
4. Run the application from the command line:
  ```
  python3 activities_data_fetcher.py
  ```
