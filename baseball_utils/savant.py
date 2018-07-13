from datetime import timedelta
from typing import ClassVar, Dict, Text, Tuple, Set, cast

import attr
from requests import Session

from baseball_utils.types import IdDict
from baseball_utils.util import create_soup, default_attrs, CachedValue

ID_TIMEOUT = timedelta(days=1)
NAME_TIMEOUT = timedelta(days=365)


@default_attrs()
class Savant(object):
    url: ClassVar[Text] = 'https://baseballsavant.mlb.com/statcast_search'
    session: Session = attr.ib()
    _ids: CachedValue[IdDict] = attr.ib(default=CachedValue(ID_TIMEOUT))
    _names: CachedValue[Set[Text]] = attr.ib(default=CachedValue(NAME_TIMEOUT))

    @property
    def ids(self) -> IdDict:
        if self._ids.timed_out:
            self._ids.clear()
        if not self._ids.is_none():
            return self._ids.get()

        res = self.session.get(self.url)
        res.raise_for_status()
        soup = create_soup(res.content)
        attrs = {
            'class': 'form-control chosen-select',
            'id': 'batters_lookup',
            'name': 'batters_lookup[]',
        }
        select = soup.find('select', attrs=attrs)
        assert select is not None
        ret = dict()
        for opt in select('option', value=True):
            name = tuple(map(str.strip, opt.string.split(',')))
            ret[opt['value']] = cast(Tuple[str, str], name)
        self._ids.refresh(ret)

        return self._ids.get()

    @property
    def team_names(self) -> Set[Text]:
        if self._names.timed_out:
            self._names.clear()
        if not self._names.is_none:
            return self._names.get()

        res = self.session.get(self.url)
        res.raise_for_status()
        soup = create_soup(res.content)
        attrs = {'class': 'form-control', 'id': 'stadium', 'name': 'stadium'}
        select = soup.find('select', attrs=attrs)
        assert select is not None
        ret = set()
        for opt in select('option', value=True):
            name = opt.string.strip()
            if name:
                ret.add(name)
        self._names.refresh(ret)

        return self.team_names

    def longest_team_name(self) -> Text:
        return max(self.team_names, key=len)
