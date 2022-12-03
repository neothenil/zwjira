from .globals import *


def fetch_fields(**data):
    _fields = get_zwjira().fields()
    field_map = {field["name"]: field["id"] for field in _fields}
    data["fields"] = field_map
    return data


def fetch_issue(issue_key=None, **data):
    if issue_key is None:
        return data
    issue = get_zwjira().issue(issue_key)
    data["issue"] = issue
    return data


def fetch_issue_test(issue=None, **data):
    if issue is None:
        return data
    data["issue"] = issue
    tests = []
    links = issue.fields.issuelinks
    for link in links:
        if link.type.name == "Tests":
            tests.append(link.inwardIssue.key)
    data["tests"] = tests
    return data


def create_test_executions(tests=None, fixversion=None, fields=None, **data):
    if tests is None or fixversion is None or fields is None:
        return data
    data["tests"] = tests
    data["fixversion"] = fixversion
    data["fields"] = fields
    issue_list = [
        {
            "project": {"id": get_zwjira().project("ZWCADTEST").id},
            "issuetype": {"name": "Test Execution"},
            "summary": "Ad-hoc execution for "
            + get_zwjira().issue(key).fields.summary,
            "fixVersions": [{"name": fixversion}],
            fields["Test VERNUM"]: config.vernums[fixversion],
            "assignee": {"name": config.username},
            fields["Tests association with a Test Execution"]: [key],
        }
        for key in tests
    ]
    test_executions = [
        response["issue"] for response in get_zwjira().create_issues(issue_list)
    ]
    data["test_executions"] = test_executions
    return data


def change_assignee(issue=None, assignee=None, **data):
    if issue is None or assignee is None:
        return data
    data["issue"] = issue
    data["assignee"] = assignee
    issue.update(assignee={"name": assignee})
    return data


def change_requirement_owner(
    issue=None, requirement_owner=None, fields=None, **data
):
    if issue is None or requirement_owner is None or fields is None:
        return data
    data["issue"] = issue
    data["requirement_owner"] = requirement_owner
    data["fields"] = fields
    issue.update(
        fields={fields["Requirement Owner"]: {"name": requirement_owner}}
    )
    return data


def fetch_transitions(issue=None, **data):
    if issue is None:
        return data
    data["issue"] = issue
    transitions = get_zwjira().transitions(issue)
    trans_name_to_id = {trans["name"]: trans["id"] for trans in transitions}
    data["transition_id"] = trans_name_to_id
    return data


def set_fix_version(issue=None, fixversion=None, transition_id=None, **data):
    if issue is None or fixversion is None or transition_id is None:
        return data
    data["issue"] = issue
    data["fixversion"] = fixversion
    data["transition_id"] = transition_id
    current_fixversions = [_fixver.name for _fixver in issue.fields.fixVersions]
    if fixversion in current_fixversions:
        return data
    current_fixversions.append(fixversion)
    get_zwjira().transition_issue(
        issue,
        transition_id["Set Fix Versions"],
        fields={
            "fixVersions": [
                {"name": _fixver} for _fixver in current_fixversions
            ]
        },
    )
    return data


def mark_as_fixed(issue=None, transition_id=None, **data):
    if issue is None or transition_id is None:
        return data
    data["issue"] = issue
    data["transition_id"] = transition_id
    get_zwjira().transition_issue(
        issue,
        transition_id["Mark as Fixed"],
        fields={"resolution": {"name": "Solved"}},
    )
    return data
