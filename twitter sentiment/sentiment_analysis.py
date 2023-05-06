import tweepy
import textblob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import datetime as dt

all_keys = open("keys.txt", "r").read().splitlines()

api_key = all_keys[0]
api_key_secret = all_keys[1]
aceess_token = all_keys[2]
aceess_token_secret = all_keys[3]
bearer_token = all_keys[4]

authenticator = tweepy.OAuthHandler(api_key, api_key_secret)
authenticator.set_access_token(aceess_token, aceess_token_secret)

api = tweepy.API(authenticator, wait_on_rate_limit=True)
crypto = "Bitcoin"

search = f"#{crypto} -is:retweet"
start  = dt.datetime(2022, 11, 6)
end = dt.datetime(2022, 11, 13)
tweet_cursor = tweepy.Cursor(api.search_tweets, q = search, lang = "en", tweet_mode="extended", until = end).items(10)
a = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_key_secret, access_token=aceess_token, access_token_secret=aceess_token_secret)
tweet_cursor = a.search_recent_tweets(query=search, max_results = 100, start_time = start, end_time = end)
tweets = []
for info in tweet_cursor[0]:
    tweets.append(info.text)
#print(tweets)
# for i in tweet_cursor:
#     print(i)
#     print(len(i))
#     print("下一条")

tweets_df = pd.DataFrame(tweets, columns=["Tweets"])

#Data clean
for _,row in tweets_df.iterrows():
    row["Tweets"] = re.sub("http\S+", "", row["Tweets"])
    row["Tweets"] = re.sub("#\S+", "", row["Tweets"])
    row["Tweets"] = re.sub("@\S+", "", row["Tweets"])
    row["Tweets"] = re.sub("\\n", "", row["Tweets"])

tweets_df["Polarity"] = tweets_df["Tweets"].map(lambda tweet: textblob.TextBlob(tweet).sentiment.polarity)
tweets_df["Result"] = tweets_df["Polarity"].map(lambda pol: "Positive" if pol>0 else "Negative")

positive = tweets_df[tweets_df.Result == "Positive"].count()["Tweets"]
negative = tweets_df[tweets_df.Result == "Negative"].count()["Tweets"]

plt.pie([negative, positive], colors=["red", "#96f97b"],labels=["Bearish", "Bullish"], explode=(0.1, 0), autopct="%.2f%%")
plt.legend(loc = "upper right", fontsize = 10)
plt.title("Market Sentiment", fontsize = 15)
plt.show()

