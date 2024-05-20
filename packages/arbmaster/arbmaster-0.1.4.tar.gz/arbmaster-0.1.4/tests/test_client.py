import json
import unittest
from unittest.mock import Mock, patch
from arbmaster import Client, Match


# Load environment variables from .env file
envfile = open(".env", "r")
dotenv = {k.strip(): v.strip() for k, v in [i.split('=') for i in envfile.read().split('\n') if i]}
envfile.close()

# Load test data
datafile = open("tests/data.json", "r")
test_data = json.load(datafile)
datafile.close()


class TestClient(unittest.TestCase):
    """
    Test cases for the Client class.
    """

    def setUp(self):
        """
        Initialize common resources for tests.
        """
        self.api_key = dotenv.get('API_KEY')
        self.client = Client(api_key=self.api_key)

    def test_initialization(self):
        """
        Test initialization of Client instance.
        """
        self.assertEqual(self.client.api_key, self.api_key)
        self.assertIsInstance(self.client.params, dict)
        self.assertIsInstance(self.client.headers, dict)
        self.assertIn("apiKey", self.client.params)
        self.assertEqual(self.client.params["apiKey"], self.api_key)
    
    def test_add_bookmakers(self):
        """
        Test adding bookmakers to the client instance.
        """
        self.client.add_bookmakers("unibet", "williamhill")
        self.assertIn("unibet", self.client.bookmakers)
        self.assertIn("williamhill", self.client.bookmakers)

    def test_update_params(self):
        """
        Test updating parameters of the client instance.
        """
        self.client.update_params(test_param="test_value")
        self.assertIn("test_param", self.client.params)
        self.assertEqual(self.client.params["test_param"], "test_value")

    def test_update_headers(self):
        """
        Test updating headers of the client instance.
        """
        self.client.update_headers(test_header="test_value")
        self.assertIn("test_header", self.client.headers)
        self.assertEqual(self.client.headers["test_header"], "test_value")

    def test_fetch_league(self):
        """
        Test fetching league data from the client.
        """
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"x-requests-remaining": "5"}
        mock_response.json.return_value = test_data

        # Mock the session
        self.client.session = Mock()
        self.client.session.get.return_value = mock_response

        matches = self.client.fetch_league("basketball_nba")
        self.assertIsInstance(matches, list)
        self.assertEqual(len(matches), 1)
        self.assertTrue(all(isinstance(match, Match) for match in matches))

    def test_fetch_sport(self):
        """
        Test fetching sport data from the client.
        """
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"x-requests-remaining": "5"}
        mock_response.json.return_value = test_data

        # Mock the session
        self.client.session = Mock()
        self.client.session.get.return_value = mock_response
        matches = self.client.fetch_sport("basketball")
        self.assertIsInstance(matches, list)
        self.assertTrue(all(isinstance(match, Match) for match in matches[0]))


if __name__ == "__main__":
    unittest.main()
