from datetime import datetime

import attr
from requests import Session

from baseball_utils.gameday import GamedayData
from baseball_utils.savant import Savant
from baseball_utils.util import SESSION, default_attrs


def get_today():
    td = Today(SESSION)

    return td.probables()


@default_attrs()
class Today(object):
    session: Session = attr.ib()
    gd: GamedayData = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.gd = GamedayData(self.session, Savant(self.session))

    def probables(self):
        pass


if __name__ == '__main__':
    pass
