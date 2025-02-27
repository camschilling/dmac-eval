"""
Module to generate report on contractors billing now hours.

Percentage/count of headcount that is billing no hours across all projects.
Percentage/count of headcount that is billing no hours on one or more projects.
Percentage/count of headcount that is billing no hours on one,
    but billing hours on another.
"""

import datetime

import pandas as pd

from dmac_eval.utilities.result import Result

from .utils import filter_time_period


def workers_no_hours(df: pd.DataFrame, months: list[datetime.date] = []) -> Result:  # noqa: B006
    """
    Counts the contractors that are billing no hours.

    :param df: Analytic dataset
    :type df: pd.DataFrame
    :param months: list of months (day shall be 1) that should be summed, defaults to []
    :type months: list[datetime.date], optional
    :return: Result object that holds the count of contractors billing no monthly hours
        alongside a dataframe that is a helpful summary df to accompany.
    :rtype: Result
    """
    # count of workers without hours across all projects
    # include proportion
    # list them, identify which projects they are on
    if len(months) > 0:
        df = filter_time_period(df=df, date_list=months)

    # Group by employee and calculate the sum of hours for this month
    df_grouped = df.groupby("employee_name")["month_hours"].sum()

    # Identify groups where the sum is 0
    zero_billed = df_grouped[df_grouped == 0].index

    # Filter original DataFrame based on zero_sum_groups
    zero_group = df[df["employee_name"].isin(zero_billed)]

    result_df = zero_group.groupby(["employee_name", "company"]).agg(
        projects=("project", lambda x: " , ".join(x)),
        total_month_hours=("month_hours", "sum"),
        total_contract_hours=("contract_hours", "sum"),
    ).reset_index()

    r = Result(name="contractors_no_hours")
    r.value = len(result_df)
    r.dataframe = result_df
    return r


# proportion of headcount with

# count of projects with workers contributing no hours
