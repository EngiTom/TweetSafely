import requests
import os as os
import json
from dotenv import load_dotenv
load_dotenv()
# To set your enviornment variables in your terminal run the following line:
# set BEARER_TOKEN='AAAAAAAAAAAAAAAAAAAAAAwMjgEAAAAAPEIVIzJzJuYKAkoggyNGDBUm0qs%3DLxetgHVJs9tuMXwdYXm1YJV26sxfaN95XkWRaLhGqR2gzdci8W'
bearer_token = os.getenv("BEARER_TOKEN")
def create_url(user):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames="+str(user)
    user_fields = "user.fields=created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r
def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    # print(response.status_code)
    if response.status_code != 200:
        # raise Exception(
        #     "Request returned an error: {} {}".format(
        #         response.status_code, response.text
        #     )
        # )
        return "ERROR"
    return response.json()
def finalFunc(nameOfUser):
    url = create_url(nameOfUser)
    json_response = connect_to_endpoint(url)
    #jsonResp=json.dumps(json_response, indent=4, sort_keys=True)
    y = json_response
    try:
        d = y['data']
    except:
        return "ERROR"

    zer = d[0]
    ret = zer['id']
    return ret