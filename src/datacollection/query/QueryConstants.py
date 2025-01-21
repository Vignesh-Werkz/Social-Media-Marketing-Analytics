from string import Template

""" This module contains the constants used in the query handling. """

DATA_SOURCE_REDDIT = "reddit"
QUERY_TYPE_GLOBAL_LATEST = "globalLatest"
QUERY_TYPE_SUBREDDIT_LATEST = "subredditLatest"
REDDIT_LATEST_DATA_URL = Template("https://oauth.reddit.com/new.json?limit=100&count=$count&after=$after")
REDDIT_LATEST_SUBREDDIT_DATA_URL = Template("https://oauth.reddit.com/r/$subreddit/new.json?limit=100")
REDDIT_GET_COMMENTS_URL = Template("https://oauth.reddit.com/r/$subreddit/comments/$postId.json?depth=1")
REDDIT_COUNT_AFTER_STRING = "&count=$count&after=$after"