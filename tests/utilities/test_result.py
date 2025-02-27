from dmac_eval.utilities.result import Result


def test_result():
    r = Result(name="test_name")
    print(r)
    r.value = 1
    print(r)
