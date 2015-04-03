"""
Generate a list of Arduino library Github URLs that can be consumed by the
Arduino team to add to their master repository list.  Takes a list of Arduino
library Github names on standard input (like the output of the find_libraries.py
script).  Will output on standard output a list of library Github URLs and types
in a tab delimited format.  Create a bug on the Arduino github to have this list
of libraries added to the master Arduino library list.
"""
import argparse
import os
import sys

from github import Github


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
    parser.add_argument('-t', '--type',
                        action='store',
                        metavar='TYPE',
                        default='Contributed',
                        help='repository type to assign to each library.  Defaults to Contributed.')
    parser.add_argument('github_root',
                        action='store',
                        help='Github user/organization name that owns the Arduino libraries')
    args = parser.parse_args()

    # Create github API instance and get account root.
    gh = Github(args.username, args.password)
    root = gh.get_user(args.github_root)
    
    # Process all Arduino library names from standard input.
    for repo_name in sys.stdin:
        repo_name = repo_name.strip()
        # Skip blank lines.
        if repo_name == '':
            continue        
        # Get repository from github to find its description and other metadata.
        repo = root.get_repo(repo_name)
        # Print out git URL and repository type.
        url = repo.clone_url
        print('{0}\t{1}'.format(url, args.type))
