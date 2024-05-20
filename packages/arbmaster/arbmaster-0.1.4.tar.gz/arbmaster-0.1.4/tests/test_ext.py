import json
import unittest
from arbmaster import Match, Odds, Bookmaker

# Load test data
file = open("project/tests/data.json", "r")
test_data = json.load(file)
file.close()


class TestBookmaker(unittest.TestCase):
    """
    Test cases for the Bookmaker class.
    """

    def test_new_method(self):
        """
        Test the creation of a Bookmaker instance using the new method.
        """
        bm_data = test_data[0]['bookmakers'][0]
        bm = Bookmaker.new(bm_data)

        self.assertEqual(bm.key, 'sport888')
        self.assertEqual(bm.title, '888sport')
        self.assertEqual(bm.home_odds, 2.75)
        self.assertEqual(bm.away_odds, 1.45)
        self.assertIsNone(bm.draw_odds)

    def test_json_method(self):
        """
        Test the conversion of a Bookmaker instance to JSON format.
        """
        bm = Bookmaker('betway', 'Betway', 2.95, 1.42)
        result = bm.json(2.95)
        self.assertEqual(result, {'key': 'betway', 'title': 'Betway', 'price': 2.95})


class TestOdds(unittest.TestCase):
    """
    Test cases for the Odds class.
    """

    def test_odds_calculation(self):
        """
        Test the calculation of best odds among bookmakers for home, away, and draw outcomes.
        """
        bookmakers = [
            Bookmaker('casumo', 'Casumo', 2.23, 1.62, 3.2),
            Bookmaker('leovegas', 'LeoVegas', 2.2, 1.61),
            Bookmaker('nordicbet', 'Nordic Bet', 2.27, 1.63),
            Bookmaker('sport888', '888sport', 2.25, 1.65)
        ]
        odds = Odds(bookmakers)
        
        self.assertEqual(odds.home, [{'key': 'nordicbet', 'title': 'Nordic Bet', 'price': 2.27}])
        self.assertEqual(odds.away, [{'key': 'sport888', 'title': '888sport', 'price': 1.65}])
        self.assertEqual(odds.draw, [{'key': 'casumo', 'title': 'Casumo', 'price': 3.2}])
    
    def test_new_method(self):
        """
        Test the creation of an Odds instance using the new method.
        """
        odds_data = {
            'home_team': [{'key': 'nordicbet', 'title': 'Nordic Bet', 'price': 2.27}],
            'away_team': [{'key': 'sport888', 'title': '888sport', 'price': 1.65}],
            'draw': [{'key': 'casumo', 'title': 'Casumo', 'price': 3.2}]
        }
        odds = Odds.new(odds_data)

        self.assertEqual(len(odds.home), 1)
        self.assertEqual(len(odds.away), 1)
        self.assertEqual(len(odds.draw), 1)

    def test_json_method(self):
        """
        Test the conversion of an Odds instance to JSON format.
        """
        odds_data = {
            'home_team': [{'key': 'nordicbet', 'title': 'Nordic Bet', 'price': 2.27}],
            'away_team': [{'key': 'sport888', 'title': '888sport', 'price': 1.65}],
            'draw': [{'key': 'casumo', 'title': 'Casumo', 'price': 3.2}]
        }
        odds = Odds.new(odds_data)
        result = odds.json()
        # Assertions
        self.assertEqual(len(result['home_team']), 1)
        self.assertEqual(len(result['away_team']), 1)
        self.assertEqual(len(result['draw']), 1)


class TestMatch(unittest.TestCase):
    """
    Test cases for the Match class.
    """

    def test_match_initialization(self):
        """
        Test the initialization of a Match instance.
        """
        match = Match(test_data[1])

        self.assertEqual(match.id, 'c87df77d60f9110b769f8e3f4fcc83c6')
        self.assertEqual(match.sport_key, 'basketball_nba')
        self.assertEqual(match.sport_title, 'NBA')
        self.assertEqual(match.home_team, 'Chicago Bulls')
        self.assertEqual(match.away_team, 'Atlanta Hawks')
        self.assertEqual(match.commence_time, '2024-04-18T03:40:00')
        self.assertIsInstance(match.odds, Odds)
    
    def test_match_json_method(self):
        """
        Test the conversion of a Match instance to JSON format.
        """
        match = Match(test_data[1])
        result = match.json()

        self.assertEqual(result['id'], 'c87df77d60f9110b769f8e3f4fcc83c6')
        self.assertEqual(result['sport_key'], 'basketball_nba')
        self.assertEqual(result['sport_title'], 'NBA')
        self.assertEqual(result['home_team'], 'Chicago Bulls')
        self.assertEqual(result['away_team'], 'Atlanta Hawks')
        self.assertEqual(result['commence_time'], '2024-04-18T03:40:00')
        self.assertIsInstance(result['odds'], dict)
    

if __name__ == '__main__':
    unittest.main()
