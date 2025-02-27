import datetime

import pandas as pd

from dmac_eval.report.document import add_df_to_doc, report_preamble, save_doc


def test_doc_build():
    df = pd.DataFrame(
        {"A": [1, 2, None, None], "B": [None, 1, None, None], "C": [3, 4, 5, None]},
    )
    path = "tests/report/test_files/test_file.docx"
    doc = report_preamble(
        report_month_start=datetime.date(2025, 1, 1),
        report_month_end=datetime.date(2025, 1, 1),
    )
    doc=add_df_to_doc(doc=doc, df=df, title="Mock Table")
    save_doc(doc=doc, file_name=path)
