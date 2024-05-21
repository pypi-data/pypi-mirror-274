import json
import requests

keyToken = ""

def login(UserName=None, Password=None):
    """
    Logs the user into SciServer.
    """
    loginURL = "https://apps.sciserver.org/login-portal/keystone/v3/tokens?TaskName=SciScript-Python.Authentication.Login"
    authJson = {"auth":{"identity":{"password":{"user":{"name":UserName,"password":Password}}}}}
    data = json.dumps(authJson).encode()

    postResponse = requests.post(loginURL,data=data,headers={'Content-Type': "application/json"})
    if postResponse.status_code != 200:
        raise Exception("Http Response from the Authentication API returned status code " + str(postResponse.status_code) + ":\n" + postResponse.content.decode());
    global keyToken 
    keyToken  = postResponse.headers['X-Subject-Token']
    return keyToken 

