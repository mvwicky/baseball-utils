from datetime import datetime
from typing import FrozenSet, Text, ClassVar

from baseball_utils.types import FPDictType
from baseball_utils.util import make_frozen


FieldingPos: FPDictType = {
    1: 'Pitcher',
    2: 'Catcher',
    3: 'First Base',
    4: 'Second Base',
    5: 'Third Base',
    6: 'Shortstop',
    7: 'Left Field',
    8: 'Center Field',
    9: 'Right Field',
    10: 'Designated Hitter',
}


class Gameday(object):
    url = 'http:// ' + '/'.join(
        (
            'gd.mlb.com',
            'components',
            'game',
            'mlb',
            'year_2018',
            'month_06',
            'day_22',
            'gid_2018_06_22_tormlb_anamlb_1',
            'inning',
            'inning_all.xml',
        )
    )


class Retrosheet(object):
    """Constants associated with Retrosheet event file parsing

    id: id,<team:3><year:3><month:2><day:2><num:1>
    """

    record_types: ClassVar[FrozenSet[Text]] = make_frozen(
        'id',
        'version',
        'info',
        'start',
        'play',
        'sub',
        'com',
        'data',
        'badj',
        'padj',
    )
    info_types: ClassVar[FrozenSet[Text]] = make_frozen(
        'visteam',
        'hometeam',
        'date',
        'number',
        'starttime',
        'daynight',
        'usedh',
        'pitches',
        'umphome',
        'ump1b',
        'ump2b',
        'ump3b',
        'umplf',
        'umprf',
        'fieldcond',
        'precip',
        'sky',
        'temp',
        'winddir',
        'windspeed',
        'timeofgame',
        'attendance',
        'site',
        'wp',
        'lp',
        'save',
        'gwrbi',
        'edittime',
        'howscored',
        'inputprogvers',
        'inputter',
        'inputtime',
        'scorer',
        'translator',
    )
    pitch_types: ClassVar[FrozenSet[Text]] = make_frozen(
        'B',
        'C',
        'F',
        'H',
        'I',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'X',
        'Y',
    )
    # ID record fields
    team_s: ClassVar[slice] = slice(3)
    assert team_s.stop is not None
    year_s: ClassVar[slice] = slice(team_s.stop, team_s.stop + 4)
    assert year_s.stop is not None
    month_s: ClassVar[slice] = slice(year_s.stop, year_s.stop + 2)
    assert month_s.stop is not None
    day_s = slice(month_s.stop, month_s.stop + 2)
    assert day_s.stop is not None
    eve_base = 'http://www.retrosheet.org/events'

    years: ClassVar[range] = range(1921, datetime.today().year)

    @classmethod
    def event_url(cls, year: int) -> Text:
        assert year in cls.years
        return cls.eve_base + '/' + '{0}eve.zip'.format(year)
