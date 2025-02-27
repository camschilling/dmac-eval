from dmac_eval.headcount.analysis.no_hours import workers_no_hours


def test_workers_no_hours(multi_project_input):
    w =workers_no_hours(df=multi_project_input)
    print(w)
