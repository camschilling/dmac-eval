"""Execution Script to Produce Necessary Reports."""

import datetime

from dmac_eval.headcount.data_build import build_analytic_data

PATH_DICT = {datetime.date(2025, 1, 1): "../../Data/dmac_eval_jan25_input.xlsx"}
df = build_analytic_data(path_dict=PATH_DICT)

print(len(df))
