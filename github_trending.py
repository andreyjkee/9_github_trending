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
    for item in response_body['items']:
        pretty_print_repository_info(item)

def get_open_issues_amount(repo_owner, repo_name):
    pass

def pretty_print_repository_info(repo):
    print('Repo name: {0}'.format(repo['full_name']))
    print('\tStars: {0}'.format(repo['stargazers_count']))
    print('\tLink: {0}'.format(repo['html_url']))
    print('\tIssues count: {0}'.format(repo['open_issues']))
    print('\tCreated at: {0}'.format(dateutil.parser.parse(repo['created_at']).strftime('%Y-%m-%d %H:%M')))


if __name__ == '__main__':
    get_trending_repositories()
