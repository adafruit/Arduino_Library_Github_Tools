"""
Scan a Github account for any Arduino libraries and print out a list of them.
The heuristic for identifying an Arduino library is to look for a Github
repository that has an 'examples' folder in its root and subfolders beneath
it that contain either .ino or .pde files.  Note that this is not a foolproof
heuristic and Processing libraries might be found too!
"""
import argparse
import os
import sys

from github import Github
from github.GithubException import UnknownObjectException


def is_arduino_library(repository):
    """Return True if repository looks like an Arduino library.  Uses a simple
    heuristic of checking for an 'examples' folder with .ino / .pde files inside
    it at depth 2.
    """
    # Check for an examples folder.
    try:
        examples = repository.get_dir_contents('/examples')
    except UnknownObjectException:
        # Examples subfolder doesn't exist, must not be an Arduino library.
        return False
    # Check each directory of the examples folder.
    for subdir in filter(lambda x: x.type == 'dir', examples):
        # Find list of files that end in .ino or .pde.
        files = repository.get_dir_contents('/examples/{0}'.format(subdir.name))
        ino_pde = filter(lambda x: x.name.lower().endswith('.ino') or \
                                   x.name.lower().endswith('.pde'),
                         files)
        if len(ino_pde) > 0:
            # Found some ino/pde files so this must be an Arduino library.
            return True
    # Couldn't find any subdir with ino/pde files, must not be an Arduino library.
    return False

def has_library_properties(repository):
    """Return True if the repository has a library.properties file."""
    try:
        lib = repository.get_contents('library.properties')
    except UnknownObjectException:
        # No library.properties file.
        return False
    # Found the file!
    return True


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
                        choices=['all', 'owner', 'public', 'private', 'member'],
                        default='all',
                        help='scan for specific type of repositories.  For example --type public will only scan public repositories.  Default is all.')
    parser.add_argument('-n', '--new',
                        action='store_true',
                        help='only list Arduino libraries which have no library.properties file (i.e. might be new)')
    parser.add_argument('github_root',
                        action='store',
                        help='Github user/organization name to scan for Arduino libraries')
    args = parser.parse_args()

    # Create github API instance.
    gh = Github(args.username, args.password)

    # Search all the Github repositories in the provided root and print out the
    # name of any that look like Arduino libraries.
    for repo in gh.get_user(args.github_root).get_repos(type=args.type):
        if is_arduino_library(repo):
            if not args.new or (args.new and not has_library_properties(repo)):
                print(repo.name)
