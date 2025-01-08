import argparse
import re
import requests

def extract_username_from_url(url):
    match = re.search(r'github\.com/([^/]+)', url)
    if match:
        return match.group(1)
    return None

def get_emails_from_repo(repo_url, token=None):
    match = re.search(r'github\.com/([^/]+)/([^/]+)', repo_url)
    if not match:
        print("Invalid GitHub repo URL.")
        return set()

    username, repo = match.groups()
    api_url = f"https://api.github.com/repos/{username}/{repo}/commits"
    headers = {"Authorization": f"token {token}"} if token else {}
    emails = set()

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        for commit in commits:
            commit_data = commit['commit']
            author_email = commit_data['author']['email']
            emails.add(author_email)
    elif response.status_code == 403:
        print("API rate limit exceeded")
    else:
        print(f"Error: {response.status_code}")
    return emails

def get_emails_from_user(username, token=None):
    if "github.com" in username:
        username = extract_username_from_url(username)
        if not username:
            print("Invalid GitHub URL.")
            return set()

    repos_url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(repos_url, headers=headers)
    if response.status_code != 200:
        if response.status_code == 403:
            print("API rate limit exceeded")
        else:
            print(f"Error: {response.status_code}")
        return set()

    repos = response.json()
    all_emails = set()

    for repo in repos:
        repo_name = repo['name']
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
        print(f"Searching in {username}/{repo_name}...")

        repo_response = requests.get(repo_url, headers=headers)
        if repo_response.status_code == 200:
            commits = repo_response.json()
            for commit in commits:
                commit_data = commit['commit']
                author_email = commit_data['author']['email']
                all_emails.add(author_email)
        elif repo_response.status_code == 403:
            print("API rate limit exceeded")
        else:
            print(f"Error: {repo_response.status_code}")

    return all_emails

def main():
    parser = argparse.ArgumentParser(
        description="GitHub Email Finder Script - Find email addresses in GitHub repositories.",
        epilog="Examples:\n"
               "  python script.py -repo https://github.com/torvalds/linux -token YOUR_TOKEN\n"
               "  python script.py -username torvalds --token YOUR_TOKEN\n"
               "  python script.py -username https://github.com/torvalds -token YOUR_TOKEN",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-repo",
        help="GitHub repository URL to search for emails. Example: https://github.com/torvalds/linux"
    )
    parser.add_argument(
        "-username",
        help="GitHub username or profile URL to search for emails in all their repositories. Example: username or https://github.com/torvalds"
    )
    parser.add_argument(
        "-token",
        help="GitHub API token to increase rate limit. Get one from: https://github.com/settings/tokens"
    )
    args = parser.parse_args()

    if args.repo:
        emails = get_emails_from_repo(args.repo, args.token)
        if emails:
            print("Found email addresses:")
            for email in emails:
                print(email)
    elif args.username:
        emails = get_emails_from_user(args.username, args.token)
        if emails:
            print("Found email addresses:")
            for email in emails:
                print(email)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()