from datetime import date

import pandas as pd
import pytest

from dmac_eval.headcount.data_build import (
    add_static_date_column,
    prepare_month_df,
    read_single_month_excel,
    remove_dupes_in_col_names,
    stack_data,
)


def test_remove_dupes_in_col_names():
    l1 = [1, 2]
    l2 = [5, 6]
    l3 = [3, 4]
    df = pd.DataFrame(
        {"colA": [1, 2], "colB": [None, 1], "colA": [3, 4]},  # noqa: F601
    )
    df = pd.DataFrame(
        list(zip(l1, l2, l3, strict=True)),
        columns=["colA", "colB", "colA"],
    )
    new_df = remove_dupes_in_col_names(df=df)
    assert (list(new_df.columns)) == ["colA", "colB", "colA.1"]


def test_read_single_month_excel():
    # Example usage:
    file_path = "../../Data/dmac_eval_jan25_input.xlsx"
    df_dict = read_single_month_excel(file_path=file_path)
    # pd.set_option("display.max_rows", None)
    # Accessing individual DataFrames by their sheet names
    for sheet_name, df in df_dict.items():
        print(f"Sheet Name: {sheet_name}")
        print(len(df))  # Count rows
        print(df.head())  # Display first few rows of each DataFrame
        print(df.tail())  # Display last few rows.


@pytest.fixture
def sample_data():
    """Fixture providing sample data for testing."""
    df1 = pd.DataFrame(
        {"A": [1, 2, None, None], "B": [None, 1, None, None], "C": [3, 4, 5, None]},
    )

    df2 = pd.DataFrame({"A": [1, None], "B": [1, None], "C": [1, None]})

    df3 = pd.DataFrame()

    return {"sheet1": df1, "sheet2": df2, "sheet3": df3}


def test_stack(sample_data):
    result_df = stack_data(sample_data)

    # Expecting an empty dataframe as output
    expected_result = pd.DataFrame(
        {"A": [1, 2, None, 1], "B": [None, 1, None, 1], "C": [3, 4, 5, 1]},
    )

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        expected_result,
        check_dtype=False,
    )


def test_add_static_date_column():
    df_in = pd.DataFrame({"A": [1, 2, 3]})
    df_expected = pd.DataFrame({"A": [1, 2, 3], "new_date": [date(2023, 10, 6)] * 3})

    # Add a new column with a static date
    df_out = add_static_date_column(df_in, "new_date", date(2023, 10, 6))
    pd.testing.assert_frame_equal(df_expected, df_out)


def test_data_build():
    df = prepare_month_df(
        month=date(2025, 1, 1),
        path_to_excel="../../Data/dmac_eval_jan25_input.xlsx",
    )
    print(df.head())
