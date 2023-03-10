import sys
import snscrape.modules.twitter as sntwitter
# import pandas as pd
import datetime
import time


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


def get_tweet(username, since):
    # Created a list to append all tweet attributes(data)
    attributes_container = []
    replies = []

    query = search('', str(username), '2023-02-01', '', 'y', 'y')
    # wait_counter = 0

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        attributes_container.append({
            'id': tweet.id,
            'date': tweet.date,
            'text': tweet.rawContent,
            'username': tweet.user.username,
            'conversationId': tweet.conversationId
        })
        # wait_counter += 1

        # if tweet.inReplyToTweetId is None:
        # for j, reply in enumerate(
        #        sntwitter.TwitterSearchScraper(f'conversation_id:{tweet.conversationId}').get_items()):
        #    replies.append({
        #     'id': tweet.id,
        #     'date': tweet.date,
        #     'text': tweet.rawContent,
        #     'username': tweet.user.username,
        #     'conversationId': tweet.conversationId
        # })
        # wait_counter += 1

        #    if wait_counter % 100 == 0:
        #        time.sleep(5)

    print(len(attributes_container))
    return attributes_container
