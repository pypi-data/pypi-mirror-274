
DEFAULT_HEADERS: "dict[str, str]" = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Arbmaster v1.0.0"
}

DEFAULT_BOOKMAKERS: "list[str]" = [
    "sport888", "leovegas", "betsson", "betway",
    "nordicbet", "pinnacle", "mrgreen", "casumo", "coolbet"
]

DEFAULT_REQUESTS_REMAINING: int = 500

LEAGUES: "list[dict[str, str]]" = [
  {
    "key": "basketball_euroleague",
    "group": "Basketball",
    "title": "Euroleague",
    "country": "International"
  },
  {
    "key": "basketball_nba",
    "group": "Basketball",
    "title": "NBA",
    "country": "USA"
  },
  {
    "key": "basketball_wnba",
    "group": "Basketball",
    "title": "WNBA",
    "country": "USA"
  },
  {
    "key": "icehockey_nhl",
    "group": "Ice Hockey",
    "title": "NHL",
    "country": "USA"
  },
  {
    "key": "icehockey_sweden_allsvenskan",
    "group": "Ice Hockey",
    "title": "HockeyAllsvenskan",
    "country": "Sweden"
  },
  {
    "key": "icehockey_sweden_hockey_league",
    "group": "Ice Hockey",
    "title": "SHL",
    "country": "Sweden"
  },
  {
    "key": "soccer_australia_aleague",
    "group": "Soccer",
    "title": "A-League",
    "country": "Australia"
  },
  {
    "key": "soccer_austria_bundesliga",
    "group": "Soccer",
    "title": "Bundesliga",
    "country": "Austria"
  },
  {
    "key": "soccer_brazil_campeonato",
    "group": "Soccer",
    "title": "Serie A",
    "country": "Brazil"
  },
  {
    "key": "soccer_brazil_serie_b",
    "group": "Soccer",
    "title": "Serie B",
    "country": "Brazil"
  },
  {
    "key": "soccer_chile_campeonato",
    "group": "Soccer",
    "title": "Primera Division",
    "country": "Chile"
  },
  {
    "key": "soccer_china_superleague",
    "group": "Soccer",
    "title": "Super League",
    "country": "China"
  },
  {
    "key": "soccer_conmebol_copa_america",
    "group": "Soccer",
    "title": "Copa America",
    "country": "International"
  },
  {
    "key": "soccer_conmebol_copa_libertadores",
    "group": "Soccer",
    "title": "Copa Libertadores",
    "country": "International"
  },
  {
    "key": "soccer_denmark_superliga",
    "group": "Soccer",
    "title": "Superliga",
    "country": "Denmark"
  },
  {
    "key": "soccer_efl_champ",
    "group": "Soccer",
    "title": "Championship",
    "country": "England"
  },
  {
    "key": "soccer_england_league1",
    "group": "Soccer",
    "title": "League One",
    "country": "England"
  },
  {
    "key": "soccer_england_league2",
    "group": "Soccer",
    "title": "League 2",
    "country": "England"
  },
  {
    "key": "soccer_epl",
    "group": "Soccer",
    "title": "Premier League",
    "country": "England"
  },
  {
    "key": "soccer_fa_cup",
    "group": "Soccer",
    "title": "FA Cup",
    "country": "England"
  },
  {
    "key": "soccer_finland_veikkausliiga",
    "group": "Soccer",
    "title": "Veikkausliiga",
    "country": "Finland"
  },
  {
    "key": "soccer_france_ligue_one",
    "group": "Soccer",
    "title": "Ligue 1",
    "country": "France"
  },
  {
    "key": "soccer_france_ligue_two",
    "group": "Soccer",
    "title": "Ligue 2",
    "country": "France"
  },
  {
    "key": "soccer_germany_bundesliga",
    "group": "Soccer",
    "title": "Bundesliga",
    "country": "Germany"
  },
  {
    "key": "soccer_germany_bundesliga2",
    "group": "Soccer",
    "title": "2. Bundesliga",
    "country": "Germany"
  },
  {
    "key": "soccer_germany_liga3",
    "group": "Soccer",
    "title": "3. Liga",
    "country": "Germany"
  },
  {
    "key": "soccer_greece_super_league",
    "group": "Soccer",
    "title": "Super League",
    "country": "Greece"
  },
  {
    "key": "soccer_italy_serie_a",
    "group": "Soccer",
    "title": "Serie A",
    "country": "Italy"
  },
  {
    "key": "soccer_italy_serie_b",
    "group": "Soccer",
    "title": "Serie B",
    "country": "Italy"
  },
  {
    "key": "soccer_japan_j_league",
    "group": "Soccer",
    "title": "J1 League",
    "country": "Japan"
  },
  {
    "key": "soccer_korea_kleague1",
    "group": "Soccer",
    "title": "K League 1",
    "country": "Korea"
  },
  {
    "key": "soccer_league_of_ireland",
    "group": "Soccer",
    "title": "Premier Division",
    "country": "Ireland"
  },
  {
    "key": "soccer_mexico_ligamx",
    "group": "Soccer",
    "title": "Liga MX",
    "country": "Mexico"
  },
  {
    "key": "soccer_netherlands_eredivisie",
    "group": "Soccer",
    "title": "Eredivisie",
    "country": "Netherlands"
  },
  {
    "key": "soccer_norway_eliteserien",
    "group": "Soccer",
    "title": "Eliteserien",
    "country": "Norway"
  },
  {
    "key": "soccer_poland_ekstraklasa",
    "group": "Soccer",
    "title": "Ekstraklasa",
    "country": "Poland"
  },
  {
    "key": "soccer_portugal_primeira_liga",
    "group": "Soccer",
    "title": "Liga Portugal",
    "country": "Portugal"
  },
  {
    "key": "soccer_spain_la_liga",
    "group": "Soccer",
    "title": "LaLiga",
    "country": "Spain"
  },
  {
    "key": "soccer_spain_segunda_division",
    "group": "Soccer",
    "title": "LaLiga 2",
    "country": "Spain"
  },
  {
    "key": "soccer_spl",
    "group": "Soccer",
    "title": "Scottish Premiership",
    "country": "Scotland"
  },
  {
    "key": "soccer_sweden_allsvenskan",
    "group": "Soccer",
    "title": "Allsvenskan",
    "country": "Sweden"
  },
  {
    "key": "soccer_sweden_superettan",
    "group": "Soccer",
    "title": "Superettan",
    "country": "Sweden"
  },
  {
    "key": "soccer_switzerland_superleague",
    "group": "Soccer",
    "title": "Super League",
    "country": "Switzerland"
  },
  {
    "key": "soccer_turkey_super_league",
    "group": "Soccer",
    "title": "Super Lig",
    "country": "Turkey"
  },
  {
    "key": "soccer_uefa_champs_league",
    "group": "Soccer",
    "title": "Champions League",
    "country": "International"
  },
  {
    "key": "soccer_uefa_europa_conference_league",
    "group": "Soccer",
    "title": "Europa Conference League",
    "country": "International"
  },
  {
    "key": "soccer_uefa_europa_league",
    "group": "Soccer",
    "title": "Europa League",
    "country": "International"
  },
  {
    "key": "soccer_uefa_european_championship",
    "group": "Soccer",
    "title": "Euro 2024",
    "country": "International"
  },
  {
    "key": "soccer_usa_mls",
    "group": "Soccer",
    "title": "MLS",
    "country": "USA"
  }
]
