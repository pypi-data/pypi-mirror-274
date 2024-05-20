from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Any, NewType, List, Dict

from arbmaster.calc import ArbitrageCalc

StrPath = NewType("StrPath", str)

@dataclass
class Bookmaker:
    key: str
    title: str
    home_odds: float
    away_odds: float
    draw_odds: Optional[float] = None

    @classmethod
    def new(cls, hteam: str, bm_data: Dict[str, Any]) -> "Bookmaker":
        key: str = bm_data['key']
        title: str = bm_data['title']
        outcomes = bm_data['markets'][0]['outcomes']
        
        if hteam == outcomes[0]['name']:
            home_odds: float = outcomes[0]['price']
            away_odds: float = outcomes[1]['price']
        else:
            home_odds: float = outcomes[1]['price']
            away_odds: float = outcomes[0]['price']
        
        draw_odds: Optional[float] = None
        if len(outcomes) == 3:
            draw_odds = outcomes[2]['price']
        return cls(key, title, home_odds, away_odds, draw_odds)

    def json(self, price) -> Dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "price": price
        }

class Odds:
    def __init__(self, bookmakers: List[Bookmaker]) -> None:
        home = max([b.home_odds for b in bookmakers if b.home_odds is not None], default=None)
        away = max([b.away_odds for b in bookmakers if b.away_odds is not None], default=None)
        draw = max([b.draw_odds for b in bookmakers if b.draw_odds is not None], default=None)
        
        self.home = [bm.json(home) for bm in bookmakers if bm.home_odds == home] if home is not None else []
        self.away = [bm.json(away) for bm in bookmakers if bm.away_odds == away] if away is not None else []
        self.draw = [bm.json(draw) for bm in bookmakers if bm.draw_odds == draw] if draw is not None else []

    @classmethod
    def new(cls, odds_data: Dict[str, Any]) -> "Odds":
        home = [Bookmaker(bm['key'], bm['title'], bm['price'], 0) for bm in odds_data['home_team']]
        away = [Bookmaker(bm['key'], bm['title'], 0, bm['price'], 0) for bm in odds_data['away_team']]
        draw = [Bookmaker(bm['key'], bm['title'], 0, 0, bm['price']) for bm in odds_data['draw'] if len(odds_data['draw']) >= 1]
        bookmakers = home + away + draw
        return cls(bookmakers)
        
    def json(self) -> Dict[str, Any]:
        return {
            "home_team": self.home,
            "away_team": self.away,
            "draw": self.draw
        }

class Match:
    def __init__(self, match_data: Dict[str, Any], stake: float = 100) -> None:
        self.id: str = match_data['id']
        self.sport_key: str = match_data['sport_key']
        self.sport_title: str = match_data['sport_title']
        self.home_team: str = match_data['home_team']
        self.away_team: str = match_data['away_team']
        
        if match_data.get("bookmakers", None) is not None:
            odds: Odds = Odds([Bookmaker.new(self.home_team, b) for b in match_data['bookmakers']])
            commence_time: str = make_europe_time(match_data['commence_time'])
        elif match_data.get("odds", None) is not None:
            odds: Odds = Odds.new(match_data['odds'])
            commence_time: str = match_data['commence_time']
        
        self.commence_time: str = commence_time
        self.odds: Odds = odds
        
        calc: ArbitrageCalc = ArbitrageCalc(odds.json(), stake=stake)
        self.is_arbitrage: bool = calc.is_arbitrage()
        self.stakes: List[float] = calc.stakes
        self.payout: float = calc.payout
        self.profit: float = calc.profit
        self.roi: str = calc.roi
    
    def json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sport_key": self.sport_key,
            "sport_title": self.sport_title,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "commence_time": self.commence_time,
            "odds": self.odds.json() if isinstance(self.odds, Odds) else self.odds
        }
    
def make_europe_time(utc_str: str) -> str:
    utc_time = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ")
    start = datetime(utc_time.year, 3, 31, 2, 0)
    end = datetime(utc_time.year, 10, 31, 3, 0)
    
    if start <= utc_time < end:
        offset = timedelta(hours=2)
    else:
        offset = timedelta(hours=1)
    
    time = utc_time + offset
    return time.strftime("%Y-%m-%dT%H:%M:%S")