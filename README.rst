YouTube Loader is a command line tool written in Python which reads a CSV file containing a list of YouTube URLs and downloads
them all at once.

Usage
=====
The command has the following syntax:
``yt-loader [CSV_PATH]``

CSV_PATH must be a valid file path pointing to a csv file matching the specification below.

CSV File Format
---------------
The minimum requirements for the csv file would just be a YouTube URL or id hash on each line. You can add optional columns
as follows::

    [0] YouTube URL / ID Hash
    [1] Directory (will save to top-level directory if blank)
    [2] Options (see below)
    [3] File name (optional - if left blank will use the video title from YouTube)

Options
-------
:audio:
    Downloads only the audio stream.

:split:
    downloads the highest available quality video and audio streams as separate files, appended with '_audio' and '_video'
    respectively.

    The default behaviour (if this is left blank) will be to download the best available joint video/audio stream, which
    will be of a slightly lower quality (but still probably HD - depending on the source.

Example CSV
-----------
Below is an example CSV file::

    H-uJY1NnwfI,News,,Junior Doctors Strike
    http://www.youtube.com/watch?v=vs7VknlKcaM,News,,Lightening in scotland
    XA4CE8LfzY0,News,,
    tlJSxBFzahY,Culture,,2016 - Logan Paul
    35XptNZU2OA,Music,audio,We Can Be Heroes

Installation
============
You should be able to download the script using PIP:
``pip install yt-loader``

Eventually I plan to make the script available via homebrew too, but beyond that you would have to download the source.