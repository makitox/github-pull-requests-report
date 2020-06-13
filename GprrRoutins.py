import threading
from typing import Set

import htmlmin
from github import Github
from github.Repository import Repository
from mako.lookup import TemplateLookup
from mako.template import Template

from GprrModels import PrContainer, GprrUser, GprrPR, Filter, GprrRepository
from convertors import convert_pr, convert_repo


class GprrReport(object):
    default_section = ""

    def __init__(self, token: str, org: str, per_page: int = 300):
        assert token is not None
        assert org is not None

        self.github = Github(token, per_page=per_page)
        self.organization_str = org
        self.accounts_filter: Filter[GprrUser] = Filter("account filter")
        self.repo_filter: Filter[GprrRepository] = Filter("repository filter")
        self.full_list = PrContainer("Full list")
        self.by_author = PrContainer("By author")
        self.by_reviewer = PrContainer("By reviewer")
        self.by_repository = PrContainer("By repository")
        self.by_assignee = PrContainer("By assignee")


    def collect_data(self, repositories: Set[str] = {}, logins: Set[str] = {}):
        organization = self.github.get_organization(self.organization_str)
        if len(logins) == 0:  # no filter, add all logins
            for usr in organization.get_members():
                gprr_user = GprrUser(id=usr.id, login=usr.login, name=usr.name, url=usr.html_url)
                self.accounts_filter.add(gprr_user)
        else: # use logins from defined list
            for login in logins:
                usr = self.github.get_user(login)
                gprr_user = GprrUser(id=usr.id, login=login, name=usr.name, url=usr.html_url)
                self.accounts_filter.add(gprr_user)

        threads = list()
        if len(repositories) == 0:
            for repo in organization.get_repos(type='all'):
                # self.__process_repo(repo)
                x = threading.Thread(target=process_repo, args=(self, repo,))
                threads.append(x)
                x.start()
        else:
            for repo_str in repositories:
                repo = organization.get_repo(repo_str)
                # self.__process_repo(repo)
                x = threading.Thread(target=process_repo, args=(self, repo,))
                threads.append(x)
                x.start()
        for thread in threads:
            thread.join()

    def generate_html_report(
            self,
            filename: str,
            minimy_html: bool = False
    ):
        assert filename is not None
        look_up = TemplateLookup(directories=['.'])
        html_template = Template(filename='html_report_template.html', lookup=look_up)
        html_report = open(filename, "w")
        report_content = html_template.render(report_data=self)
        if minimy_html:
            report_content = htmlmin.minify(report_content)
        html_report.write(report_content)
        html_report.flush()
        html_report.close()


def process_repo(report: GprrReport, repo: Repository):
    gprr_repo = convert_repo(repo)
    report.repo_filter.add(gprr_repo)
    process_all_prs(report, repo)


def process_all_prs(report: GprrReport, repo: Repository):
    for pr in repo.get_pulls(state='open'):
        marked_pr = False
        gprr_pr: GprrPR = convert_pr(pr)

        if report.accounts_filter.contains_item_id(gprr_pr.creator.id):
            report.by_author.append_item(gprr_pr, gprr_pr.creator.name)
            marked_pr = True

        for review in gprr_pr.reviews:
            if report.accounts_filter.contains_item_id(review.user.id):
                report.by_reviewer.append_item(gprr_pr, review.user.name, True)
                marked_pr = True

        for assignee in gprr_pr.assignees:
            if report.accounts_filter.contains_item_id(assignee.id):
                report.by_assignee.append_item(gprr_pr, assignee.name)
                marked_pr = True

        if marked_pr:
            report.by_repository.append_item(gprr_pr, repo.name)
            report.full_list.append_item(gprr_pr, report.default_section)
