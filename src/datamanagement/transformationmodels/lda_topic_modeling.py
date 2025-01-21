"""Module for LDA Topic Modelling"""
from typing import List, Dict
from collections import defaultdict
import nltk
import spacy
from spacy.cli import download
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
from .transformation import Transformation

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
download("en_core_web_sm")


class LDATopicModeling(Transformation):
    """
    Applies LDA (Latent Dirichlet Allocation) topic modeling to selftext, title, and comments.
    This class assumes that stopword filtering has already been applied.
    """

    def __init__(self, num_topics=3, passes=40, top_n_keywords=5, min_word_len=3):
        """
        Initializes the LDA topic model class.

        :param num_topics: Number of topics to generate in LDA.
        :param passes: Number of passes for the LDA model.
        :param top_n_keywords: Number of top unique keywords to extract.
        :param min_word_len: Minimum word length to consider for LDA.
        """
        self.num_topics = num_topics
        self.passes = passes
        self.top_n_keywords = top_n_keywords
        self.min_word_len = min_word_len
        self.lemmatizer = WordNetLemmatizer()
        self.nlp = spacy.load("en_core_web_sm")

        # Exclude certain labels such as time, percent, quantity, ordinal, and cardinal
        self.excluded_labels = {'DATE', 'TIME',
                                'PERCENT', 'QUANTITY', 'ORDINAL', 'CARDINAL'}

    def preprocess_text(self, tokens):
        """
        Preprocess tokens by POS tagging, lemmatization, and filtering.
        Retains nouns, proper nouns, and named entities (like company names).
        """
        text = " ".join(tokens)
        named_entities = self.extract_named_entities(text)

        # POS tagging and token filtering
        pos_tagged = nltk.pos_tag(tokens)
        relevant_pos_tags = {'NN', 'NNS', 'NNP', 'NNPS', 'JJ'}
        filtered_tokens = [
            self.lemmatizer.lemmatize(word) for word, pos in pos_tagged
            if pos in relevant_pos_tags and word.isalpha() and len(word) >= self.min_word_len
        ]

        return filtered_tokens + named_entities

    def extract_named_entities(self, text):
        """
        Use NER to extract named entities from the text, such as company names.
        Exclude entities based on specific labels like TIME, PERCENT, etc.
        """
        doc = self.nlp(text)
        named_entities = [
            ent.text for ent in doc.ents if ent.label_ not in self.excluded_labels]
        unique_named_entities = list(set(named_entities))
        return unique_named_entities

    def apply_tfidf_filtering(self, tokens):
        """
        Applies TF-IDF filtering to retain only relevant words.

        :param tokens: List of tokens.
        :return: Filtered tokens.
        """
        if not tokens:
            return tokens

        # Convert the tokens list into a single document (input for the TfidfVectorizer)
        text_data = [" ".join(tokens)]

        try:
            vectorizer = TfidfVectorizer(
                tokenizer=lambda x: x.split(), min_df=1)
            tfidf_matrix = vectorizer.fit_transform(text_data)
            tfidf_scores = dict(
                zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0]))

            # Keep words with a lower TF-IDF score
            filtered_tokens = [word for word,
                               score in tfidf_scores.items() if score >= 0.05]

            # Return the original tokens if TF-IDF filtering removes all words
            if not filtered_tokens:
                return tokens  # Return original tokens if none pass the TF-IDF filter

            return filtered_tokens

        except ValueError as e:
            print(f"Error in TF-IDF filtering: {e}")
            return tokens  # Return the original tokens if TF-IDF fails

    def apply(self, data: List[Dict]) -> List[Dict]:
        """
        Applies LDA topic modeling to 'selftext', 'title', and 'comments' fields after stopwords 
        have already been removed.

        :param data: The list of posts (each post contains 'selftext_tokens', 'title_tokens', 
                     and 'comments_tokens').
        :return: The modified data with 'lda_keywords' field containing the top N unique topic keywords.
        """
        # Add tqdm to track progress
        for post in tqdm(data, desc="Processing topics", unit="post"):
            # Combine tokens from 'selftext', 'title', and 'comments'
            transformed_data = post.get('transformed_data', {})
            combined_tokens = (
                transformed_data.get('selftext_tokens', []) +
                transformed_data.get('title_tokens', []) +
                [token for comment in transformed_data.get(
                    'comments_tokens', []) for token in comment]
            )

            # Skip LDA processing if no valid tokens remain after filtering
            if not combined_tokens:
                post['keywords'] = []  # Assign an empty keywords list
                continue

            # Preprocess tokens: Apply POS tagging, lemmatization, and length filtering
            processed_tokens = self.preprocess_text(combined_tokens)

            # Apply TF-IDF filtering
            processed_tokens = self.apply_tfidf_filtering(processed_tokens)

            # If after filtering the tokens list is empty, skip LDA
            if not processed_tokens:
                post['keywords'] = []
                continue

            # Create a dictionary and corpus for LDA
            dictionary = corpora.Dictionary([processed_tokens])
            corpus = [dictionary.doc2bow(processed_tokens)]

            # Skip LDA if the corpus is empty
            if not corpus or all(len(doc) == 0 for doc in corpus):
                post['keywords'] = []  # Assign an empty keywords list
                continue

            # Train LDA model
            lda_model = LdaModel(
                corpus, num_topics=self.num_topics, id2word=dictionary, passes=self.passes,
                iterations=100, chunksize=10000, eval_every=None)

            # Get topics from LDA model
            topics = lda_model.show_topics(num_words=5, formatted=False)

            # Aggregate the keyword scores across all topics
            keyword_scores = defaultdict(float)
            for topic in topics:
                for word, score in topic[1]:
                    keyword_scores[word] += score

            # Sort keywords by their cumulative score and select the top N unique keywords
            sorted_keywords = sorted(
                keyword_scores.items(), key=lambda x: x[1], reverse=True)
            top_keywords = [word for word,
                            _ in sorted_keywords[:self.top_n_keywords]]

            # Extract subreddit and include it in the top keywords
            subreddit = post.get("subreddit", "").lower()
            if subreddit and subreddit not in top_keywords:
                top_keywords.insert(0, subreddit)

            # Store top unique keywords in the post
            post['keywords'] = top_keywords

        return data
