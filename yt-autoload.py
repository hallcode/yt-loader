from clint import arguments
from pytube import YouTube

from clint.textui import puts, indent, colored, columns

import csv
import re
import os

# Dont hate me
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

def main():
    # Get first argument passed
    # Argument should be the path to the csv file
    args = arguments.Args()
    filePath = args.get(0)

    if filePath:
        try:
            with open(filePath, newline='') as csvFile:
                csvObject = csv.reader(csvFile, delimiter=',')

                for row in csvObject:
                    # Get URL
                    # Check that the URL contains correct domain, otherwise add it
                    urlRegex = r"v=([^&]+)"
                    YouTubeURL = "https://www.youtube.com/watch?v="
                    match = re.search(urlRegex, row[0])
                    if match:
                        videoRef = match.group(1)
                    else:
                        videoRef = row[0]

                    videoURL = YouTubeURL + videoRef

                    try:
                        downloadVideo(videoURL, videoRef, row)
                    except Exception as e:
                        puts(colored.red('Error: ')+e)

        except IOError as e:
            puts(colored.red('Error: ') + 'File does not exist or you do not have permission to access it.')

    else:
        puts(colored.red('ERROR: ') + 'No file path specified.')

def drawProgressBar(stream=None, chunk=None, file_handle=None, remaining=None):
    file_size = stream.filesize
    percent = (100 * (file_size - remaining)) / file_size

    puts('\r', '')
    with indent(4):
        puts(columns(
            ["{:.2f}".format(remaining * 0.000001) + ' MB', 8],
            ['/',1],
            ["{:.2f}".format(file_size * 0.000001) + ' MB', 8],
            ["({:.2f} %)".format(percent), 10]
        ), '')

def downloadVideo(videoURL, videoRef, row):
    # Create YouTube video object
    text = "a string"
    video = YouTube(videoURL, on_progress_callback=drawProgressBar)

    # Work out new title
    if row[3] != '':
        videoTitle = row[3]
    else:
        videoTitle = video.title

    # Work out path
    folder = ''
    if row[1] != '':
        folder = row[1]

    videoPath = os.path.join(folder, videoTitle)
    fullPath = os.path.join(os.getcwd(),folder)

    # Create required directory
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)

    # Do Download
    try:
        if row[2] == 'audio':
            # Only load audio streams
            audioStream = stream = video.streams.filter(only_audio=True).first()
            audioStream.download(output_path=fullPath, filename=videoTitle + '_audio')

            size = format(stream.filesize * 0.000001, '.2f') + ' MB'

        elif row[2] == 'high' or row[2] == 'split':
            # Load split streams (With higher quality)
            videoStream = video.streams.filter(adaptive=True).first()
            audioStream = video.streams.filter(only_audio=True).first()

            audioStream.download(output_path=fullPath, filename=videoTitle+'_audio')
            videoStream.download(output_path=fullPath, filename=videoTitle+'_video')
            size = format(videoStream.filesize * 0.000001, '.2f') + ' MB'

        else:
            # Download streams
            stream = video.streams.filter(progressive=True).first()
            stream.download(output_path=fullPath, filename=videoTitle)
            size = format(stream.filesize * 0.000001, '.2f') + ' MB'

        # Print line
        with indent(4):
            puts('\r','')
            puts(columns(
                [colored.blue(videoRef), 14],
                [videoPath[:48], 50],
                [size, 11],
                [colored.green('DONE'), 20]
            ))
    except FileNotFoundError as e:
        # Print error line
        with indent(4):
            puts('\r', '')
            puts(columns(
                [colored.blue(videoRef), 14],
                [videoPath[:48], 50],
                [colored.red('ERROR'), 50]
            ))

# Run
if __name__ == '__main__':
    main()