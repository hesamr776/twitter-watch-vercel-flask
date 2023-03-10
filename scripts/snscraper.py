import sys
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import time
import json


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


def get_reply(sinceId, language='en'):
    # The max_id is the ID of the tweet of interest, and the since_id is one below that; or in other words, since_id
    # filters for tweets newer than an ID (not inclusive) and max_id filters for tweets older than an ID (inclusive).
    # e.g. snscrape --jsonl twitter-search 'since_id:1303506596216045567 max_id:1303506596216045568 -filter:safe'
    replies = []
    count = 0
    for j, reply in enumerate(
            sntwitter.TwitterSearchScraper(f'since_id:{str(sinceId)} -filter:safe').get_items()):

        if language == 'all':
            replies.append({
                'id': reply.id,
                'date': reply.date,
                'text': reply.rawContent,
                'username': reply.user.username,
                'conversationId': reply.conversationId
            })
            count += 1

        else:
            if reply.lang == str(language):
                replies.append({
                    'id': reply.id,
                    'date': reply.date,
                    'text': reply.rawContent,
                    'username': reply.user.username,
                    'conversationId': reply.conversationId
                })

                count += 1

        if count == 20:
            break

    return replies


def get_tweet(username, since='2023-02-01'):
    #
    original_tweets = []

    # this query returns original tweets by given username
    query = search('', str(username), since, '', 'y', 'y')
    count = 0

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        original_tweets.append({
            'id': tweet.id,
            'date': tweet.date,
            'text': tweet.rawContent,
            'username': tweet.user.username,
            'conversationId': tweet.conversationId
        })
        count += 1
        if count == -1:
            break

    try:
        tweets_df = pd.DataFrame(original_tweets)
        tweets_df.to_csv(f'../data/{username}_since-{since}.csv', encoding='utf-8')
    except:
        print('failed to save file')
        pass

    return original_tweets


if __name__ == '__main__':

    user = 'elonmusk'
    elon_tweets = get_tweet(user)

    replies = []
    for tweet in elon_tweets:
        tweetId = tweet['id']
        elon_replies = get_reply(tweetId)
        replies.append({'tweetId': tweetId, 'replies': elon_replies})

    print(replies)
    try:
        with open(f'../data/replyTo-{user}', 'w') as f:
            json.dump(replies, f)
    except:
        print('failed to save file')
        pass
