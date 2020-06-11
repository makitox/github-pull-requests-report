from typing import List, Set
import datetime

from github import Github
from github.Label import Label
from github.NamedUser import NamedUser
from github.PullRequest import PullRequest
from github.Repository import Repository

from GprrModels import PrContainer, GprrUser, GprrPR, GprrPrFlag, GprrPrLabel, \
    GprrReview, Filter, GprrRepository
from globals import CONFIGURATION, APPCONFIG_SECTION, HTML_REPORT_FILE_NAME, JSON_REPORT_FILE_NAME


class GprrReport(object):

    def __init__(
            self,
            token: str = None,
            logins: Set[str] = None,
            repos: Set[str] = None,
            org:str = None,
            per_page: int = 300
    ):
        assert logins is not None
        assert repos is not None
        assert org is not None

        self.default_html_report_name = datetime.datetime.today().strftime(CONFIGURATION[APPCONFIG_SECTION][HTML_REPORT_FILE_NAME])
        self.default_json_report_name = datetime.datetime.today().strftime(CONFIGURATION[APPCONFIG_SECTION][JSON_REPORT_FILE_NAME])
        self.github = Github(token, per_page=per_page)
        self.organization_str = org

        self.accounts_filter: Filter[GprrUser] = Filter("account filter")
        self.repo_filter: Filter[GprrRepository] = Filter("repository filter")

        self.full_list = PrContainer("Full list")
        self.by_author = PrContainer("By author")
        self.by_reviewer = PrContainer("By reviewer")
        self.by_repository = PrContainer("By repository")
        self.by_assignee = PrContainer("By assignee")


    def collect_data(self, repositories: Set = {}, logins: Set = {}):
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

        if len(repositories) == 0:
            for repo in organization.get_repos(type='all'):
                self.__process_repo(repo)
        else:
            for repo_str in repositories:
                repo = self.github.get_repo(repo_str)
                self.__process_repo(repo)

    def __process_repo(self, repo: Repository):
        gprr_repo = self.__convert_repo(repo)
        self.repo_filter.add(gprr_repo)
        self.__process_all_prs(repo)

    def __process_all_prs(self, repo: Repository):
        for pr in repo.get_pulls(state='open'):
            marked_pr = False
            gprr_pr = self.__convert_pr(pr)

            if self.accounts_filter.contains_item_id(gprr_pr.creator.id):
                self.by_author.append_item(gprr_pr, gprr_pr.creator.name)
                marked_pr = True

            for review in gprr_pr.reviews:
                if self.accounts_filter.contains_item_id(review.user.id):
                    self.by_reviewer.append_item(gprr_pr, review.user.name)
                    marked_pr = True

            for assignee in gprr_pr.assignees:
                if self.accounts_filter.contains_item_id(assignee.id):
                    self.by_reviewer.append_item(gprr_pr, assignee.name)
                    marked_pr = True

            if marked_pr:
                self.by_repository.append_item(gprr_pr, repo.name)
                self.full_list.append_item(gprr_pr)

    def __convert_pr(
            self,
            pr: PullRequest,
    ) -> GprrPR:
        gprr_pr = GprrPR()
        gprr_pr.id = pr.id
        gprr_pr.number = pr.number
        gprr_pr.url = pr.html_url
        gprr_pr.repository = pr.head.repo.name
        gprr_pr.title = pr.title
        gprr_pr.creator = self.__convert_user(pr.user)
        gprr_pr.created = pr.created_at
        gprr_pr.updated = pr.updated_at
        gprr_pr.since_updated = datetime.datetime.today() - gprr_pr.updated

        for assignee in pr.assignees:
            gprr_pr.assignees.append(self.__convert_user(assignee))

        gprr_pr.flags.append(GprrPrFlag("Draft", str(pr.draft)))
        gprr_pr.flags.append(GprrPrFlag("Mergeable", str(pr.mergeable)))
        gprr_pr.flags.append(GprrPrFlag("Mergeable State", str(pr.mergeable_state)))

        for label in pr.get_labels():
            gprr_pr.labels.append(self.__convert_label(label))
        gprr_pr.initial_branch = pr.base.ref

        active_reviewers = []
        for review in pr.get_reviews():
            reviewer = self.__convert_user(review.user)
            if not self.__known_review(active_reviewers, reviewer):
                active_reviewers.append(reviewer)
                gprr_review = GprrReview(
                    user=reviewer,
                    state=review.state,
                    submitted_at=review.submitted_at,
                    url=review.html_url,
                )
                gprr_pr.reviews.append(gprr_review)
        for revusr in pr.get_review_requests()[0]:
            usr = self.__convert_user(revusr)
            review = GprrReview(user=usr, state="PENDING")
            gprr_pr.reviews.append(review)

    def __known_review(
            self,
            active_reviewers: List[GprrUser],
            user: GprrUser
    ) -> bool:
        for rvw in active_reviewers:
            if rvw.id == user.id:
                return True
        return False

    def __convert_label(
            self,
            label: Label
    ) -> GprrPrLabel:
        return GprrPrLabel(
            title=label.name,
            color=label.color,
            description=label.description
        )

    def __convert_user(
            self,
            user: NamedUser
    ) -> GprrUser:
        usr = GprrUser(
            login=user.login,
            name=user.name,
            id=user.id,
            url=user.html_url
        )
        return usr

    def __convert_repo(self, repo: Repository) -> GprrRepository:
        assert repo is not None
        return GprrRepository(
            id=repo.id,
            title=repo.description,
            url=repo.html_url,
            name=repo.name
        )


    # def generate_html_report(
    #         self,
    #         filename: str = __default_html_report_name
    # ):
    #     pass
    #
    # def generate_json_report(
    #         self,
    #         filename: str = __default_json_report_name
    # ):
    #     pass

