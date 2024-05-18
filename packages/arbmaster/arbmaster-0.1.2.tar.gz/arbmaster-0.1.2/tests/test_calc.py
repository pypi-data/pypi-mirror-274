import unittest
from arbmaster import ArbitrageCalc

class TestArbitrageCalc(unittest.TestCase):
    """
    Test cases for the ArbitrageCalc class.
    """

    def test_arbitrage_calculation(self):
        """
        Test the calculation of arbitrage opportunities.
        """
        odds = {
            'home_team': [{'price': 2.0}],
            'away_team': [{'price': 3.0}],
            'draw': [{'price': 2.5}]
        }
        stake = 100
        
        calc = ArbitrageCalc(odds, stake)
        
        self.assertEqual(calc.odds, [2.0, 3.0, 2.5])
        self.assertEqual([round(x, 2) for x in calc.stakes], [40.54, 27.03, 32.43])
        self.assertEqual(calc.payout, 81.08)
        self.assertEqual(calc.profit, -18.92)
        self.assertEqual(calc.roi, '-18.92%')

    def test_is_arbitrage_method(self):
        """
        Test the identification of arbitrage opportunities.
        """
        odds_no_arbitrage = {
            'home_team': [{'price': 1.5}],
            'away_team': [{'price': 2.0}],
            'draw': [{'price': 2.5}]
        }
        odds_arbitrage = {
            'home_team': [{'price': 4.2}],
            'away_team': [{'price': 3.0}],
            'draw': [{'price': 3.1}]
        }
        
        calc_no_arbitrage = ArbitrageCalc(odds_no_arbitrage)
        calc_arbitrage = ArbitrageCalc(odds_arbitrage)
        
        self.assertFalse(calc_no_arbitrage.is_arbitrage())
        self.assertTrue(calc_arbitrage.is_arbitrage())


if __name__ == '__main__':
    unittest.main()
