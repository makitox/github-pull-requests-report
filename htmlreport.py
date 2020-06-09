from mako.lookup import TemplateLookup
from mako.template import Template
from colorama import Fore, Style
import datetime

from globals import CONFIGURATION, HTML_REPORT_FILE_NAME, APPCONFIG_SECTION


def generate_report(organizations, teamfilter, repofilter):
    print(f"{Fore.BLUE}Collect data: {Style.RESET_ALL}", end='')

    organizations_repos = {}  # org name : list of repositories
    for org in organizations:
        organizations_repos[org.login] = get_org_repositories_list(org, repofilter)

    PullsFullList = get_filtered_pulls_list (organizations_repos, teamfilter)
    PullsByCreator = sort_pulls_by_creator(PullsFullList)
    PullsByRepo = sort_pulls_by_repo(PullsFullList)
    PullsByAssignee = sort_pulls_by_assignee(PullsFullList)
    PullsByReviewer = get_pulls_reviewers(PullsFullList)

    print(f"{Fore.GREEN}Done{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Report generation: {Style.RESET_ALL}", end='')
    create_rich_html_report(
        PullsFullList,
        PullsByCreator,
        PullsByRepo,
        PullsByAssignee,
        PullsByReviewer,
        teamfilter,
        repofilter
    )
    print(f"{Fore.GREEN}Done{Style.RESET_ALL}")


def sort_pulls_by_creator(pulls_full_list):
    sorted_pulls = {}
    for pull in pulls_full_list:
        if pull.user.name not in sorted_pulls:
            sorted_pulls[pull.user.name] = []
        pull_list = sorted_pulls[pull.user.name]
        pull_list.append(pull)
        sorted_pulls[pull.user.name] = pull_list
    return sorted_pulls


def sort_pulls_by_repo(pulls_full_list):
    sorted_pulls = {}
    for pull in pulls_full_list:
        if pull.head.repo.name not in sorted_pulls:
            sorted_pulls[pull.head.repo.name] = []
        pull_list = sorted_pulls[pull.head.repo.name]
        pull_list.append(pull)
        sorted_pulls[pull.head.repo.name] = pull_list
    return sorted_pulls


def sort_pulls_by_assignee(pulls_full_list):
    sorted_pulls = {}
    for pull in pulls_full_list:
        for assignee in pull.assignees:
            if assignee.name not in sorted_pulls:
                sorted_pulls[assignee.name] = []
            pull_list = sorted_pulls[assignee.name]
            pull_list.append(pull)
            sorted_pulls[assignee.name] = pull_list
    return sorted_pulls


def get_pulls_reviewers(pulls_full_list):
    sorted_pulls = {}

    for pull in pulls_full_list:
        # get all started reviews:
        for reviewer in pull.get_reviews():
            if reviewer.user.name not in sorted_pulls:
                sorted_pulls[reviewer.user.name] = []
            pull_list = sorted_pulls[reviewer.user.name]
            pull_list.append(pull)
            sorted_pulls[reviewer.user.name] = pull_list

        # get all pending reviews:
        for revs in pull.get_review_requests()[0]:
            if revs.name not in sorted_pulls:
                sorted_pulls[revs.name] = []
            pull_list = sorted_pulls[revs.name]
            pull_list.append(pull)
            sorted_pulls[revs.name] = pull_list

    return sorted_pulls


def get_filtered_pulls_list(organizations_repos, teamfilter):
    full_pull_list = []
    for orgName, repoList in organizations_repos.items():
        for repo in repoList:
            if len(teamfilter) == 0:
                # no filters. add all
                for pull in repo.get_pulls(state='open'):
                    full_pull_list.append(pull)
            else:
                # team filters in place. filter pulls by creator
                for pull in repo.get_pulls(state='open'):
                    if (pull.user.login in teamfilter) \
                            or is_user_reviewer(teamfilter, pull) \
                            or is_user_assignee(teamfilter, pull):
                        full_pull_list.append(pull)
    return full_pull_list


def is_user_reviewer(user_list, pull):
    return False
    # for rev in pull.get_reviews():
    #     if rev.user.login in user_list:
    #         return True
    # for rev in pull.get_review_requests()[0]:
    #     if rev.login in user_list:
    #         return True
    # return False


def is_user_assignee(user_list, pull):
    return False
    # for assignee in pull.assignees:
    #     if assignee.login in user_list:
    #         return True
    # return False

def get_org_repositories_list(organization, repo_filter):
    repositories = []
    repos = organization.get_repos()
    if len(repo_filter) == 0:
        # we don't need to filter repositories
        for repo in repos:
            repositories.append(repo)
    else:
        # we have repo filter, let's filter
        for repo in repos:
            if repo.name in repo_filter:
                repositories.append(repo)
    return repositories


def create_rich_html_report(
        pulls_full_list,
        pulls_by_creator,
        pulls_by_repo,
        pulls_by_assignee,
        pulls_by_reviewer,
        team_filter,
        repo_filter):
    look_up = TemplateLookup(directories=['.'])
    html_template = Template(filename='report_html_template.html', lookup=look_up)
    filename = datetime.datetime.today().strftime(CONFIGURATION[APPCONFIG_SECTION][HTML_REPORT_FILE_NAME])
    html_report = open(filename, "w")
    html_report.write(html_template.render(
        PullsFullList=pulls_full_list,
        PullsByCreator=pulls_by_creator,
        PullsByRepo=pulls_by_repo,
        PullsByAssignee=pulls_by_assignee,
        PullsByReviewer=pulls_by_reviewer,
        teamfilter=team_filter,
        repofilter=repo_filter,
        ignoredpulls=[]
    ))
    html_report.flush()
    html_report.close()
