from .jira import *
from .xray import *


def command_mark_fixed(issue_key, fixversion):
    data = {"issue_key": issue_key, "fixversion": fixversion}
    data = fetch_fields(**data)
    data = fetch_issue(**data)
    data = fetch_issue_test(**data)
    data = create_test_executions(**data)
    data = mark_testexec_pass(**data)
    data["assignee"] = config.username
    data["requirement_owner"] = config.username
    data = change_assignee(**data)
    data = change_requirement_owner(**data)
    data = fetch_transitions(**data)
    data = set_fix_version(**data)
    data = mark_as_fixed(**data)
    return 0
