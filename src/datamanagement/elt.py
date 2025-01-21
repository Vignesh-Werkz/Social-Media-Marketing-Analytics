"""ELT Module"""
from .filters import TextCleaningFilter, TokenizationFilter, StopWordFilter, pipe_filter
from .dataclient import DataClientManager, DataClientConfig
from .transformationmodels import TextBlobSentimentAnalysis, VaderSentimentAnalysis, LDATopicModeling


class ELT:
    """
    This class orchestrates the ELT process to transform data collected in
    Data Collection module and stores into target database for further analysis.
    """

    def __init__(self, source_db: DataClientConfig, target_db: DataClientConfig,
                 transformations: list):
        """
        Initializes the ELT component with source and target database configurations.

        :param source_db: A DatabaseConfig object containing the source database details.
        :param target_db: A DatabaseConfig object containing the target database details.
        :param transformations: A list of transformation strings to apply during 
                                the process. (e.g. 'vader')
        """
        self.source_db = source_db
        self.source_client = None
        self.target_db = target_db
        self.target_client = None
        self.transformations = transformations

    def get_models(self, model_names: list[str]) -> list:
        """
        Given a list of strings containing the model names, returns a 
        list of instantiated model objects.

        :param model_names: A list of model names in string.
        :returns: The model/class representation of models mapped from the string.
        """

        # Dictionary to map strings to their corresponding classes
        model_mapping = {
            'vader': VaderSentimentAnalysis,
            'textblob': TextBlobSentimentAnalysis,
            'lda': LDATopicModeling
        }

        return [model_mapping[model]() for model in model_names if model in model_mapping]

    def preprocess(self, raw_data):
        """
        Preprocesses the raw data by applying a series of filters.

        :param raw_data: The raw data loaded from the source.
        :return: Preprocessed data after applying the filters.
        """

        # Initialize a Pipe object to hold the data
        pipe = pipe_filter.Pipe()
        pipe.set_data(raw_data)

        # Apply preprocessing filters
        cleaning_filter = TextCleaningFilter()
        tokenization_filter = TokenizationFilter()
        stopword_filter = StopWordFilter()

        # Execute each filter on the data
        cleaning_filter.execute(pipe)
        tokenization_filter.execute(pipe)
        stopword_filter.execute(pipe)

        # Return the preprocessed data from the pipe
        return pipe.get_data()

    def load(self):
        """
        Loads raw data from the data source.

        :return: raw_data the data that is retrieved from the specified database source.
        """

        self.source_client = DataClientManager.get_database_client(
            self.source_db)
        raw_data = self.source_client.load_data()
        self.source_client.close()

        return raw_data

    def transform(self, data):
        """Applies a series of transformations to the data.

        :param data: The preprocessed data that needs to be transformed.
        :return: The transformed data after applying all transformations.
        """

        models = self.get_models(self.transformations)
        for model in models:
            # Each transformation object has an apply method
            data = model.apply(data)

        return data

    def store(self, transformed_data):
        """
        Stores the transformed data in the target database.

        :param transformed_data: The transformed data to store into target database.
        """

        self.target_client = DataClientManager.get_database_client(
            self.target_db)
        self.target_client.upsert_data(transformed_data)

        self.target_client.close()

    def execute(self):
        """
        Executes the ETL process.
        """

        try:
            # Step 1: Load raw data from the source database
            raw_data = self.load()
            if not raw_data:
                return {'status': 'error', 'message': 'No data found in source.'}

            # Step 2: Preprocess the data
            preprocessed_data = self.preprocess(raw_data)
            # print(preprocessed_data)

            # Step 3: Transform the data
            transformed_data = self.transform(preprocessed_data)

            # Step 4: Store (upsert) the transformed data into the target database
            self.store(transformed_data)

            return {'status': 'success', 'message': 'ELT process completed successfully.'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}
