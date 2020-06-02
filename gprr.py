from github import Github
from colorama import Fore, Style
from htmlreport import generate_report
import configparser

APPCONFIG_SECTION = "appconfig"
ACCESS_TOKEN = "access_token"
ORGANIZATION = "organization"
REPO_FILTER_SECTION = "repositories filter"
TEAM_FILTER_SECTION = "team filter"
DEFAULT_CONFIG_FILE = "configuration.ini"

if __name__ == "__main__":
    # for debug uncomment line below
    # enable_console_debug_logging()

    print(f"{Fore.BLUE}Read configuration: {Style.RESET_ALL}", end='')
    config = configparser.ConfigParser()
    import sys

    if len(sys.argv) > 1:
        configFile = sys.argv[1]
        config.read(configFile)
        print(f"{Fore.WHITE} config file: {configFile}  {Style.RESET_ALL}", end='')
    else:
        config.read(DEFAULT_CONFIG_FILE)
        print(f"{Fore.WHITE} config file: {DEFAULT_CONFIG_FILE}  {Style.RESET_ALL}", end='')
    print(f"{Fore.GREEN}Done{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Check configuration sections: {Style.RESET_ALL}")
    if APPCONFIG_SECTION in config:
        print(f"{Fore.BLUE}\tGithub configuration: {Fore.GREEN}Done{Style.RESET_ALL}")
    else:
        print(f"{Fore.BLUE}\tGithub configuration: {Fore.RED}Empty. Exit with error{Style.RESET_ALL}")
        exit(1)
    if TEAM_FILTER_SECTION in config:
        print(f"{Fore.BLUE}\tTeam filter configuration: {Fore.GREEN}Done{Style.RESET_ALL}")
    else:
        print(
            f"{Fore.BLUE}\tTeam filter configuration: {Fore.RED}Empty. All available users will be used{Style.RESET_ALL}")
    if REPO_FILTER_SECTION in config:
        print(f"{Fore.BLUE}\tRepo filter configuration: {Fore.GREEN}Done{Style.RESET_ALL}")
    else:
        print(
            f"{Fore.BLUE}\tRepo filter configuration: {Fore.RED}Empty. All available repos will be used{Style.RESET_ALL}")

    accessToken = config[APPCONFIG_SECTION][ACCESS_TOKEN]
    if accessToken is not None:
        github = Github(accessToken)
        print(f"{Fore.BLUE}Access user: {Fore.GREEN}{github.get_user().name}{Style.RESET_ALL}")
        organizations = []
        teamfilter = set()
        repofilter = set()
        if config[APPCONFIG_SECTION][ORGANIZATION] is not None:  # organization provided. create report only for this org
            filteredOrg = config[APPCONFIG_SECTION][ORGANIZATION]
            org = github.get_organization(filteredOrg)
            organizations.append(org)
            print(f"{Fore.BLUE}Organization filter: {Fore.GREEN}{org.login}{Style.RESET_ALL}")

        else:  # organization is not provided. create report for all user's organizations
            for org in github.get_user().get_orgs():
                organizations.append(org)
                org.get_repos()
                print(f"{Fore.BLUE}Organization: {Fore.GREEN}{org.name}{Style.RESET_ALL}")

        for teammember in config[TEAM_FILTER_SECTION]:
            teamfilter.add(teammember)
        for repo in config[REPO_FILTER_SECTION]:
            repofilter.add(repo)

        # here we have all needed organizations. lets create report for them
        generate_report(organizations, teamfilter, repofilter)
    else:
        print(f"{Fore.RED}Missing {ACCESS_TOKEN}. Exit with error{Style.RESET_ALL}")
        exit(1)
