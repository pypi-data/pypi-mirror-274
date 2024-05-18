from typing import Optional, Literal, List, Dict, Any

from requests import Session, Response
from requests_cache import (
    CachedSession,
    BackendSpecifier,
    SerializerType,
    DEFAULT_CACHE_NAME,
    StrOrPath,
)

from arbmaster.ext import Match
from arbmaster.logger import logger
from arbmaster.constants import (
    DEFAULT_HEADERS, 
    DEFAULT_BOOKMAKERS,
    DEFAULT_REQUESTS_REMAINING,
    LEAGUES
)


class Client:
    
    #: Odds api url
    url: str = "https://api.the-odds-api.com/v4/sports/{}/odds"

    #: Available leagues to fetch
    _leagues = LEAGUES
    
    def __init__(self,
                 api_key: str,
                 *,
                 params: Optional[Dict[str, str]] = None,
                 headers: Dict[str, str] = DEFAULT_HEADERS,
                 bookmakers: List[str] = DEFAULT_BOOKMAKERS,
                 requests_remaining: int = DEFAULT_REQUESTS_REMAINING,
                 use_cache: Optional[bool] = None,
                 cache_name: Optional[StrOrPath] = DEFAULT_CACHE_NAME,
                 expire_after: Optional[Any] = -1,
                 cache_backend: Optional[BackendSpecifier] = None,
                 serializer: Optional[SerializerType] = None
                ) -> None:
        
        self.api_key = api_key
        self.params = params or self._make_params(api_key, bookmakers)
        if "apiKey" not in self.params.keys():
            self.update_params(apiKey=api_key)
        
        self.headers = headers
        self.bookmakers = bookmakers
        self.requests_remaining: int = requests_remaining
        
        if use_cache:
            self.session: CachedSession = CachedSession(cache_name=cache_name,
                                                        backend=cache_backend,
                                                        serializer=serializer,
                                                        expire_after=expire_after)
        else:
            self.session: Session = Session()
    
    def _make_params(self,
                     api_key: str, 
                     bookmakers: List[str]
                    ) -> Dict[str, str]:
        params = {"apiKey": api_key}
        bm = []
        for bookmaker in bookmakers:
            bm.append(bookmaker.lower())
        
        bm_str = ",".join(bm)
        params.update({"bookmakers": bm_str})
        return params
    
    def add_bookmakers(self, *names: str) -> None:
        for name in names:
            if name not in self.bookmakers:
                self.bookmakers.append(name)
        
        bm_str = ",".join(self.bookmakers)
        self.update_params(bookmakers=bm_str)
    
    def update_params(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.params.update({k: v})
    
    def update_headers(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.headers.update({k: v})
    
    def parse_response(self, response: Response, stake: float) -> Optional[List[Match]]:
        self.requests_remaining = int(response.headers.get("x-requests-remaining", 0))
        body: List[dict] = response.json()
        matches: List[Match] = []
        
        for match_data in body:
            match: Match = Match(match_data, stake=stake)
             
            if match.is_arbitrage:
                matches.append(match)
        
        return matches if matches else None
    
    def fetch_league(self, 
                     key: str,
                     stake: float = 100,
                     timeout: Optional[float] = None) -> Optional[List[Match]]:
        if self.requests_remaining >= 2:
            url = self.url.format(key)
            resp: Response = self.session.get(url=url,
                                              params=self.params,
                                              headers=self.headers,
                                              timeout=timeout)
            
            if resp.status_code == 200:
                logger.info(f"Successfully fetched odds for league '{key}'.")
                return self.parse_response(response=resp, stake=stake)
            elif resp.status_code == 429:
                logger.error("Rate Limit exceeded. We recommend spacing out requests over several seconds.")
            elif resp.status_code == 401:
                logger.error("Unauthorized, Check that the api key is valid")
            else:
                logger.error(f"Error: {resp.status_code}")
        else:
            logger.error("There are no requests remaining. Change/update the API key")

    def fetch_all(self,
                stake: float = 100,
                leagues: Optional[List[Dict[str, str]]] = None,
                timeout: Optional[float] = None) -> List[Optional[List[Match]]]:
        result = []
        leagues_list = leagues or LEAGUES
        for league in leagues_list:
            resp = self.fetch_league(league['key'], stake, timeout=timeout)
            if resp is not None:
                result.append(resp)
        return result
    
    def fetch_sport(self,
                    sport: Literal["soccer", "basketball", "icehockey"],
                    stake: float = 100,
                    timeout: Optional[float] = None
                    ) -> List[Optional[List[Match]]]:
        result = []
        for league in LEAGUES:
            league_sport = league['key'].split('_')[0]
            if league_sport == sport.lower():
                resp = self.fetch_league(league["key"], stake, timeout=timeout)
                if resp is not None:
                    result.append(resp)
        return result