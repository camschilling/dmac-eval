import datetime

import pandas as pd
import pytest

from dmac_eval.headcount.analysis.utils import filter_time_period


def test_filter_time_period():
    date1 = datetime.date(2024, 12, 1)
    date2 = datetime.date(2025, 1, 1)
    cols = ["project", "report_month"]
    project_col = ["TDL1"] * 5 + ["CA002"] * 5
    report_month_col = [date1] * 7 + [date2] * 3

    df = pd.DataFrame(
        list(
            zip(
                project_col,
                report_month_col,
                strict=False,
            ),
        ),
        columns=cols,
    )
    filtered_d1 = filter_time_period(df=df, date_list=[date1])
    assert len(filtered_d1) == 7

    filtered_d2 = filter_time_period(df=df, date_list=[date1, date2])
    assert len(filtered_d2) == 10

    m = "provide a date_list"
    with pytest.raises(ValueError, match=m):
        filter_time_period(df=df, date_list=[])
