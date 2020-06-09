from typing import List, Set
import datetime

from github import Github

from GprrModels import PrContainer
from globals import CONFIGURATION, APPCONFIG_SECTION, HTML_REPORT_FILE_NAME, JSON_REPORT_FILE_NAME


class GprrReport(object):

    __default_html_report_name: str = datetime.datetime.today().strftime(CONFIGURATION[APPCONFIG_SECTION][HTML_REPORT_FILE_NAME])
    __default_json_report_name: str = datetime.datetime.today().strftime(CONFIGURATION[APPCONFIG_SECTION][JSON_REPORT_FILE_NAME])
    __github: Github = None

    fullList: PrContainer = None
    byRepos: PrContainer = None
    byAuthor: PrContainer = None
    byAssignee: PrContainer = None
    byReviewer: PrContainer = None

    def __init__(
            self,
            token: str = None
    ):
        self.__github = Github(token, )

    def collect_data(
            self,
            companies: Set = {},
            repositories: Set = {},
            logins: Set = {}
    ):
        pass

    def generate_html_report(
            self,
            filename: str = __default_html_report_name
    ):
        pass

    def generate_json_report(
            self,
            filename: str = __default_json_report_name
    ):
        pass
