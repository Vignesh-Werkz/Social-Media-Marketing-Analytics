"""Module for Stopword filter."""
import nltk
from nltk.corpus import stopwords
from .pipe_filter import Pipe, Filter

# Ensure NLTK resources are downloaded (if needed)
nltk.download('stopwords')

class StopWordFilter(Filter):
    """
    Removes stop words from the tokenized text stored under the 'transformed_data' key.
    Skips removal if tokenized text does not exist. Uses only NLTK's stop words.
    """

    def __init__(self):
        """
        Initializes the StopWordFilter class using NLTK stop words.
        """
        # Use NLTK stop words
        self.stop_words = set(stopwords.words('english'))

    def execute(self, pipe: Pipe) -> None:
        """
        Implemented method that executes the filter to remove stop words.

        :param pipe: The pipe that contains the data to filter and update in.
        """
        try:
            data = pipe.get_data()
            for post in data:
                if 'transformed_data' not in post:
                    post['transformed_data'] = {}

                # Remove stopwords from 'selftext_tokens' if they exist in 'transformed_data'
                if 'selftext_tokens' in post['transformed_data']:
                    post['transformed_data']['selftext_tokens'] = [
                        word for word in post['transformed_data']['selftext_tokens']
                        if word not in self.stop_words
                    ]

                # Remove stopwords from 'title_tokens' if they exist in 'transformed_data'
                if 'title_tokens' in post['transformed_data']:
                    post['transformed_data']['title_tokens'] = [
                        word for word in post['transformed_data']['title_tokens']
                        if word not in self.stop_words
                    ]

                # Remove stopwords from 'comments_tokens' if they exist in 'transformed_data'
                if 'comments_tokens' in post['transformed_data'] and isinstance(
                        post['transformed_data']['comments_tokens'], list):
                    post['transformed_data']['comments_tokens'] = [
                        [word for word in comment_tokens if word not in self.stop_words]
                        for comment_tokens in post['transformed_data']['comments_tokens']
                    ]

            # After stopword removal, update the data in the pipe
            pipe.set_data(data)

        except KeyError as e:
            print(f"Key error during stopword filtering: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error during stopword filtering: {e}")
            raise
