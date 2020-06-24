# GitHub pull requests report (GPRR)

This script creates PR report, that can help with understanding situation with PRs in a high level - how many PRs are in open state, how many PRs are assigned to particular developer, etc.

It is quite usefull report for scrum masters, team leads and team members, who want to see high level picture. 

Why HTML report: all is simple. HTML report is interactive, it is easier to show multilayer information. Plus, usually online scrum's stand ups are performed with screen sharing - usually it is browser with Jira, VersionOne or other tools. I believe it is logical to create report as html page that can be opened in new tab  

## How to install
Download and install [python](https://www.python.org/downloads/) (if not installed yet). You will need Python version 3.x.  
Download [GPRR latest release](https://github.com/makitox/github-pull-requests-report/releases) (stable) or download code from [master](https://github.com/makitox/github-pull-requests-report/archive/master.zip) (newest features)
Install dependencies:

    pip install -r requirements.txt

that's it. GPRR ready to use.

## How to configure and use
First of all, you need to update configuration file. configuration.ini is the configuration, but you can copy configuration to any file and pass it as parameter:

    python3 gprr.py myconfig.ini

In the example above myconfig.ini it the custom config file. Please read the comments in configuration.ini file, they should describe pretty clear what you need to insert.


## Known issues and limitations:
* Work time - it is usually takes a few minutes to create report. 
* GitHub API calls request limit - there is Github's limit 5000 quests per hour. GPRR sends a lot of requests to collect all needed data, so it easily can exceeds limit. Please use more strict filters in configuration file (you may use several configuration files)
  