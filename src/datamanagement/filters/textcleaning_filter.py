"""Module for TextCleaning Filter."""
import re
from .pipe_filter import Filter, Pipe


class TextCleaningFilter(Filter):
    """
    Cleans text in the fields by removing unwanted characters.
    """

    def execute(self, pipe: Pipe) -> None:
        """
        Executes the text cleaning process on each document in the pipe.

        :param pipe: The pipe containing the data to filter.
        """
        
        try:
            data = pipe.get_data()
            for post in data:
                if 'transformed_data' not in post:
                    post['transformed_data'] = {}

                # Clean the 'selftext' field if it exists
                if 'selftext' in post:
                    post['transformed_data']['selftext'] = self.clean_text(
                        post['selftext'])

                # Clean the 'title' field if it exists
                if 'title' in post:
                    post['transformed_data']['title'] = self.clean_text(
                        post['title'])

                # Clean the 'comments' field if it exists and is a list
                if 'comments' in post and isinstance(post['comments'], list):
                    post['transformed_data']['comments'] = [
                        self.clean_text(comment) for comment in post['comments']]

            # After cleaning, update the data in the pipe
            pipe.set_data(data)

        except KeyError as e:
            print(f"Key error during text cleaning: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error during text cleaning: {e}")
            raise

    def clean_text(self, text: str) -> str:
        """
        Cleans text by converting to lowercase and removing non-alphanumeric characters.

        :param text: The text string to be cleaned.
        :return: The processed text.
        """

        return re.sub(r'\W+', ' ', text.lower()).strip()
