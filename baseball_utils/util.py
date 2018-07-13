import functools
from datetime import datetime, timedelta
from typing import (
    Any,
    BinaryIO,
    ByteString,
    Dict,
    FrozenSet,
    Generator,
    Generic,
    Optional,
    Text,
    TextIO,
    TypeVar,
    Union,
    cast,
)
from urllib.parse import urljoin, urlparse, urlunparse

import attr
import requests
from bs4 import BeautifulSoup, Tag

from baseball_utils.types import AnyStream, BytesIterGen, FileIterGen


SESSION = requests.Session()

THIS_YEAR = datetime.now().year

utf8open = functools.partial(open, encoding='utf-8')


PARSER = 'lxml'


def create_soup(content: ByteString) -> BeautifulSoup:
    return BeautifulSoup(content, PARSER)


def default_attrs():
    return attr.s(slots=True, auto_attribs=True)


def home_away_vals(t: Optional[Tag]) -> Dict[Text, int]:
    ret = {'away': 0, 'home': 0}
    if t is not None:
        for elem in ('away', 'home'):
            if elem in t.attrs and t[elem]:
                ret[elem] = int(t[elem])

    return ret


def base_url(url: str) -> str:
    parsed = urlparse(url)._asdict()
    parsed['path'] = '/'.join(parsed['path'].split('/')[:-1]) + '/'

    return urlunparse(tuple(v for v in parsed.values()))


def make_abs_url(base: str, href: str) -> str:
    parsed = urlparse(href)._asdict()
    if not parsed['netloc']:
        return urljoin(base, href)

    if not parsed['scheme']:
        parsed['scheme'] = urlparse(base).scheme

        return urlunparse(tuple(v for v in parsed.values()))

    return href


def file_iter(
    file: Union[Text, AnyStream],
    mode: Text = 'rt',
    *,
    strip: bool = False,
    chunk_size: int = 1024
) -> FileIterGen:
    if isinstance(file, TextIO):
        # Text File
        for line in file:
            if strip:
                line = line.strip()
            yield line

    elif isinstance(file, BinaryIO):
        # Binary File
        cts = file.read(chunk_size)
        while cts:
            yield cts

            cts = file.read(chunk_size)
    else:
        # Got a file name
        with open(file, mode) as f:
            f = cast(AnyStream, f)
            return file_iter(f, mode, strip=strip, chunk_size=chunk_size)


F = TypeVar('F')


def make_frozen(*args: F) -> FrozenSet[F]:
    return frozenset(args)


T = TypeVar('T')


@attr.s(auto_attribs=True)
class CachedValue(Generic[T]):
    """Encapsulates a value which is cached and periodically refreshed

        Pretty DIY compared to some solutions out there, but it works with
    slotted 'attrs' classes.
    """

    timeout: timedelta = attr.ib()  # TTL for value
    value: Optional[T] = attr.ib(default=None)  # The actual value
    last: datetime = attr.ib(default=datetime.min)  # Last update time

    @property
    def timed_out(self) -> bool:
        """Have we timed out?"""
        return datetime.now() - self.last >= self.timeout

    def is_none(self) -> bool:
        """Are we even storing a value?"""
        return self.value is None

    def get(self) -> T:
        return cast(T, self.value)

    def clear(self) -> None:
        """Reset the stored value to None"""
        self.value = None

    def refresh(self, val: T) -> None:
        """Reset last update time and set a new value"""
        self.last = datetime.now()
        self.value = val
