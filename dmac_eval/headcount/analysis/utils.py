"""Utilities support analysis of the monthly billing."""
import datetime

import pandas as pd


def filter_time_period(
    df: pd.DataFrame, date_list: list[datetime.date],
) -> pd.DataFrame:
    """
    Filters the dataframe to those that are for the given month.

    :param df: analytic dataset.
    :type df: pd.DataFrame
    :param date_list: list of dates that will be used to filter "report_month" column.
        Raises a ValueError if not all dates and the day of the month is not `1`.
    :type date_list: list[datetime.date]
    :raises ValueError: Raises error if the date_list is not all date objects with
        the day field being `1`.
    :return: Dataset corresponding to appropriately filtered records.
    :rtype: pd.DataFrame
    """
    day_set = {d.day for d in date_list}
    if day_set != {1}:
        msg = "provide a date_list where each date is the first of the month."
        raise ValueError(msg)
    return df[df["report_month"].isin(date_list)]
