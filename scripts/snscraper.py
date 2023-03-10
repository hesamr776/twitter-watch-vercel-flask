import sys
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import json
from json import JSONEncoder
from preprocessing import preprocess

from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis")


def search(text, username, since, until, retweet, replies):
    query = text

    if username != '':
        query += f" from:{username}"

    if until == '':
        until = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    query += f" until:{until}"
    if since == '':
        since = datetime.datetime.strftime(datetime.datetime.strptime(until, '%Y-%m-%d') - datetime.timedelta(days=7)
                                           , '%Y-%m-%d')
    query += f" since:{since}"

    if retweet == 'y':
        query += f" exclude:retweets"
    if replies == 'y':
        query += f" exclude:replies"

    return query


def get_tweet(username, since='2023-02-01', preproc=False):

    original_tweets = []

    # this query returns original tweets by given username
    query = search('', str(username), since, '', 'y', 'y')
    max_tweet = -1

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):

        if max_tweet != -1:
            if i >= max_tweet:
                break

        if preproc:
            text = preprocess(tweet.rawContent).get_result()
        else:
            text = tweet.rawContent

        if len(text) == 0:
            continue

        sentiment_prediction = sentiment_pipeline(str(text))
        if sentiment_prediction[0]['label'] == 'NEGATIVE' and sentiment_prediction[0]['score'] > 0.8:
            sentiment = 0
        elif sentiment_prediction[0]['label'] == 'POSITIVE' and sentiment_prediction[0]['score'] > 0.8:
            sentiment = 1
        else:
            sentiment = -1

        original_tweets.append({
            'id': tweet.id,
            'date': tweet.date,
            'text': tweet.rawContent,
            'username': tweet.user.username,
            'conversationId': tweet.conversationId,
            'sentiment': sentiment
        })

    try:
        with open(f'../data/{username}_since-{since}.json', 'w') as t:
            json.dump(original_tweets, t, cls=DateTimeEncoder)
        # tweets_df = pd.DataFrame(original_tweets)
        # tweets_df.to_csv(f'../data/{username}_since-{since}.csv', encoding='utf-8')
    except:
        print('failed to save tweets')
        pass

    return original_tweets


def get_reply(sinceId, language='en', preproc=False):
    # The max_id is the ID of the tweet of interest, and the since_id is one below that; or in other words, since_id
    # filters for tweets newer than an ID (not inclusive) and max_id filters for tweets older than an ID (inclusive).
    # e.g. snscrape --jsonl twitter-search 'since_id:1303506596216045567 max_id:1303506596216045568 -filter:safe'
    replies = []
    max_reply = 20
    for j, reply in enumerate(
            sntwitter.TwitterSearchScraper(f'since_id:{str(sinceId)} -filter:safe').get_items()):

        if j >= max_reply:
            break

        if preproc:
            text = preprocess(reply.rawContent).get_result()
        else:
            text = reply.rawContent

        if len(text) == 0:
            continue

        sentiment_prediction = sentiment_pipeline(str(text))
        if sentiment_prediction[0]['label'] == 'NEGATIVE' and sentiment_prediction[0]['score'] > 0.8:
            sentiment = 0
        elif sentiment_prediction[0]['label'] == 'POSITIVE' and sentiment_prediction[0]['score'] > 0.8:
            sentiment = 1
        else:
            sentiment = -1

        if language == 'all':
            replies.append({
                'id': reply.id,
                'date': reply.date,
                'text': reply.rawContent,
                'username': reply.user.username,
                'conversationId': reply.conversationId,
                'sentiment': sentiment
            })

        else:
            if reply.lang == str(language):
                replies.append({
                    'id': reply.id,
                    'date': reply.date,
                    'text': text,
                    'username': reply.user.username,
                    'conversationId': reply.conversationId,
                    'sentiment': sentiment
                })

    return replies


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


if __name__ == '__main__':

    users = ['elonmusk', 'BarackObama', 'taylorlorenz', 'cathiedwood', 'ylecun']

    for user in users:

        tweets = get_tweet(user, preproc=True)

        # the tweets which include empty list for replies, were just link or media
        replies = []
        for tweet in tweets:
            tweetId = tweet['id']
            reply = get_reply(tweetId, preproc=True)
            if reply is not None:
                replies.append({'tweetId': tweetId, 'replies': reply})
        print(f'scraping {user} has been done!')

        try:
            with open(f'../data/replyTo-{user}.json', 'w') as f:
                json.dump(replies, f, cls=DateTimeEncoder)
        except:
            print('failed to save replies')
            pass
