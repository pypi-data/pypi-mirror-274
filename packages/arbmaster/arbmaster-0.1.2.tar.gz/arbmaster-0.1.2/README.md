# arbmaster

Arbmaster is a Python package for fetching sports odds data from the Odds API and performing arbitrage calculations. It provides functionalities for retrieving odds data from multiple bookmakers, identifying arbitrage opportunities, and calculating potential profits.

## Installation

You can install arbmaster via pip:

```bash
pip install arbmaster
```

## Usage

### Fetching Odds Data

```python
from arbmaster import Client
from arbmaster import LEAGUES

# Make sure to save your key in a secure
# place for example a .env file
client = Client(api_key="YOUR_ODDS_API_KEY")

fetch_all_data_from_api = client.fetch_all()
data_for_a_single_sport = client.fetch_sport('basketball') # or LEAGUES[1]['group']
data_for_a_league = client.fetch_league(LEAGUES[1]['key'])
```

### Performing Arbitrage Calculations

You can also perform arbitrage calculations using the `ArbitrageCalc` class.
Example:

```python
from arbmaster import ArbitrageCalc

odds = {'home_team': [{'price': 2.0}], 'away_team': [{'price': 3.0}], 'draw': [{'price': 2.5}]}
calc = ArbitrageCalc(odds, stake=100)
print(f"Is Arbitrage Possible? {calc.is_arbitrage()}")
print(f"Potential Profit: {calc.profit}")
print(f"Return on Investment: {calc.roi}")
```

## Licence

Arbmaster is licensed under the MIT License.
