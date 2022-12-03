from jira import JIRA
from atlassian import Xray

from .config import config


__all__ = ["get_zwjira", "get_zwxray", "config"]

_zwjira = None
_zwxray = None


def get_zwjira():
    global _zwjira
    if _zwjira is None:
        _zwjira = JIRA(
            server=config.server, auth=(config.username, config.password)
        )
    return _zwjira


def get_zwxray():
    global _zwxray
    if _zwxray is None:
        _zwxray = Xray(
            url=config.server,
            username=config.username,
            password=config.password,
        )
    return _zwxray
