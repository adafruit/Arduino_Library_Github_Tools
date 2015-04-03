"""
Generate library.properties files for Arduino libraries using metadata from
each library Github repository.  Takes the list of directories from standard
input (ideally piped in from the output of the find_libraries.py script) and
creates a subfolder with library.properties file for each library.

Uses the library's Github description to populate the library sentence and
paragraph descriptions and tries to pick good default values for version,
author, and maintainer if not specified.

After generating the library.properties files be sure to inspect them and set
the category and architecture by hand.
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
    parser.add_argument('-a', '--author',
                        action='store',
                        metavar='NAME',
                        help='author to assign to each library.  Defaults to the name of the Github user/organization if not specified.')
    parser.add_argument('-m', '--maintainer',
                        action='store',
                        metavar='NAME',
                        help='maintainer to assign to each library.  Defaults to the name of the Github user/organization if not specified.')
    parser.add_argument('-v', '--version',
                        action='store',
                        metavar='VERSION',
                        default='1.0.0',
                        help='version to assign to each library.  Defaults to 1.0.0 if not specified.')
    parser.add_argument('-o', '--output',
                        action='store',
                        metavar='PATH',
                        help='path to use as the root for output files.  Defaults to the current directory if not specified.')
    parser.add_argument('github_root',
                        action='store',
                        help='Github user/organization name to reference for looking up libraries')
    args = parser.parse_args()

    # Create github API instance and get account root.
    gh = Github(args.username, args.password)
    root = gh.get_user(args.github_root)

    # Set author and maintainer if none are specified.
    author = args.author if args.author is not None else root.name
    maintainer = args.maintainer if args.maintainer is not None else root.name

    # Make sure output directory exists if specified and change to it.
    if args.output is not None:
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        os.chdir(args.output)

    # Process all Arduino library names from standard input.
    for repo_name in sys.stdin:
        repo_name = repo_name.strip()
        # Skip blank lines.
        if repo_name == '':
            continue
        print('Processing {0}...'.format(repo_name))
        # Get repository from github to find its description and other metadata.
        repo = root.get_repo(repo_name)
        # Create subdirectory for repo if it doesn't exist.
        if not os.path.exists(repo_name):
            os.makedirs(repo_name)
        # Create library.properties file for the repo.
        with open(os.path.join(repo_name, 'library.properties'), 'w') as libfile:
            # Fill library.properties file with information about the repo.
            # See this page for information on each value:
            #  https://github.com/arduino/Arduino/wiki/Arduino-IDE-1.5:-Library-specification#libraryproperties-file-format
            # First pick a name by using the repo name and converting _ and - to
            # whitespace.
            name = repo.name.translate({ord('-'): u' ', ord('_'): u' '})
            libfile.write('name={0}\n'.format(name))
            # Write version, autho, and maintainer.
            libfile.write('version={0}\n'.format(args.version))
            libfile.write('author={0}\n'.format(author))
            libfile.write('maintainer={0}\n'.format(maintainer))
            # Use repo description as sentence and paragraph description.  If no
            # description is assigned to the repo then just use the repo name.
            description = repo.description
            if description is None or description.strip() == '':
                description = name
            libfile.write('sentence={0}\n'.format(description))
            libfile.write('paragraph={0}\n'.format(description))
            # Assume category is 'Other'.  This should ideally be changed before
            # writing the file to the repo.  See this page for possible values:
            #   https://github.com/arduino/Arduino/wiki/Arduino-IDE-1.5:-Library-specification#libraryproperties-file-format
            libfile.write('category=Other\n')
            # Use repo URL on Github as the library URL.
            libfile.write('url={0}\n'.format(repo.html_url))
            # Assume library works with all architectures.  Ideally this should
            # be changed before writing the file to the repo if it only supports
            # a few architectures.
            libfile.write('architectures=*\n')
