from github import Github
from colorama import Fore, Style
from globals import CONFIGURATION, DEFAULT_CONFIG_FILE, APPCONFIG_SECTION, TEAM_FILTER_SECTION, REPO_FILTER_SECTION, \
    ACCESS_TOKEN, ORGANIZATION
from htmlreport import generate_report



if __name__ == "__main__":
    # for debug uncomment line below
    # enable_console_debug_logging()

    print(f"{Fore.BLUE}Read configuration: {Style.RESET_ALL}", end='')
    import sys

    if len(sys.argv) > 1:
        configFile = sys.argv[1]
        CONFIGURATION.read(configFile)
        print(f"{Fore.WHITE} config file: {configFile}  {Style.RESET_ALL}", end='')
    else:
        CONFIGURATION.read(DEFAULT_CONFIG_FILE)
        print(f"{Fore.WHITE} config file: {DEFAULT_CONFIG_FILE}  {Style.RESET_ALL}", end='')
    print(f"{Fore.GREEN}Done{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Check configuration sections: {Style.RESET_ALL}")
    if APPCONFIG_SECTION in CONFIGURATION:
        print(f"{Fore.BLUE}\tGithub configuration: {Fore.GREEN}Done{Style.RESET_ALL}")
    else:
        print(f"{Fore.BLUE}\tGithub configuration: {Fore.RED}Empty. Exit with error{Style.RESET_ALL}")
        exit(1)
    if TEAM_FILTER_SECTION in CONFIGURATION:
        print(f"{Fore.BLUE}\tTeam filter configuration: {Fore.GREEN}Done{Style.RESET_ALL}")
    else:
        print(
            f"{Fore.BLUE}\tTeam filter configuration: {Fore.RED}Empty. All available users will be used{Style.RESET_ALL}")
    if REPO_FILTER_SECTION in CONFIGURATION:
        print(f"{Fore.BLUE}\tRepo filter configuration: {Fore.GREEN}Done{Style.RESET_ALL}")
    else:
        print(f"{Fore.BLUE}\tRepo filter configuration: {Fore.RED}Empty. All available repos will be used{Style.RESET_ALL}")

    accessToken = CONFIGURATION[APPCONFIG_SECTION][ACCESS_TOKEN]
    if accessToken is not None:
        github = Github(accessToken)
        print(f"{Fore.BLUE}Access user: {Fore.GREEN}{github.get_user().name}{Style.RESET_ALL}")
        organizations = []
        teamfilter = set()
        repofilter = set()
        if CONFIGURATION[APPCONFIG_SECTION][ORGANIZATION] is not None:  # organization provided. create report only for this org
            filteredOrg = CONFIGURATION[APPCONFIG_SECTION][ORGANIZATION]
            org = github.get_organization(filteredOrg)
            organizations.append(org)
            print(f"{Fore.BLUE}Organization filter: {Fore.GREEN}{org.login}{Style.RESET_ALL}")

        else:  # organization is not provided. create report for all user's organizations
            for org in github.get_user().get_orgs():
                organizations.append(org)
                org.get_repos()
                print(f"{Fore.BLUE}Organization: {Fore.GREEN}{org.name}{Style.RESET_ALL}")

        for teammember in CONFIGURATION[TEAM_FILTER_SECTION]:
            teamfilter.add(teammember)
        for repo in CONFIGURATION[REPO_FILTER_SECTION]:
            repofilter.add(repo)

        # here we have all needed organizations. lets create report for them
        generate_report(organizations, teamfilter, repofilter)
    else:
        print(f"{Fore.RED}Missing {ACCESS_TOKEN}. Exit with error{Style.RESET_ALL}")
        exit(1)
