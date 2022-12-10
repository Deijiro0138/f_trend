import tweepy
from tweepy import cursor 
import collections
import other_function
from datetime import timedelta
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import *
import MeCab

def getApiInstance(CONSUMER_KEY,COMSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET):
    global api,consumer_key,consumer_secret,access_token,access_token_secret
    consumer_key = CONSUMER_KEY
    consumer_secret = COMSUMER_SECRET
    access_token = ACCESS_TOKEN
    access_token_secret = ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    
    return api

def get_follower_information(user):
    followerIDs = api.followers_ids(user)
    followerDatas = []
    for followerID in followerIDs:
        followerData = {}
        data = api.get_user(followerID)
        followerData["Name"] = data.name
        followerData["Follow"] = data.friends_count
        followerData["Description"] = data.description
        followerData["TweetCount"] = data.statuses_count
        followerDatas.append(followerData)

    return followerDatas


def get_followers(user):
    #参考:https://teratail.com/questions/303666

    followers_ids = tweepy.Cursor(api.followers_ids, id = user, cursor = -1).items()
    followers_name_list = []

    try:
        for follower_id in followers_ids:
            followers_name_list.append(api.get_user(follower_id).screen_name)
        return followers_name_list
    except tweepy.TweepError as e:
        print(e.reason)


def get_friend(user):
    #参考:https://talosta.hatenablog.com/entry/twitter-auto-remove

    friend_ids = tweepy.Cursor(api.friends_ids, id = user, cursor = -1).items()
    friend_name_list = []
    try:
        for friend_id in friend_ids:
            friend_name_list.append(api.get_user(friend_id).screen_name,)
        return friend_name_list
    except tweepy.TweepError as e:
        if e.reason == "Not authorized.":
            print("ツイートを取得する権限がありません")
        elif e.reason == "Rate limit exceeded.":
            print("処理に15分以上かかります。")
        else:
            print("原因不明なエラーが発生しています。")


def get_tweet(user):
    #参照:https://www.pytry3g.com/entry/python-twitter-timeline
    tweet_datas = []
    try:
        results = api.user_timeline(screen_name=user,count=10)
        for result in results:
            if  result.text[0] == "@" or result.text[0:2] == "RT":
                continue
            #tweet_text = other_function.delete_emoji(result.text).strip()
            tweet_text = result.text
            tweet_datas.append(tweet_text)


    except tweepy.TweepError as e:
        print(e)
        if e.reason == "Not authorized.":
            print("@"+str(user)+"のツイートを取得する権限がありません")
        elif e.reason == "Rate limit exceeded.":
            print("処理に15分以上かかります。")
        else:
            print("原因不明なエラーが発生しています。")
        return []

    else:
        return tweet_datas    
    
def user_trend(tweet,trend_dict):
    #参照:https://mocobeta.github.io/janome/

    t = Tokenizer()
    
    for token in t.tokenize(tweet):
        if (token.part_of_speech.split(',')[0] == '名詞') & (token.part_of_speech.split(',')[1] in ['一般', '固有名詞', 'サ変接続', '形容動詞語幹']):
            word = token.surface
            if word in trend_dict:
                trend_dict[word] += 1
            else:
                trend_dict[word] = 1

    return trend_dict

def tweet(content):
    api.update_status(content)

def tweet_image(content,img):
    api.update_with_media(status=content,filename="")

def old_user_trend(tweet,trend_dict):
    token_filters = [POSKeepFilter(['名詞']),TokenCountFilter()]
    analyzation = Analyzer(token_filters=token_filters)
    for k,v in analyzation.analyze(tweet):
        if k in trend_dict:
            trend_dict[k] += v
        else:
            trend_dict[k] = v
            
    return trend_dict


def trend(tweet,trend_dict):
    #参考:https://mana.bi/wiki.cgi?page=%B7%C1%C2%D6%C1%C7%B2%F2%C0%CF%B4%EFMeCab#p6
    #参考:https://hibiki-press.tech/python/mecab/5153

    m = MeCab.Tagger('')
    token_list = m.parseToNode(tweet)
    #characters = ['質問箱','募集中','‼',';','&','"','-','1','2','3','4','5','6','7','8','9','0','RT','#','https','/','…','_','.',',','@',':','、','。','(','〜',')','!','！','？','?','「','」','。','、','・']

    while token_list:
        words = token_list.feature.split(",")
        if words[1] == "固有名詞":
            word = token_list.surface

            if word in trend_dict:
                trend_dict[word] += 1
            else:
                trend_dict[word] = 1
        
        token_list = token_list.next

    return trend_dict







