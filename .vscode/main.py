import tweepy_module,api_module
import os,sys,time




if __name__ == "__main__":
  start_time = time.time()
  count = 0
  keys = {
  'CONSUMER_KEY' : "5bAhIZrD13LvE43B4obtXYEgm",
  'COMSUMER_SECRET' : "BH5txoB2Rx3F7JBJCWJMxg2mx8V2zIJb8rQLBTSUH7R4i77v3I",
  'ACCESS_TOKEN' : "1250271488021688320-QdrGx3KtO1bIl3Zsbshnigdbd45NxO",
  'ACCESS_TOKEN_SECRET' : "kUHzESKXi8n5fAjiA38XDx6kIEivjuVJq9uDF87X5lEQh"
  }
  
  user = "JsUniv"
  api = tweepy_module.getApiInstance(**keys)
  followers_list = tweepy_module.get_followers(user)
  trend_dict = {}

  for follower in followers_list:
    tweets = tweepy_module.get_tweet(follower)
    if len(tweets) != 0:
      for tweet in tweets:
         trend_dict = tweepy_module.trend(tweet,trend_dict)

  trend_dict = sorted(trend_dict.items(),key=lambda x:x[1],reverse=True)

  for word,i in trend_dict:
    count += 1
    if count == 30:
      break
    print('%s : %d'%(word,i))
  
  alart = time.time() - start_time
  print("処理に"+str(alart)+"秒かかりました。")


  





