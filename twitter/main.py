# import modules
from keys import *
import pandas as pd
import tweepy
# from tweepy.streaming import StreamListener
import string

class SL(tweepy.Stream):

    def on_status(self, status):
        print(status.text)

# function to display data of each tweet
def printtweetdata(n, ith_tweet):
    print()
    print(f"Tweet {n}:")
    print(f"Username:{ith_tweet[0]}")
    print(f"Description:{ith_tweet[1]}")
    print(f"Location:{ith_tweet[2]}")
    print(f"Following Count:{ith_tweet[3]}")
    print(f"Follower Count:{ith_tweet[4]}")
    print(f"Total Tweets:{ith_tweet[5]}")
    print(f"Retweet Count:{ith_tweet[6]}")
    print(f"Tweet Text:{ith_tweet[7]}")
    print(f"Hashtags Used:{ith_tweet[8]}")


# function to perform data extraction
def scrape(words, numtweet):
    # Creating DataFrame using pandas
    db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                               'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags'])

    # We are using .Cursor() to search through twitter for the required tweets.
    # The number of tweets can be restricted using .items(number of tweets)
    tweets = tweepy.Cursor(api.search_tweets, q=words, count=5, lang="en").items(numtweet)

    # .Cursor() returns an iterable object. Each item in
    # the iterator has various attributes that you can access to
    # get information about each tweet
    list_tweets = [tweet for tweet in tweets]

    # Counter to maintain Tweet Count
    i = 1

    # we will iterate over each tweet in the list for extracting information about each tweet
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']

        # Retweets can be distinguished by a retweeted_status attribute,
        # in case it is an invalid reference, except block will be executed
        text = tweet.text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        # Here we are appending all the extracted information in the DataFrame
        ith_tweet = [username, description, location, following,
                     followers, totaltweets, retweetcount, text, hashtext]
        db.loc[len(db)] = ith_tweet

        # Function call to print tweet data on screen
        printtweetdata(i, ith_tweet)
        i = i + 1
    filename = 'scraped_tweets.csv'

    # we will save our database as a CSV file.
    # db.to_csv(filename)


if __name__ == '__main__':
    # Enter your own credentials obtained
    # from your developer account
    #consumer_key = "i8QkhVxn5Dk8oh4XQgNPwd27l"
    #consumer_secret = "AJnvvFcfHcKQ3bwFLw69cQdWb8EGcw2DQ6Yb6RkKKqitWUUUIE"
    # access_key = "1440726244102864904-H36HeQI7VU50qjdTRcvSnazHackPU0"
    # access_secret = "tS41RWtbpTYB5hbLQPCOdSY5gnruQm2w8QiFsew9sPsnF"
    auth = tweepy.OAuthHandler(API_key, API_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Enter Hashtag and initial date
    # print("Enter Twitter HashTag to search for")
    # words = input()
    # print("Enter Date since The Tweets are required in yyyy-mm--dd")
    # date_since = input()
    words = "#ECE4564T13"


    # number of tweets you want to extract in one run
    numtweet = 5
    #scrape(words, numtweet)
    myStream = SL(API_key, API_key_secret, access_token, access_token_secret)
    myStream.filter(track = ["#ECE4564T13"], threaded=True)
    print('Scraping has completed!')
