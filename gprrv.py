from datetime import datetime
from typing import Set

from github import Github, enable_console_debug_logging
from colorama import Fore, Style

from GprrRoutins import GprrReport
from globals import CONFIGURATION, DEFAULT_CONFIG_FILE, APPCONFIG_SECTION, TEAM_FILTER_SECTION, REPO_FILTER_SECTION, \
    ACCESS_TOKEN, ORGANIZATION, HTML_REPORT_FILE_NAME



if __name__ == "__main__":
    # for debug uncomment line below
    # enable_console_debug_logging()

# Check all configs
# Only one organization
# Create logins list
# Create repos list
# Start refactores GPRR routins
# Make someone more happy

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
        teamfilter: Set[str] = set()
        repofilter: Set[str] = set()

        organization = CONFIGURATION[APPCONFIG_SECTION][ORGANIZATION]
        assert organization is not None

        for teammember in CONFIGURATION[TEAM_FILTER_SECTION]:
            teamfilter.add(teammember)
        for repo in CONFIGURATION[REPO_FILTER_SECTION]:
            repofilter.add(repo)

        html_report_name = datetime.today().strftime(
            CONFIGURATION[APPCONFIG_SECTION][HTML_REPORT_FILE_NAME])
        # self.default_json_report_name = datetime.datetime.today().strftime(
        #     CONFIGURATION[APPCONFIG_SECTION][JSON_REPORT_FILE_NAME])
        report = GprrReport(token=accessToken, org=organization)
        print(f"{Fore.BLUE}Collectiong data: ", end='')
        report.collect_data(repofilter, teamfilter)
        print(f"{Fore.GREEN}Done{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Generating html report: ", end='')
        report.generate_html_report(filename=html_report_name, minimy_html=False)
        print(f"{Fore.GREEN}Done{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Missing {ACCESS_TOKEN}. Exit with error{Style.RESET_ALL}")
        exit(1)
