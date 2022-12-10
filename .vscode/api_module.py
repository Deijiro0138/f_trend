from requests_oauthlib import OAuth1Session
import json

def getApiInstance(CONSUMER_KEY,COMSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET):
    global api,consumer_key,consumer_secret,access_token,access_token_secret
    consumer_key = CONSUMER_KEY
    consumer_secret = COMSUMER_SECRET
    access_token = ACCESS_TOKEN
    access_token_secret = ACCESS_TOKEN_SECRET

    api = OAuth1Session(consumer_key,consumer_secret,access_token,access_token_secret)
    return api

def get_followers(user):
    Cursor = '-1'
    GetFollowersList = []
    url = 'https://api.twitter.com/1.1/followers/ids.json'
    while Cursor != '0':
        params = {
            'user_id' : user,
            'screen_name' : '',
            'cursor' : Cursor,
            'stringify_ids' : '',
            'count' : '5000'
        }
        GetFollowersIdsResponse = api.get(url,params = params)

        if GetFollowersIdsResponse.status_code == 200:
            GetFollowersIdsResult = json.loads(GetFollowersIdsResponse.text)
            GetFollowersList.extend(GetFollowersIdsResult['ids'])
            Cursor = GetFollowersIdsResult['next_cursor_str']
        else:
            print(GetFollowersIdsResponse)
    
    return GetFollowersList