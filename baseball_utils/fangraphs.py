import copy
import enum
import functools
from datetime import datetime
from typing import Any, Dict, Optional, Text, Tuple, Union, cast

from bs4 import BeautifulSoup
from mypy_extensions import TypedDict
from requests import Session

from .types import FGParams, TempParams
from .util import THIS_YEAR


@enum.unique
class League(enum.Enum):
    NL = ('nl',)
    AL = ('al',)
    ALL = 'all'


@enum.unique
class Stats(enum.Enum):
    BAT = 'bat'
    PIT = 'pit'


@enum.unique
class StatType(enum.Enum):
    DASHBOARD = 8
    STANDARD = 0
    ADVANCED = 1
    BATTED_BALL = 2
    WIN_PROB = 3
    PITCH_TYPE = 4
    PITCH_VALUE = 7
    PLATE_DISCIPLINE = 5
    VALUE = 6
    PI_PITCH_TYPE = 16
    PI_VELO = 17
    PI_H_MOVEMENT = 18
    PI_V_MOVEMENT = 19
    PI_VALUE = 20
    PI_VALUE_PER_C = 21
    PI_PLATE_DISCIPLINE = 22


NUM_STATS = len(StatType)


class Fangraphs(object):
    url: Text = 'https://fangraphs.com/leaders.aspx'

    ParamsType = TypedDict(
        'ParamsType',
        {
            'pos': str,
            'stats': Stats,
            'lg': League,
            'qual': Union[Text, int],
            'type': StatType,
            'season': int,
            'month': int,
            'season1': int,
            'ind': int,
        },
    )

    Params: FGParams = {
        'pos': 'all',
        'stats': Stats.PIT,
        'lg': League.ALL,
        'qual': 'y',
        'type': StatType.DASHBOARD,
        'season': 2018,
        'month': 0,
        'season1': 2018,
        'ind': 0,
    }

    def __init__(self, session: Session) -> None:
        self.session = session

    @classmethod
    def convert_params(cls, params) -> Dict[Text, Text]:
        ret = copy.copy(params)
        for k in ret:
            ret[k] = str(ret[k])
        return ret

    def fetch_stats(
        self,
        pos: Stats,
        qual: Union[Text, int] = 'y',
        lg: League = League.ALL,
        stat_type: StatType = StatType.DASHBOARD,
        start_season: int = THIS_YEAR,
        end_season: int = THIS_YEAR,
    ) -> Any:
        """Fetch statistics for a certain position

        :param pos: type of position for which stats are fetched ('pit' or 'bat')
        :param qual: minimum number of PA/IP or 'y' for qualified players only
        :param lg: restrict stats to a certain league (AL or NL)
        :param stat_type: specify the 'category' of stats to fetch
        :param start_season: low end of range to fetch
        :param end_season: high end of range to fetch
        """
        params = copy.copy(cast(TempParams, self.Params))
        # params = copy.copy(self.Params)
        params['stats'] = pos.value
        params['qual'] = qual
        params['lg'] = lg.value
        params['type'] = stat_type.value
        assert end_season >= start_season
        params['season'] = end_season
        params['season1'] = start_season
        res = self.session.get(self.url, params=self.convert_params(params))
        return res

    @functools.lru_cache(maxsize=NUM_STATS)
    def rows(self, pos: Stats, stat_type: StatType) -> Tuple[Text, ...]:
        """Returns a tuple representing the names of the rows for each category

        TODO: cache the result in some way
        """
        res = self.fetch_stats(pos, stat_type=stat_type)
        # TODO: Do an actual check, don't just dump out
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'lxml')
        att = {'scope': 'col', 'class': 'rgHeader'}
        return tuple([th.string for th in soup('th', attrs=att)])

    def batter_stats(
        self,
        qual: Union[Text, int] = 'y',
        lg: League = League.ALL,
        stat_type: StatType = StatType.DASHBOARD,
        season: int = THIS_YEAR,
    ) -> Any:
        stats = self.fetch_stats(Stats.BAT, qual, lg, stat_type, season)


if __name__ == '__main__':
    fg = Fangraphs(Session())

    for pos in Stats:
        for st in StatType:
            print(st.name, end='\t')
            print(fg.rows(pos, st))
