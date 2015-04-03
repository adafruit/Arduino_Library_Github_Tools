Arduino Library Github Tools
============================

Scripts to help identify and prepare Arduino libraries on Github for publication
to Arduino's library manager.  This is useful if you have a lot of Arduino
libraries on a Github account and want to make them available in Arduino's
library manager without having to do a lot of manual changes to each library.

The scripts are written in Python and tested with Python 2.7.9.

Background
----------

You'll want to familiarize yourself with the [Arduino library manager][0]
and the [library format][1]. At a high level the steps to publish a library are:

-   Add a [library.properties file][2] to the root of the library and populate
    the fields with appropriate values.

-   Create a release on the library's Github repository and set the release
    tag to the library version (following the [semantic version standard][3],
    like 1.0.0 for example).  Note that each tagged release will be shown in
    the library manager as a different library version that users can choose to
    install.

-   Make Arduino aware of the URL to your library's Github repository by
    opening a bug on their repository [as mentioned here][4].

The scripts in this repository will help automate all three steps of the
process above for a potentially large number of Arduino libraries that a Github
user/organization owns.

[0]: https://github.com/arduino/Arduino/wiki/Library-Manager-FAQ

[1]: https://github.com/arduino/Arduino/wiki/Arduino-IDE-1.5:-Library-specification

[2]: https://github.com/arduino/Arduino/wiki/Arduino-IDE-1.5:-Library-specification#libraryproperties-file-format

[3]: http://semver.org/

[4]: https://github.com/arduino/Arduino/wiki/Library-Manager-FAQ#how-can-i-add-my-library-to-library-manager

Dependencies
------------

You will need the [PyGithub module][5] installed to use these scripts.  The 
easiest way to install this module is with [pip][6], using the command:

    sudo pip install github

(omit the sudo on Windows)

[5]: https://github.com/PyGithub/PyGithub

[6]: https://pip.pypa.io/en/latest/installing.html

Usage
-----

The provided scripts perform the following actions:

-   find_libraries.py: Crawl all repositories for a Github user/organization and
    identify which ones look like Arduino libraries.

-   generate_properties.py: Automatically create a set of library.properties
    files for a list of Arduino libraries.  The name and description of each
    library will be set based on the name and description of the library's
    Github repository.

-   upload_properties.py: Upload a set of library.properties files for Arduino
    libraries to Github.

-   create_releases.py: Automatically create and tag a release for a set of
    Arduino libraries on Github.

-   generate_list.py: Build a list of Arduino library Github URLs that can be
    submitted to the Arduino team for inclusion in their master library list.

Each script is run from the command line and takes input from command line
parameters and in some cases standard input.  Commands can be run with a --help
parameter to print usage information.  For example run:

    python find_libraries.py --help

To see usage information about the find_libraries.py script printed.

In general each script needs to access Github using the credentials of a user
with read and write access to Arduino libraries on Github.  Credentials can be
passed to each script either as command line parameters or through environment
variables (and if both are present values given as command line parameters take
precedence).  For example to specify credentials as command line parameters
call a script with the --username and --password parameters like:

    python find_libraries.py --username foo --password bar

Where a user 'foo' with password 'bar' will be used to access Github.
Alternatively the environment variables GITHUB_USERNAME and GITHUB_PASSWORD can
be set to provide these values like (assuming a bash/Linux environment):

    export GITHUB_USERNAME=foo GITHUB_PASSWORD=bar
    python find_libraries.py

License
-------

The MIT License (MIT)

Copyright (c) 2015 Adafruit Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
