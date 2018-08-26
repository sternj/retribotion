import tweepy
import os
from tweepy import TweepError

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()
print(user.name)


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        uid = status.id_str
        try: 
            api.create_favorite(uid)
        except TweepError as e:
            print(e)
            print(status.text)
        print("Favorited {}".format(status.text))
    def on_error(self, status_code):
        print(status_code)
        if status_code == 139:
            return True
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)
stream.filter(track=['retribution', 'Retribution'])