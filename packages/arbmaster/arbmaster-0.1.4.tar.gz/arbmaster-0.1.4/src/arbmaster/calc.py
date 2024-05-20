from typing import Dict, List

class ArbitrageCalc:
    
    def __init__(self, odds: Dict[str, list], stake: float = 100) -> None:        
        self.odds = [v[0]["price"] for v in odds.values() if len(v) >= 1]
        self.probability: float = self._calc_prob(self.odds)
        
        self.stakes: List[float] = self._calc_stakes(stake)
        self.payout: float = self._calc_payout()
        self.profit: float = self._calc_profit()
        self.roi: str = self._calc_roi()
    
    def is_arbitrage(self) -> bool:
        return 0 < self.probability < 1
    
    def _calc_prob(self, odds) -> float:
        p = 0.0
        for odd in odds:
            if odd is not None:
                p += 1 / odd
        return p
    
    def _calc_stakes(self, stake: float) -> List[float]:
        stakes: List[float] = []
        for odd in self.odds:
            if self.is_arbitrage():
                bet = (stake * (1 / odd)) / self.probability
                stakes.append(bet)
        return stakes
    
    def _calc_payout(self) -> float:
        payout: float = 0.0
        if self.is_arbitrage():
            for odd, stake in zip(self.odds, self.stakes):
                payout = stake * odd
        return round(payout, 2)
    
    def _calc_profit(self) -> float:
        return round(self.payout - sum(self.stakes), 2) if self.is_arbitrage() else 0.0
    
    def _calc_roi(self) -> str:
        return "{:.2f}%".format((self.profit / sum(self.stakes)) * 100) if self.is_arbitrage() else "0.0%"