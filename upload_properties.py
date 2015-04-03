"""
Upload library.properties files to a collection of Arduino libraries on Github.

Should be pointed at the output of a generate_properties.py and it will read
each subfolder as an Arduino library and upload the library.properties inside
it to the master branch of the library's Github repository.

Note that if a library already has a library.properties file in its root on
Github then it will NOT be overwritten.  Only libraries without an existing
library.properties file will be processed.
"""
import argparse
import base64
import glob
import os
import sys

from github import Github
from github.GithubException import UnknownObjectException


def create_file(repo, path, message, content):
    """Create a file in a github repository using Github's content create API:
      https://developer.github.com/v3/repos/contents/#create-a-file
    Will create the file at the specified path under a given repo and use the
    provided commit message.  Content should be base64 encoded content for the
    file.  The master/default branch will be used to own the file.

    Note that this is just working around a deficiency in PyGithub as it hasn't
    yet implemented this API.
    """
    # Note that this implementation does some horrible stuff and assumes intimate
    # details of the PyGithub implementation.  This is ok as the function only
    # exists to quickly fill the gap until PyGithub implements a file create 
    # function.  Also very little error checking is done--caller beware!
    params = { 'message': message, 'content': content }
    headers, data = repo._requester.requestJsonAndCheck(
        "PUT",
        repo.url + "/contents" + path,
        input=params
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
    parser.add_argument('-r', '--root',
                        action='store',
                        default='.',
                        help='path to root of library folders from gen_properties.py output.  Defaults to the current directory.')
    parser.add_argument('github_root',
                        action='store',
                        help='Github user/organization name that owns the Arduino libraries')
    args = parser.parse_args()

    # Create github API instance and get account root.
    gh = Github(args.username, args.password)
    root = gh.get_user(args.github_root)

    # Change to the specified root directory.
    os.chdir(os.path.abspath(args.root))

    # Read reposities from directories with library.
    for repo_name in os.listdir('.'):
        # Skip this item if it's not a directory or it doesn't have a
        # library.properties file inside it.
        if not os.path.isdir(repo_name) or not os.path.exists(os.path.join(repo_name, 'library.properties')):
            print('Skipping {0} because it is not a directory with library.properties...'.format(repo_name))
            continue
        # Get associated repository from Github and check if a library.properties
        # file already exists.  Skip processing this repo if a file exists.
        repo = root.get_repo(repo_name)
        try:
            lib = repo.get_contents('library.properties')
            if lib is not None:
                # Found a library.properties file.  Skip processing this repo.
                print('Found existing library.properties for {0} on Github, skipping...'.format(repo_name))
                continue
        except UnknownObjectException:
            # Do nothing if library.properties file doesn't exist.  Continue on
            # and upload the file.
            pass
        print('Processing {0}...'.format(repo_name))
        # Read the contents of the library.properties file.
        content = None
        with open(os.path.join(repo_name, 'library.properties'), 'r') as infile:
            content = infile.read()
        if content is None:
            print('No library.properties data for {0}, skipping...'.format(repo_name))
            continue
        # Commit the file to the repository.
        create_file(repo, 
                    '/library.properties', 
                    'Automatic library.properties generation.',
                    base64.b64encode(content))
