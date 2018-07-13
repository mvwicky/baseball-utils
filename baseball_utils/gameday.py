from datetime import datetime, timedelta
from functools import lru_cache, partial
from typing import Any, ByteString, Dict, Text, Tuple, Optional, ClassVar, List
from urllib.parse import urljoin, urlparse, urlunparse

import attr
from bs4 import BeautifulSoup, Tag
from requests import Session

from baseball_utils.savant import Savant
from baseball_utils.util import (
    create_soup,
    default_attrs,
    make_abs_url,
    base_url,
    CachedValue,
    home_away_vals,
)


class GamedayError(Exception):
    pass


MASTER_TIMEOUT = timedelta(minutes=1)


@default_attrs()
class GamedayData(object):
    """Represents the MLB gameday data for a specific date"""

    session: Session = attr.ib()
    savant: Savant = attr.ib()
    dt: datetime = attr.ib(factory=datetime.today)
    gd_base: ClassVar[Text] = 'http://gd.mlb.com'
    _master: CachedValue[BeautifulSoup] = attr.ib(
        default=CachedValue(MASTER_TIMEOUT)
    )

    @property
    def gameday_url(self) -> Text:
        url = '/'.join(
            (
                self.gd_base,
                'components',
                'game',
                'mlb',
                'year_{0:%Y}',
                'month_{0:%m}',
                'day_{0:%d}',
            )
        )
        return url.format(self.dt)

    @property
    def master_scoreboard(self) -> BeautifulSoup:
        if self._master.timed_out:
            self._master.clear()
        if not self._master.is_none():
            return self._master.get()

        res = self.session.get(self.gameday_url)
        res.raise_for_status()

        soup = create_soup(res.content)
        master_href: Optional[Text] = None
        for a in soup('a', href=True):
            if 'master_scoreboard.xml' in a['href']:
                master_href = a['href']
                break

        if master_href is None:
            raise GamedayError(
                'unable to find master scoreboard ({0})'.format(
                    self.gameday_url
                )
            )

        base = base_url(self.gameday_url)
        r = self.session.get(make_abs_url(base, master_href))
        r.raise_for_status()

        self._master.refresh(create_soup(r.content))
        return self._master.get()

    @property
    def games(self):
        """For convinience, we iterate over games a lot"""
        return (game for game in self.master_scoreboard('game'))

    def ip_games(self):
        """Yields 'game' elements for in-progress games"""
        for game in self.games:
            stat = game.find('status', ind=True)
            if stat is None:
                continue
            if stat['ind'] == 'I':
                yield game

    class BoxScore(object):
        pass

    def boxscores(self):
        """Yield a series of BoxScore objects for each in-progress or finished
        game
        """
        for game in self.ip_games():
            pass

    def linescores(self):
        for game in self.games:
            ls = game.find('linescore')
            if ls is None:
                continue
            yield Linescore(ls, game)
            continue
            line = Linescore(game['away_team_name'], game['home_team_name'])
            for inning in ls('inning', away=True, home=True):
                a_runs, h_runs = 0, 0
                if inning['away']:
                    a_runs = int(inning['away'])

                if inning['home']:
                    h_runs = int(inning['home'])

                line.innings.append({'away': a_runs, 'home': h_runs})
            h = ls.find('h')
            if h is None:
                continue
            a_hits, h_hits = 0, 0
            if h['away']:
                a_hits = int(h['away'])
            if h['home']:
                h_hits = int(h['home'])
            line.hits.update({'away': a_hits, 'home': h_hits})
            yield line


@default_attrs()
class Game(object):
    tag: Tag = attr.ib()


@default_attrs()
class Linescore(object):
    tag: Tag = attr.ib()
    game: Tag = attr.ib()

    def _innings(self) -> List[Dict[Text, int]]:
        ret = list()
        for inn in self.tag('inning', away=True, home=True):
            ret.append(home_away_vals(inn))
        return ret

    def __str__(self) -> Text:
        away, home = self.game['away_team_name'], self.game['home_team_name']
        innings = self._innings()
        hits = home_away_vals(self.tag.find('h'))
        errors = home_away_vals(self.tag.find('e'))
        long_team = max(map(len, (away, home)))

        runs = {
            'away': sum(e['away'] for e in innings),
            'home': sum(e['home'] for e in innings),
        }
        max_col = max(
            list(runs.values()) + list(hits.values()) + list(errors.values())
        )
        max_width = len(str(max_col))

        num_inn = max(len(innings), 9)

        def _box(i: Any) -> Text:
            b = '| ' + '{0:^' + str(max_width) + '} '
            return b.format(i)

        max_box_width = len(_box(max_col))
        line_width = long_team + (max_box_width * num_inn) + 2

        msg = []

        head = []
        head.append(' ' * (long_team + 1))
        for i in range(num_inn):
            head.append(_box(i + 1))

        head.append(_box('r'))
        head.append(_box('h'))
        head.append(_box('e'))
        head.append('|')

        msg.append(''.join(head))
        line_width = len(msg[-1])
        msg.append('-' * line_width)

        def make_line(t):
            if t == 'away':
                team = away
            else:
                team = home

            r = []
            r.append(team)
            r.append(' ' * (long_team - len(team) + 1))
            for inn in innings:
                r.append(_box(inn[t]))
            if len(innings) < 9:
                diff = 9 - len(innings)
                for _ in range(diff):
                    r.append(_box(''))
            r.append(_box(runs[t]))
            r.append(_box(hits[t]))
            r.append(_box(errors[t]))
            r.append('|')
            return ''.join(r)

        msg.append(make_line('away'))
        msg.append('-' * line_width)
        msg.append(make_line('home'))

        return '\n'.join(msg)


if __name__ == '__main__':
    pass
