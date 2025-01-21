"""Module for Tokenization Filter."""
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from .pipe_filter import Filter, Pipe


class TokenizationFilter(Filter):
    """
    Tokenizes the text data and stores the tokens under the 'transformed_data' key.
    If the keys selftext, title and comments do not exist, the tokenization is skipped.
    """

    def execute(self, pipe: Pipe) -> None:
        """
        Executes the tokenization process on each document in the pipe.

        :param pipe: The pipe containing the data to filter.
        """

        try:
            data = pipe.get_data()
            for post in data:
                if 'transformed_data' not in post:
                    post['transformed_data'] = {}

                # Tokenize 'selftext' if it exists and store in 'transformed_data'
                if 'selftext' in post['transformed_data']:
                    post['transformed_data']['selftext_tokens'] = word_tokenize(
                        post['transformed_data']['selftext'])

                # Tokenize 'title' if it exists and store in 'transformed_data'
                if 'title' in post['transformed_data']:
                    post['transformed_data']['title_tokens'] = word_tokenize(
                        post['transformed_data']['title'])

                # Tokenize 'comments' if they exist and are a list, store in 'transformed_data'
                if 'comments' in post['transformed_data'] and isinstance(post['transformed_data']['comments'], list):
                    post['transformed_data']['comments_tokens'] = [
                        word_tokenize(comment) for comment in post['transformed_data']['comments']]

            # After tokenization, update the data in the pipe
            pipe.set_data(data)

        except KeyError as e:
            print(f"Key error during tokenization: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error during tokenization: {e}")
            raise
