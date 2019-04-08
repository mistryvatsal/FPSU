import tweepy
from textblob import TextBlob

consumer_key = "fX5HSbJqe61Ybc4g5PRMlhHRp"
consumer_secret_key = "L4iBCxGgLaF7s7bo7I7RfkedNQ2u1ReoAZxoId9PJqV2LKAGyE"

access_token = "2993243198-dpmOLqDpFbA57W4Eup2tlCJHXBlC6bGliDV7Cz2"
access_token_secret = "OKfCoJ6HtTAmcLIxfRAmkghJQUXkzldTIKByfrKMC934u"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#public_tweets = api.search("Trump")
#for tweet in public_tweets:
#    print(tweet.text)
#    analysis = TextBlob(tweet.text)
#    print(analysis.sentiment)
#    print("\n")

analysis = TextBlob("Never.")
print analysis.sentiment.polarity
