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

[0]: https://github.com/arduino/library-registry/blob/main/FAQ.md#readme

[1]: https://arduino.github.io/arduino-cli/0.35/library-specification/#15-library-format-rev-22

[2]: https://arduino.github.io/arduino-cli/0.35/library-specification/#libraryproperties-file-format

[3]: http://semver.org/

[4]: https://github.com/arduino/library-registry/blob/main/FAQ.md#how-can-i-add-a-library-to-library-manager

Dependencies
------------

You will need the [PyGithub module][5] installed to use these scripts.  The 
easiest way to install this module is with [pip][6], using the command:

    sudo pip install pygithub

(omit the sudo on Windows)

[5]: https://github.com/PyGithub/PyGithub

[6]: https://pip.pypa.io/en/latest/installation/

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
with read and write access to your Arduino libraries on Github.  Credentials can be
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

To explain the usage of the scripts follow a walkthrough below of how Adafruit's
libraries were populated using them.  For brevity all of the script calls below
will omit the --username and --password parameters, but remember those are
required (or the GITHUB_USERNAME and GITHUB_PASSWORD environment variables
need to be set).

First generate a list of all public Arduino libraries for the adafruit Github
organization.  Save the output to the file adafruit_arduino_libraries.txt:

    python find_libraries.py --type public adafruit > adafruit_arduino_libraries.txt

The --type parameter allows you to filter to a specific type of repository
like public ones (run the script with just the --help parameter to see possible
options).

The adafruit parameter is the name of the Github user/organization to scan for
Arduino libraries.  Change this to your Github user/organization name.

If you have a lot of of repositories on Github the command can take some time to
run as each repository is individually examined.  A full scan of Adafruit's 300+
repositories took about 5 minutes.

Now examine the output file and remove any lines that are repositories which are
not Arduino libraries or which you explicitly don't want to process further.

Note that before you process the entire list it would be prudent to make a list
with only one or two libraries and use it for the next steps to do a 'dry run'
of generating properties, uploading properties, and tagging releases.  Once
everything looks good, then run the full list through all the steps.

Next generate all the library.properties files and save them in a subfolder
called arduino_libs using the command below:

    python generate_properties.py --output arduino_libs --author "Adafruit" --maintainer "Adafruit <info@adafruit.com>" adafruit < adafruit_arduino_libraries.txt

The --output parameter specifies a subdirectory to create that will be the root
of all the generated library.properties files (if not specified the current
directory will be used).

The --author and --maintainer parameters specify nicer names for those properties
in the generated files.  

Again the Github user/organization name is specified as the only positional
parameter.

Notice the list of Arduino libraries generated earlier is piped as standard input
to the script.

Now go through the library.properties files inside the arduino_libs subfolder
hierarchy and fix up any descriptions, names, etc.  Be sure to set a sensible
category as the default is 'Other' (see [this page][2] for the list of possible
categories).

Then upload all the library.properties files inside the arduino_libs subfolder
hiearchy:

    python upload_properties.py --root arduino_libs adafruit

The --root parameter specifies a folder that is the root of the library.properties
files (i.e. the output of the last command).  The Github user/organization is
specified in the only positional parameter.

Now create and tag a 1.0.0 release for each library on Github by running:

    python create_releases.py adafruit < adafruit_arduino_libraries.txt

The only parameter is the name of the Github user/organization, and again notice
the list of Arduino libraries to process is piped in to standard input from the
list generated earlier.

Finally generate the list of Arduino library URLs to send to the Arduino team:

    python generate_list.py adafruit < adafruit_arduino_libraries.txt > adafruit_arduino_library_urls.txt

The Github user/organization is specified as a parameter, then the input file is
piped to standard input and the output list is piped to a file.

Now send the adafruit_arduino_library_urls.txt file to the Arduino team in an
issue on their Github repository (see [this page][4] for details)!

After your libraries are visible in Arduino's manager be aware as they are changed 
on your Github repository they will NOT be automatically picked up by Arduino's library system.
Only when a new tagged release is created will Arduino pick up the library as updated.

For example if a library has a tagged release with version 1.0.0 and new fixes are
integrated then be sure to create a new tagged release with a higher version,
like 1.0.1, after integrating the fixes.  Arduino's library system should pick
up the new tag & release after processing the library again (apparently happens
every few hours).

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
