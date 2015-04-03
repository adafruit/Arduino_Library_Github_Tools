"""
Process a list of Arduino libraries and ensure a tagged release exists on Github
for each one.  The input list of libraries should be provided on standard input
(such as from the output of the find_libraries.py script).  Each library will
be processed and checked to see if at least one tagged release exists and create
a default 1.0.0 release for libraries that have none.

Note that only libraries which have a library.properties file in their master
branch root will be processed!
"""
import argparse
import os
import sys

from github import Github
from github.GithubException import UnknownObjectException


def create_release(repo, tag_name, name, body):
    """Create a release for the current master branch of a repository using the
    Github API:
      https://developer.github.com/v3/repos/releases/#create-a-release

    Note that this is just working around a deficiency in PyGithub as it hasn't
    yet implemented this API.
    """
    # Note that this implementation does some horrible stuff and assumes intimate
    # details of the PyGithub implementation.  This is ok as the function only
    # exists to quickly fill the gap until PyGithub implements a release create
    # function.
    params = { 'tag_name': tag_name, 'name': name, 'body': body }
    headers, data = repo._requester.requestJsonAndCheck(
        "POST",
        repo.url + "/releases",
        input=params
    )
    return headers, data

def get_latest_release(repo):
    """Get the latest release for a repo, or throw an error if no releases exist.
    Uses the following GitHub API:
      https://developer.github.com/v3/repos/releases/#get-the-latest-release
    """
    # Again this implementation assumes inner workings of PyGithub because the
    # API isn't implemented yet in PyGithub.
    headers, data = repo._requester.requestJsonAndCheck(
        "GET",
        repo.url + "/releases/latest"
    )
    return headers, data


if __name__ == '__main__':
    # Build command line argument parser and parse arguments.
    # Use docstring of the file as the description of the tool.
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('-u', '--username',
                        action='store',
                        metavar='USERNAME',
                        default=os.environ.get('GITHUB_USERNAME', None),
                        help='Github username for accessing Github API.  If not specified the GITHUB_USERNAME environment variable value will be used.')
    parser.add_argument('-p', '--password',
                        action='store',
                        metavar='PASSWORD',
                        default=os.environ.get('GITHUB_PASSWORD', None),
                        help='Github password for accessing Github API.  If not specified the GITHUB_PASSWORD environment variable value will be used.')
    parser.add_argument('-v', '--version',
                        action='store',
                        metavar='VERSION',
                        default='1.0.0',
                        help='release version to create for each library.  Defaults to 1.0.0 if not specified.')
    parser.add_argument('github_root',
                        action='store',
                        help='Github user/organization name that owns the Arduino libraries')
    args = parser.parse_args()

    # Create github API instance and get account root.
    gh = Github(args.username, args.password)
    root = gh.get_user(args.github_root)

    # Read reposities from standard input and process each one.
    for repo_name in sys.stdin:
        repo_name = repo_name.strip()
        # Skip blank lines.
        if repo_name == '':
            continue
        # Get associated repository from Github and check if a library.properties
        # file already exists.  Skip processing this repo if a library.properties
        # file does not exist.
        repo = root.get_repo(repo_name)
        try:
            lib = repo.get_contents('library.properties')
        except UnknownObjectException:
            # Skip this repository if it has no library.properties file as this
            # file is required to be picked up by Arduino's library tooling.
            print('No library.properties file found for {0}, skipping...'.format(repo_name))
            continue
        # Check for an existing release tag and skip the repo if found.
        try:
            get_latest_release(repo)
            # Found a release, skip processing this repository.
            print('Found a release for {0}, skipping...'.format(repo_name))
            continue
        except UnknownObjectException:
            # No current release, continue processing.
            pass
        print('Processing {0}...'.format(repo_name))
        create_release(repo, 
                       args.version,  # Release tag value.
                       '{0} release for Arduino'.format(args.version),  # Release name.
                       'Automated initial release for Arduino library system.')  # Release description.
