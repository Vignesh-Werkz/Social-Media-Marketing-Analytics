"""Module for Test ELT"""
import unittest
from unittest.mock import patch, MagicMock
from src.datamanagement.dataclient.data_client_config import DataClientConfig
from src.datamanagement.elt import ELT


class TestELT(unittest.TestCase):
    """
    Unit test class for ELT.
    """
    # pylint: disable=arguments-differ, unused-variable, unused-argument, too-few-public-methods

    def setUp(self):
        """
        Set up mock configurations and ELT instance.
        """
        self.source_db_config = DataClientConfig(
            db_type="mongodb", uri="mongodb://localhost", db_name="source_db",
            collection="source_collection"
        )
        self.target_db_config = DataClientConfig(
            db_type="mongodb", uri="mongodb://localhost", db_name="target_db",
            collection="target_collection"
        )
        self.transformations = ['vader', 'textblob']
        self.elt = ELT(self.source_db_config,
                       self.target_db_config, self.transformations)

    @patch('src.datamanagement.elt.VaderSentimentAnalysis')
    @patch('src.datamanagement.elt.TextBlobSentimentAnalysis')
    def test_get_models(self, mock_vader, mock_textblob):
        """
        Test get_models() returns the correct transformation objects.
        """
        models = self.elt.get_models(self.transformations)
        self.assertEqual(len(models), 2)
        self.assertIsInstance(models[0], MagicMock)
        self.assertIsInstance(models[1], MagicMock)

    @patch('src.datamanagement.filters.pipe_filter.Pipe')
    @patch('src.datamanagement.elt.TextCleaningFilter')
    @patch('src.datamanagement.elt.TokenizationFilter')
    @patch('src.datamanagement.elt.StopWordFilter')
    def test_preprocess(self, mock_stopword, mock_tokenization, mock_cleaning, mock_pipe):
        """
        Test preprocess() applies filters to the raw data.
        """
        raw_data = [{'selftext': 'Test text'}]
        mock_pipe_instance = mock_pipe.return_value
        self.elt.preprocess(raw_data)
        mock_cleaning().execute.assert_called_once_with(mock_pipe_instance)
        mock_tokenization().execute.assert_called_once_with(mock_pipe_instance)
        mock_stopword().execute.assert_called_once_with(mock_pipe_instance)

    @patch('src.datamanagement.dataclient.DataClientManager.get_database_client')
    def test_load(self, mock_get_db_client):
        """
        Test load() retrieves data from the source database.
        """
        mock_client = MagicMock()
        mock_get_db_client.return_value = mock_client
        mock_client.load_data.return_value = [{'selftext': 'Test text'}]
        data = self.elt.load()
        mock_get_db_client.assert_called_once_with(self.source_db_config)
        mock_client.load_data.assert_called_once()
        self.assertEqual(data, [{'selftext': 'Test text'}])
        mock_client.close.assert_called_once()

    @patch('src.datamanagement.elt.VaderSentimentAnalysis')
    @patch('src.datamanagement.elt.TextBlobSentimentAnalysis')
    def test_transform(self, mock_textblob, mock_vader):
        """
        Test transform() applies the transformations to the data.
        """
        data = [{'selftext': 'Test text'}]
        mock_vader_instance = mock_vader.return_value
        mock_textblob_instance = mock_textblob.return_value
        transformed_data = self.elt.transform(data)
        mock_vader_instance.apply.assert_called_once_with(data)
        mock_textblob_instance.apply.assert_called_once_with(
            mock_vader_instance.apply.return_value)
        self.assertEqual(transformed_data,
                         mock_textblob_instance.apply.return_value)

    @patch('src.datamanagement.dataclient.DataClientManager.get_database_client')
    def test_store(self, mock_get_db_client):
        """
        Test store() inserts the transformed data into the target database.
        """
        mock_client = MagicMock()
        mock_get_db_client.return_value = mock_client
        transformed_data = [{'selftext': 'Test text'}]
        self.elt.store(transformed_data)
        mock_get_db_client.assert_called_once_with(self.target_db_config)
        mock_client.upsert_data.assert_called_once_with(transformed_data)
        mock_client.close.assert_called_once()

    @patch('src.datamanagement.elt.ELT.load')
    @patch('src.datamanagement.elt.ELT.preprocess')
    @patch('src.datamanagement.elt.ELT.transform')
    @patch('src.datamanagement.elt.ELT.store')
    def test_execute_success(self, mock_store, mock_transform, mock_preprocess, mock_load):
        """
        Test execute() runs successfully and returns success response.
        """
        mock_load.return_value = [{'selftext': 'Test text'}]
        mock_preprocess.return_value = [{'selftext': 'Preprocessed text'}]
        mock_transform.return_value = [{'selftext': 'Transformed text'}]

        result = self.elt.execute()

        mock_load.assert_called_once()
        mock_preprocess.assert_called_once_with(mock_load.return_value)
        mock_transform.assert_called_once_with(mock_preprocess.return_value)
        mock_store.assert_called_once_with(mock_transform.return_value)

        self.assertEqual(
            result, {'status': 'success', 'message': 'ELT process completed successfully.'})

    @patch('src.datamanagement.elt.ELT.load')
    def test_execute_no_data(self, mock_load):
        """
        Test execute() returns an error if no data is found.
        """
        mock_load.return_value = []
        result = self.elt.execute()
        self.assertEqual(result, {'status': 'error',
                         'message': 'No data found in source.'})

    @patch('src.datamanagement.elt.ELT.load', side_effect=Exception('Unexpected error'))
    def test_execute_exception(self, mock_load):
        """
        Test execute() returns an error if an exception occurs.
        """
        result = self.elt.execute()
        self.assertEqual(result, {'status': 'error',
                         'message': 'Unexpected error'})


if __name__ == '__main__':
    unittest.main()
