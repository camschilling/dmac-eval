import datetime

import pandas as pd
import pytest


@pytest.fixture
def multi_project_input():
    date1 = datetime.date(2024, 12, 1)
    # date2 = datetime.date(2025, 1, 1)
    cols = [
        "project",
        "labor_cat",
        "soc",
        "employee_name",
        "company",
        "exempt",
        "month_hours",
        "contract_hours",
        "report_month",
    ]
    project_col = ["TDL1"] * 2 + ["CA002"] * 5
    labor_cat_col = [
        "labor1",
        "labor2",
        "labor1",
        "labor1",
        "labor1",
        "labor1",
        "labor1",
    ]
    soc_col = ["blah"] * 7
    name_col = ["emp1", "emp2", "emp1", "emp3", "emp4", "emp5", "emp6"]
    company_col = ["B"] * 6 + ["C"]
    exempt_col = ["Y"] * 7
    month_hrs_col = [1.0, 0.0, 0.0, 2.0, 3.0, 4.0, 0.0]
    contract_hrs_col = [2.0, 3.0, 4.0, 5.0, 6.0, 6.0, 6.0]
    report_month_col = [date1] * 7

    return pd.DataFrame(
        list(
            zip(
                project_col,
                labor_cat_col,
                soc_col,
                name_col,
                company_col,
                exempt_col,
                month_hrs_col,
                contract_hrs_col,
                report_month_col,
                strict=False,
            ),
        ),
        columns=cols,
    )
