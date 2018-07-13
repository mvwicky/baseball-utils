import sys
import os
from typing import Text, List, Dict

import attr

from baseball_utils.download import retrosheet_seasons
from baseball_utils.retrosheet import parse, Game
from baseball_utils.util import default_attrs


@default_attrs()
class RetrosheetData(object):
    retro_dir: Text = attr.ib()
    _yd: List[Text] = attr.ib(factory=list, repr=False)
    _gms: Dict[int, List[Game]] = attr.ib(factory=dict, repr=False)

    @property
    def zip_dir(self):
        return os.path.join(self.retro_dir, 'events', 'raw')

    @property
    def data_dir(self) -> Text:
        return os.path.join(self.retro_dir, 'events', 'data')

    @property
    def year_dirs(self) -> List[Text]:
        if not self._yd or not os.listdir(self.retro_dir):
            self._yd = retrosheet_seasons(
                self.retro_dir, self.zip_dir, self.data_dir
            )
        return self._yd

    @property
    def years(self) -> Dict[int, Text]:
        ret = dict()
        for folder in self.year_dirs:
            name = os.path.split(folder)[1]
            ret[int(name[:4])] = folder
        return ret

    def event_files(self, year: int):
        assert year in self.years
        folder = self.years[year]
        ret = []
        for elem in os.listdir(folder):
            if elem.endswith('.EVA') or elem.endswith('.EVN'):
                path = os.path.join(folder, elem)
                ret.append(path)
        return ret

    def games(self, year: int):
        assert year in self.years
        if year not in self._gms or not self._gms[year]:
            self._gms[year] = list()
            for file in self.event_files(year):
                with open(file) as f:
                    self._gms[year].extend(parse(f))
        return self._gms[year]


def main():
    print(sys.implementation)
    print(sys.executable)

    retro_dir = os.path.join('f:\\local_scratch', 'retrosheet')
    data = RetrosheetData(retro_dir)
    for year in range(2010, 2018):
        print(year, len(data.games(year)))


if __name__ == '__main__':
    main()
