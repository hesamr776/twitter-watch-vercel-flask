import sys
import snscrape.modules.twitter as sntwitter
# import pandas as pd
import datetime


def search(text, username, since, until, retweet, replies):
    q = text

    if username != '':
        q += f" from:{username}"

    if until == '':
        until = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    q += f" until:{until}"
    if since == '':
        since = datetime.datetime.strftime(datetime.datetime.strptime(until, '%Y-%m-%d') - datetime.timedelta(days=7)
                                           , '%Y-%m-%d')
    q += f" since:{since}"

    if retweet == 'y':
        q += f" exclude:retweets"
    if replies == 'y':
        q += f" exclude:replies"

    # FILE NAME
    if username != '' and text != '':
        filename = f"{since}_{until}_{username}_{text}.csv"
    elif username != "":
        filename = f"{since}_{until}_{username}.csv"
    else:
        filename = f"{since}_{until}_{text}.csv"
    return q


def get_tweet(username, since):
    # Created a list to append all tweet attributes(data)
    attributes_container = []

    query = search('', str(username), '2023-02-01', '', 'y', 'y')

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if tweet.inReplyToTweetId is None:
            attributes_container.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username, tweet.replyCount,
                                         tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.inReplyToTweetId])

    # Creating a dataframe from the tweets list above
    # tweets_df = pd.DataFrame(attributes_container, columns=['DateTime', 'TweetId', 'Text', 'Username', 'ReplyCount',
    # 'RetweetCount', 'LikeCount', 'QuoteCount', '-'])

    # Creating a dataframe from the tweets list above
    # print(attributes_container)
    return attributes_container
