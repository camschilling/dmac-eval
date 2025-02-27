"""Stores utilities related to result objects."""
from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Result:
    """
    Dataclass to hold results.

    Required constructor attributes:

    :param name: name of the result
    :type name: str

    Additional attributes that may be added:

    :param value: value of the result
    :type value: float or int
    :param dictionary: dictionary of items associated with the result.
        may be a log or additional relevant details
    :type dictionary: dict
    :param dataframe: dataframe supporting the result
    :type dataframe: pd.DataFrame

    """

    name: str = field(init=True)
    value: float | int | None = field(default=None, init=False)
    dictionary: dict | None = field(default=None, init=False)
    dataframe: pd.DataFrame | None = field(default=None, init=False)
