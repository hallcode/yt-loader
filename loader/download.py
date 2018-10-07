import os

from clint.textui import puts, indent, columns, colored
from pytube import YouTube, exceptions

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
    try:
        video = YouTube(videoURL, on_progress_callback=drawProgressBar)
    except Exception as e:
        if row[3] != '':
            videoTitle = row[3]
        else:
            videoTitle = 'Unable to read video title'

        # Print error line
        with indent(4):
            puts('\r', '')
            puts(columns(
                [colored.blue(videoRef), 14],
                [videoTitle[:48], 50],
                [colored.red('ERROR: Invalid URL'), 50]
            ))

        return False

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
    except Exception as e:
        # Print error line
        with indent(4):
            puts('\r', '')
            puts(columns(
                [colored.blue(videoRef), 14],
                [videoPath[:48], 50],
                [colored.red('ERROR: Unable to download video'), 50]
            ))