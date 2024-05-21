"""
Holds the function to get a Comtrade object which can be used to access data in np arrays. The data is parsed using
the C# parser.
Memory is tentatively kept to a minimum.
"""
import os
import sys
from importlib import resources
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

import clr
import numpy as np

here = os.path.dirname(__file__)


with resources.path("comtrade_pysharp", "ReaderDll.dll") as p:
    path = str(p)
    sys.path.append(path)
    clr.AddReference(path)

from ReaderDll import Reader  # always red, unclear if there's a way to clear this.


@dataclass
class Comtrade:
    """
    Holder for data
    """
    timestamps: list[datetime]
    analog: Dict[str, np.array]
    digital: Dict[str, np.array]
    analog_names: List[str]
    digital_names: List[str]


def read_comtrade(filename: Union[str, Path]) -> Comtrade:
    """
    Reads the file at filename and returns a Comtrade object containing its data
    :param filename:
    :return:
    """
    reader = Reader(str(filename))
    timestamps = [datetime.fromtimestamp(timestamp) for timestamp in reader.timestamps]
    analog = {}
    for n, name in enumerate(reader.analog_names):
        analog[name] = np.array(reader.analog_data[n])
    analog_names = reader.analog_names

    digital = {}
    for n, name in enumerate(reader.digital_names):
        digital[name] = np.array(reader.digital_data[n])
    digital_names = reader.digital_names

    reader.Clear()
    return Comtrade(timestamps=timestamps,
                    analog=analog,
                    digital=digital,
                    analog_names=analog_names,
                    digital_names=digital_names,
                    )

