import enum
from typing import (
    BinaryIO,
    ByteString,
    Dict,
    FrozenSet,
    Generator,
    Text,
    TextIO,
    Tuple,
    Union,
)

from mypy_extensions import TypedDict

# Define Types

# const.py
FPDictType = Dict[int, Text]
FPSetType = FrozenSet[Tuple[int, Text]]

# retrosheet.py
TextStream = TextIO
AnyStream = Union[TextIO, BinaryIO]
CountType = Tuple[int, int]

# util.py
BytesIterGen = Generator[ByteString, None, None]
TextIterGen = Generator[Text, None, None]
FileIterGen = Union[BytesIterGen, TextIterGen]

# savant.py
IdDict = Dict[Text, Tuple[Text, Text]]

# fangraphs.py
FGParams = TypedDict(
    'FGParams',
    {
        'pos': str,
        'stats': enum.Enum,
        'lg': enum.Enum,
        'qual': Union[Text, int],
        'type': enum.Enum,
        'season': int,
        'month': int,
        'season1': int,
        'ind': int,
    },
)
TempParams = Dict[Text, Union[Text, int]]

# download.py
Path = Text
