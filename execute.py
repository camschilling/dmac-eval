"""Execution Script to Produce Necessary Reports."""

import datetime as dt

from dmac_eval.headcount.analysis.no_hours import workers_no_hours
from dmac_eval.headcount.data_build import build_analytic_data
from dmac_eval.report.document import add_df_to_doc, report_preamble, save_doc

PATH_DICT = {dt.date(2025, 1, 1): "../../Data/dmac_eval_jan25_input.xlsx"}
OUT_PATH = "../../Documents/Reports/dmac_eval/tests/"
STAMP = dt.datetime.now().strftime("%y_%m_%d")  # noqa: DTZ005
REPORT_NAME = OUT_PATH + STAMP + "_report.docx"
DATA_NAME = OUT_PATH + STAMP + "_data.csv"
CURRENT_MO = dt.date(2025, 1, 1)

df = build_analytic_data(path_dict=PATH_DICT)

doc = report_preamble(
    report_month_start=dt.date(2025, 1, 1),
    report_month_end=CURRENT_MO,
)

# 0 Report

total_hc = df["employee_name"].nunique()


result_all_0 = workers_no_hours(df=df, months=[CURRENT_MO])
hc_all_0 = result_all_0.value
hc_all_0_pct = f"{(hc_all_0/total_hc)*100:.2f}"

doc.add_heading("Onboarded Contractors Billing 0 Hours", level=2)
txt = f"There are {total_hc} onboarded contractors. "
txt = txt + f"{hc_all_0}, or {hc_all_0_pct}% of these onboarded contractors billed 0.00 this month across all projects. "
txt = txt + "The table below displays this list."
doc.add_paragraph(txt)
doc = add_df_to_doc(
    doc=doc,
    df=result_all_0.dataframe,
    title="Onboarded Contractors Billing 0 Hours This Month",
)

save_doc(doc,file_name=REPORT_NAME)


df.to_csv(
    DATA_NAME,
    sep=",",  # Use comma as separator
    header=True,  # Include header row
    index=False,  # Do not include row indices
    encoding="utf-8",  # Use UTF-8 encoding
)
