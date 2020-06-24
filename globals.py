import configparser

APPCONFIG_SECTION = "appconfig"
HTML_REPORT_FILE_NAME = "html_report_file_name"
JSON_REPORT_FILE_NAME = "json_report_file_name"
ACCESS_TOKEN = "access_token"
ORGANIZATION = "organization"
MINIFY_REPORT = "minify_report"
STRICT_TO_TEAM = "strict_to_team_filter"

# filter sections
REPO_FILTER_SECTION = "repositories filter"
TEAM_FILTER_SECTION = "team filter"
DEFAULT_CONFIG_FILE = "configuration.ini"

CONFIGURATION = configparser.ConfigParser()