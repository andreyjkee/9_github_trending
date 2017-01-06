import argparse

import requests
import datetime
import dateutil.parser


API_BASE = 'https://api.github.com/'

def get_trending_repositories(top_size=20):
    week_ago_iso8601 = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(microsecond=0).isoformat()
    response = requests.get(API_BASE+'search/repositories', {
        'q': 'created:>{0}'.format(week_ago_iso8601),
        'sort': 'stars',
        'order': 'desc',
        'page': 1,
        'per_page': top_size
    })
    response_body = response.json()
    return response_body

def get_open_issues_amount(repo_owner, repo_name):
    response = requests.get(API_BASE+'repos/{0}/{1}/issues'.format(repo_owner, repo_name), {
        'state': 'open'
    })
    return response.json()

def pretty_print_repository_info(repo):
    print('Repo name: {0}'.format(repo['name']))
    print('\tOwner: {0}'.format(repo['owner']['login']))
    print('\tStars: {0}'.format(repo['stargazers_count']))
    print('\tLink: {0}'.format(repo['html_url']))
    print('\tIssues count: {0}'.format(repo['open_issues']))
    print('\tCreated at: {0}'.format(dateutil.parser.parse(repo['created_at']).strftime('%Y-%m-%d %H:%M')))


def pretty_print_issues(issues):
    if type(issues) != list:
        return
    for issue in issues:
        print('\t\tIssue title: {0}'.format(issue['title']))
        print('\t\tIssue url: {0}'.format(issue['url']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get duplicated files")
    parser.add_argument("-c", "--count", type=int, dest="count", default=20)
    options = parser.parse_args()
    repositories = get_trending_repositories(top_size=options.count)
    if repositories:
        for repo in repositories['items']:
            pretty_print_repository_info(repo)
            issues = get_open_issues_amount(repo['owner']['login'], repo['name'])
            pretty_print_issues(issues)
