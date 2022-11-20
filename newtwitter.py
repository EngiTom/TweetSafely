import requests
import os
import json
import userLookup

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

def create_url(username):
    # Replace with user ID below
    user_id = userLookup.finalFunc(username)
    if user_id == "ERROR":
        return "ERROR"
    #print(user_id)
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"max_results":99}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main(username):
    url = create_url(username)
    if url == 'ERROR':
        return "ERROR"
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    if json_response == "ERROR":
        return "ERROR"
    #print(type(json_response))
    listOfRecentTweets=[]
    for i in range(len(json_response['data'])):
        listOfRecentTweets.append(json_response["data"][i]['text'])
    return(listOfRecentTweets)