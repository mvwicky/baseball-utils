"""Script to parse Retrosheet files"""
from datetime import datetime
from typing import Any, Iterator, List, Optional, Text, Type, cast

import attr

from baseball_utils.const import Retrosheet
from baseball_utils.types import CountType, TextStream
from baseball_utils.util import default_attrs, file_iter


def quoted_field(record: Text) -> Optional[Text]:
    if record[0] != '"' or record.count('"') < 2:
        return None

    next_q = record.find('"', 1)
    return record[1:next_q]


@default_attrs()
class Player(object):
    retro_id: Text = attr.ib()
    name: Text = attr.ib()
    home: bool = attr.ib()
    batting_pos: int = attr.ib()
    fielding_pos: int = attr.ib()

    @classmethod
    def from_record(cls: Type['Player'], record: Text) -> 'Player':
        rid, name, home, b, f = record.split(',')
        return cls(rid, name.strip('"'), (home == '1'), int(b), int(f))
        rlist = list(record)
        f = rlist.pop()  # pop last digit
        n = rlist.pop()  # comma or sub number
        if n.isnumeric():  # if player was a sub
            f = n + f  # number is 11 or 12
            rlist.pop()  # Ditch comma
        f = int(f)

        b = int(rlist.pop())
        rlist.pop()

        home = rlist.pop() == '1'
        rlist.pop()
        name_elems: List[Text] = []

        rlist.pop()  # Remove the trailing '"'
        while rlist[-1] != '"':
            name_elems.append(rlist.pop())
        name = ''.join(reversed(name_elems))
        rlist.pop()  # Get rid of the first '"'
        rlist.pop()  # Remove the delimiter

        rid = ''.join(rlist)
        return cls(rid, name, home, b, f)


@default_attrs()
class Event(object):
    """Retrosheet Event Description

    1st Part: 'description of the basic play'
    2nd Part: 'modifier for the 1st part'
    3rd Part: 'describes the advance of any runners'
    """

    cts: Text = attr.ib()

    @classmethod
    def from_field(cls: Type['Event'], field: Text) -> 'Event':
        pass


@default_attrs()
class Pitches(object):
    """Retrosheet Pitches field"""

    pitch_list: List[Text] = attr.ib(factory=list)

    def __len__(self) -> int:
        return len(self.pitch_list)


@default_attrs()
class Play(object):
    inning: int = attr.ib()
    home_team: bool = attr.ib()
    batter_id: Text = attr.ib()
    event: Event = attr.ib()
    count: Optional[CountType] = attr.ib(default=None)
    pitches: Optional[Pitches] = attr.ib(default=None)
    com: List[Text] = attr.ib(factory=list)

    @property
    def num_pitches(self) -> int:
        return len(self.pitches or [])

    @classmethod
    def from_record(cls: Type['Play'], record: Text) -> 'Play':
        inning, home, rid, cnt, ps, event = record.split(',')
        count: Optional[CountType] = None
        if cnt.isnumeric():
            count = cast(CountType, tuple(map(int, cnt))[:2])

        pitches: Optional[Pitches] = None
        if ps:
            pitches = Pitches(list(ps))

        return Play(int(inning), (home == '1'), rid, event, count, pitches)


@default_attrs()
class Info(object):
    visit_team: Text = attr.ib(default='unknown')
    home_team: Text = attr.ib(default='unknown')
    number: int = attr.ib(default=0, repr=False)
    start_dt: datetime = attr.ib(default=datetime.min)
    day: Optional[bool] = attr.ib(default=None, repr=False)
    used_dh: bool = attr.ib(default=False, repr=False)
    pitches: Optional[Text] = attr.ib(default=None, repr=False)
    ump_home_id: Text = attr.ib(default='unknown', repr=False)
    ump_first_id: Text = attr.ib(default='unknown', repr=False)
    ump_second_id: Text = attr.ib(default='unknown', repr=False)
    ump_third_id: Text = attr.ib(default='unknown', repr=False)
    ump_left_id: Optional[Text] = attr.ib(default=None, repr=False)
    ump_right_id: Optional[Text] = attr.ib(default=None, repr=False)
    field_cond: Optional[Text] = attr.ib(default=None)
    precip: Optional[Text] = attr.ib(default=None, repr=False)
    sky: Optional[Text] = attr.ib(default=None)
    temp: Optional[int] = attr.ib(default=None)
    wind_dir: Optional[Text] = attr.ib(default=None)
    wind_speed: Optional[int] = attr.ib(default=None)
    time_of_game: Optional[int] = attr.ib(default=None)
    attendance: Optional[int] = attr.ib(default=None)
    site: Text = attr.ib(default='unknown', repr=False)
    winning_pitcher: Text = attr.ib(default='unknown')
    losing_pitcher: Text = attr.ib(default='unknown')
    save_pitcher: Optional[Text] = attr.ib(default=None)
    gw_rbi: Optional[Text] = attr.ib(default=None, repr=False)

    def translate(self, retro_field: Text) -> Optional[Text]:
        """Translate a Retrosheet info field to a Info class field"""
        raise NotImplementedError

        if retro_field in attr.asdict(self):
            return retro_field

    def add_field(self, fields: Text) -> bool:
        info_type, info_value = fields.split(',', maxsplit=1)

        if info_type not in Retrosheet.info_types:
            return False

        info_field: Optional[Text] = None
        new_value: Optional[Any] = None
        if info_type.endswith('team'):
            if info_type == 'visteam':
                info_field = 'visit_team'
            elif info_type == 'hometeam':
                info_field = 'home_team'
        elif info_type == 'date':
            info_field = 'start_dt'
            ndt = datetime.strptime(info_value, '%Y/%m/%d')
            year, month, day = ndt.year, ndt.month, ndt.day
            new_value = self.start_dt.replace(year=year, month=month, day=day)
        elif info_type == 'number':
            info_field = 'number'
            new_value = int(info_value)
        elif info_type == 'starttime':
            if not info_value.startswith('0:00'):
                info_field = 'start_dt'
                ndt = datetime.strptime(info_value, '%I:%M%p')
                hour, minute = ndt.hour, ndt.minute
                new_value = self.start_dt.replace(hour=hour, minute=minute)
        elif info_type == 'daynight':
            info_field = 'day'
            new_value = info_value == 'day'
        elif info_type == 'usedh':
            info_field = 'used_dh'
            new_value = info_value == 'true'
        elif info_type.startswith('ump'):
            if info_type == 'umphome':
                info_field = 'ump_home_id'
            elif info_type == 'ump1b':
                info_field = 'ump_first_id'
            elif info_type == 'ump2b':
                info_field = 'ump_second_id'
            elif info_type == 'ump3b':
                info_field = 'ump_third_id'
            elif info_type == 'umplf':
                info_field = 'ump_left_id'
            elif info_type == 'umprf':
                info_field = 'ump_right_id'
        elif info_type == 'fieldcond':
            info_field = 'field_cond'
        elif info_type == 'temp':
            info_field = 'temp'
            new_value = int(info_value)
        elif info_type == 'winddir':
            info_field = 'wind_dir'
        elif info_type == 'windspeed':
            info_field = 'wind_speed'
            new_value = int(info_value)
            if new_value < 0:
                info_field = None
        elif info_type == 'timeofgame':
            info_field = 'time_of_game'
            new_value = int(info_value)
        elif info_type == 'attendance':
            info_field = 'attendance'
            new_value = int(info_value)
        elif info_type == 'wp':
            info_field = 'winning_pitcher'
        elif info_type == 'lp':
            info_field = 'losing_pitcher'
        elif info_type == 'save':
            info_field = 'save_pitcher'
        elif info_type == 'gwrbi':
            info_field = 'gw_rbi'
        else:
            info_field = info_type

        if info_field is not None and hasattr(self, info_field):
            if new_value is not None:
                setattr(self, info_field, new_value)
            else:
                setattr(self, info_field, info_value or None)
            return True
        return False


@default_attrs()
class Game(object):
    info: Info = attr.ib(factory=Info)
    starters: List[Player] = attr.ib(factory=list, repr=False)
    subs: List[Player] = attr.ib(factory=list, repr=False)
    plays: List[Play] = attr.ib(factory=list, repr=False)
    com: List[Text] = attr.ib(factory=list, repr=False)


# @profile
def parse(file: TextStream):
    games: List[Game] = []

    last_rec = None
    file_map: Iterator[Text] = map(lambda i: i.rstrip(), file)
    for line in file_iter(file, strip=True):
        assert isinstance(line, Text)
        rec_type, fields = line.split(',', maxsplit=1)
        if rec_type not in Retrosheet.record_types:
            continue

        if rec_type == 'id':
            games.append(Game())
        elif rec_type == 'version':
            # version field (ignore)
            pass
        elif rec_type == 'info':
            games[-1].info.add_field(fields)
        elif rec_type == 'start':
            games[-1].starters.append(Player.from_record(fields))
        elif rec_type == 'sub':
            games[-1].subs.append(Player.from_record(fields))
        elif rec_type == 'play':
            games[-1].plays.append(Play.from_record(fields))
        elif rec_type == 'com':
            com = fields.strip('"').lstrip('$')
            if last_rec is not None and last_rec == 'play':
                games[-1].plays[-1].com.append(com)
            else:
                games[-1].com.append(com)
        last_rec = rec_type
    return games


def teams(year):
    pass
