"""Module to build the analytic dataset."""

import datetime

import pandas as pd


def remove_dupes_in_col_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes column name duplicates in df.

    If a column name is duplicated, adds a decimal and integer.

    e.g. column list of ["colA", "colA", "colA"] becomes
    ["colA", "colA.1", "colA.2"]

    :param df: _description_
    :type df: pd.DataFrame
    :return: _description_
    :rtype: pd. DataFrame
    """
    cols = pd.Series(df.columns)

    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [  # noqa: PD011
            dup + "." + str(i) if i != 0 else dup for i in range(sum(cols == dup))
        ]

    # rename the columns with the cols list.
    df.columns = cols

    return df


def read_single_month_excel(
    file_path: str,
    row_skip: int = 5,
    row_end: int = 211,
) -> dict[str, pd.DataFrame]:
    """
    Reads an Excel file and stores each tab as a pandas DataFrame.

    :param file_path: The path to the Excel file.
    :type file_path: str
    :param row_skip: The number of rows to skip on each tab.
        Pandas will begin reading on the row `row_skip + 1`.
        Ddefaults to 5 as per the structure of the monthly reports.
        e.g. if 5 is provided, the data will be read starting on row 6.
    :type row_skip: int
    :param row_end: The last row of the table that should be read in.
        Defaults to 211 as per the monthly reports.
        (a "Grand Total" row starts on row 212)

    :return: A dictionary where keys are sheet names and values are DataFrames.

    """
    # Read all sheets into a dictionary of DataFrames
    nrows = row_end - row_skip - 1
    return pd.read_excel(file_path, sheet_name=None, header=row_skip, nrows=nrows)


def stack_data(df_dict: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Cleans and unions dataframes.

    Removes rows where all fields are null from each DataFrame in the input dictionary,
    and unions the DataFrames together.

    :param df_dict: A dictionary where keys are identifiers and values are DataFrames.
    :type df_dict: dict

    :return: A single pandas DataFrame containing the union of all input DataFrames.
    :rtype: pd.DataFrame

    """
    cleaned_dfs = []

    for df in df_dict.values():
        # skip if not a df
        if not isinstance(df, pd.DataFrame):
            continue
        # skip if empty df
        if len(df) == 0:
            continue
        # Remove rows where all fields are null
        cleaned_df = df.dropna(how="all")
        cleaned_dfs.append(cleaned_df)

    # Concatenate all cleaned DataFrames into one
    return pd.concat(cleaned_dfs, ignore_index=True)


def add_static_date_column(
    df: pd.DataFrame,
    column_name: str,
    static_date: datetime.date | str,
) -> pd.DataFrame:
    """
    Adds a new column to the DataFrame with a static provided date.

    :param df: The input pandas DataFrame.
    :type df: pd.DataFrame
    :param column_name: The name of the new column to be added.
    :type column_name: str
    :param static_date: The static date to be added in the new column.
    :type static_date: datetime.date or str (in 'YYYY-MM-DD' format)

    :return: A new DataFrame with the added static date column.
    :rtype: pd.DataFrame
    """
    # If the provided date is a string, convert it to a datetime.date object
    if isinstance(static_date, str):
        static_date = pd.to_datetime(static_date).date()

    # Add the new column with the static date
    df[column_name] = static_date

    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames the columns of the report to a better set of column names.

    Assumes that columns are static across the tabs.

    :param df: input dataframe with column names sourced from the excel.
    :type df: pd.DataFrame
    :return: Dataframe with refined column names.
    :rtype: pd.DataFrame
    """
    # TDL/CA,LABOR CATEGORY,SOC,EMPLOYEE NAME,COMPANY,EXEMPT (Y/N/NA),HOURS.1,HOURS.2
    new_cols = [
        "project",
        "labor_cat",
        "soc",
        "employee_name",
        "company",
        "exempt",
        "month_hours",
        "contract_hours",
    ]
    df.columns = new_cols
    return df


def prepare_month_df(month: datetime.date, path_to_excel: str) -> pd.DataFrame:
    """
    Calls appropriate functions to clean and union a single month of data.

    :param month: Date object that is the first of the month of the month
        of the corresponding report.
    :type month: datetime.date
    :param path_to_excel: Path to the month's excel report.
    :type path_to_excel: str
    :return: Stacked data with a "report_month" column added.
    :rtype: pd.DataFrame

    """
    df_dict = read_single_month_excel(file_path=path_to_excel)
    df = stack_data(df_dict=df_dict)
    df = rename_columns(df=df)
    return add_static_date_column(
        df=df,
        column_name="report_month",
        static_date=month,
    )


def build_analytic_data(path_dict: dict[datetime.date, str]) -> pd.DataFrame:
    """
    Builds a full analytic dataset from multiple monthly reports.

    :param path_dict: Dictionary where keys are the date associated with a report
        and the values are paths to the excel report.
    :type path_dict: dict[datetime.date, str]
    :return: Dataframe with each report stacked, with identifier column "report_month"
        to differentiate between months.
    :rtype: pd.DataFrame
    """
    df_list = []
    for d, path in path_dict.items():
        mo1 = d.replace(day=1)  # set to first of a given month
        df = prepare_month_df(month=mo1, path_to_excel=path)
        df_list.append(df)
    return pd.concat(df_list, ignore_index=True)
