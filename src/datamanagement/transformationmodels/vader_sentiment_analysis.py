"""Module for VaderSentiment Model"""
from typing import List, Dict
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .transformation import Transformation


class VaderSentimentAnalysis(Transformation):
    """
    Applies vaderSentiment sentiment analysis to selftext, title, and comments.
    If the keys selftext, title and comments do not exist, the analysis is skipped.
    """

    def __init__(self):
        """
        Initializes the VaderSentimentAnalysis by initalising SentimentIntensityAnalyzer.
        """

        self.analyzer = SentimentIntensityAnalyzer()

    def apply(self, data: List[Dict]) -> List[Dict]:
        """
        Implemented method that transforms the raw data by running TextBlob with PatternAnalyzer.

        :param data: raw data received, could be pre-processed.
        :returns data: transformed data that contains the compound sentiment 
                       scores of each post content.
        """

        try:
            for post in tqdm(data, desc="Processing vader", unit="post"):
                # Ensure the 'transformation' and 'model_output' keys exist
                post.setdefault('transformed_data', {})
                post.setdefault('model_output', {})

                # Initialize 'vader' under 'model_output' if not present
                post['model_output'].setdefault('vader', {})

                # Now ensure that the vader field exists in the 'model_output' dictionary
                data_results = post['model_output']['vader']

                # Analyze sentiment for 'selftext'
                if 'selftext' in post:
                    sentiment = self.analyzer.polarity_scores(post['selftext'])
                    data_results['selftext_sentiment'] = sentiment['compound']

                # Analyze sentiment for 'title'
                if 'title' in post:
                    sentiment = self.analyzer.polarity_scores(post['title'])
                    data_results['title_sentiment'] = sentiment['compound']

                # Analyze sentiment for each comment and store all scores
                if 'comments' in post and isinstance(post['comments'], list):
                    # Store the compound score for each comment
                    comment_sentiments = [
                        self.analyzer.polarity_scores(comment)['compound']
                        for comment in post['comments']
                    ]
                    data_results['comments_sentiment'] = comment_sentiments

            return data

        except KeyError as e:
            print(f"Key error during sentiment analysis: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error during sentiment analysis: {e}")
            raise
