from .globals import *


def mark_testexec_pass(tests=None, test_executions=None, **data):
    if tests is None or test_executions is None:
        return data
    data["tests"] = tests
    data["text_executions"] = test_executions
    execkeys = [_exec.key for _exec in test_executions]
    for key in tests:
        test_runs = get_zwxray().get_test_runs(key)
        for test_run in test_runs:
            if test_run["testExecKey"] in execkeys:
                test_run_id = test_run["id"]
                get_zwxray().update_test_run_status(test_run_id, "PASS")
    return data
