"""Module for TextBlob Model"""
from typing import List, Dict
from textblob import TextBlob
from textblob.sentiments import PatternAnalyzer
from tqdm import tqdm
from .transformation import Transformation


class TextBlobSentimentAnalysis(Transformation):
    """
    This class textblob sentiment analysis to selftext, title, and comments.
    If the keys selftext, title and comments do not exist, the analysis is skipped.
    """

    def __init__(self):
        """
        Initializes the TextBlobSentimentAnalysis by initalising PatternAnalyser.
        """

        self.analyzer = PatternAnalyzer()

    def apply(self, data: List[Dict]) -> List[Dict]:
        """
        Implemented method that transforms the raw data by running TextBlob with PatternAnalyzer.

        :param data: raw data received, could be pre-processed.
        :returns data: transformed data that contains the polarity scores of each post content.
        """

        try:
            for post in tqdm(data, desc="Processing textblob", unit="post"):
                # Ensure the 'transformed_data' and 'model_output' keys exist
                post.setdefault('transformed_data', {})
                post.setdefault('model_output', {})
                post['model_output'].setdefault('textblob', {})

                # Initialize 'textblob' under 'model_output' if not present
                post['model_output'].setdefault('textblob', {})

                # Ensure that the textblob field exists in the 'model_output' dictionary
                data_results = post['model_output']['textblob']

                # Analyze sentiment for 'selftext'
                if 'selftext' in post:
                    sentiment = TextBlob(
                        post['selftext'], analyzer=self.analyzer).sentiment
                    data_results['selftext_sentiment'] = sentiment.polarity

                # Analyze sentiment for 'title'
                if 'title' in post:
                    sentiment = TextBlob(
                        post['title'], analyzer=self.analyzer).sentiment
                    data_results['title_sentiment'] = sentiment.polarity

                # Analyze sentiment for each comment and store all scores
                if 'comments' in post and isinstance(post['comments'], list):
                    # Store the polarity score for each comment
                    comment_sentiments = [
                        TextBlob(comment, analyzer=self.analyzer)
                        .sentiment.polarity for comment in post['comments']
                    ]
                    data_results['comments_sentiment'] = comment_sentiments

            return data

        except KeyError as e:
            print(f"Key error during textblob analysis: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error during textblob analysis: {e}")
            raise
