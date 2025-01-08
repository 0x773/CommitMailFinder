# Commit Mail Finder
Commit Mail Finder is a Python script that allows you to extract email addresses from GitHub repositories. It can search for emails in a specific repository or across all repositories of a given user. The script uses the GitHub API to fetch commit data and extract author email addresses.

Usage:
 -h, --help          show this help message and exit
  -repo REPO          GitHub repository URL to search for emails. Example: https://github.com/torvalds/linux
  -username USERNAME  GitHub username or profile URL to search for emails in all their repositories. Example: username or https://github.com/torvalds
  -token TOKEN        GitHub API token to increase rate limit. Get one from: https://github.com/settings/tokens

Examples:
  python script.py -repo https://github.com/torvalds/linux -token YOUR_TOKEN
  python script.py -username AppFlowy-IO --token YOUR_TOKEN
  python script.py -username https://github.com/torvalds -token YOUR_TOKEN
