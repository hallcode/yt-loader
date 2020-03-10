import os

from clint.textui import puts, indent, columns, colored
from pytube import YouTube, exceptions

def draw_progress_bar(stream=None, chunk=None, file_handle=None, remaining=None):
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

def download_video(video_url, video_ref, row):
    # Create YouTube video object
    try:
        video = YouTube(video_url, on_progress_callback=draw_progress_bar)
    except Exception as e:
        if row[3] != '':
            video_title = row[3]
        else:
            video_title = '[Error]'

        # Print error line
        with indent(4):
            puts('\r', '')
            puts(columns(
                [colored.blue(video_ref), 14],
                [video_title[:48], 50],
                [colored.red('Error: Invalid name'), 50]
            ))

        return False

    # Work out new title
    if row[3] != '':
        video_title = row[3]
    else:
        video_title = video.title

    # Work out path
    folder = ''
    if row[1] != '':
        folder = row[1]

    video_path = os.path.join(folder, video_title)
    full_path = os.path.join(os.getcwd(),folder)

    # Create required directory
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    # Do Download
    try:
        if row[2] == 'audio':
            # Only load audio streams
            audio_stream = stream = video.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=full_path, filename=video_title + '_audio')

            size = format(stream.filesize * 0.000001, '.2f') + ' MB'

        elif row[2] == 'high' or row[2] == 'split':
            # Load split streams (With higher quality)
            video_stream = video.streams.filter(adaptive=True).first()
            audio_stream = video.streams.filter(only_audio=True).first()

            audio_stream.download(output_path=full_path, filename=video_title+'_audio')
            video_stream.download(output_path=full_path, filename=video_title+'_video')
            size = format(video_stream.filesize * 0.000001, '.2f') + ' MB'

        else:
            # Download streams
            stream = video.streams.filter(progressive=True).first()
            stream.download(output_path=full_path, filename=video_title)
            size = format(stream.filesize * 0.000001, '.2f') + ' MB'

        # Print line
        with indent(4):
            puts('\r','')
            puts(columns(
                [colored.blue(video_ref), 14],
                [video_path[:48], 50],
                [size, 11],
                [colored.green('DONE'), 20]
            ))
    except Exception as e:
        # Print error line
        with indent(4):
            puts('\r', '')
            puts(columns(
                [colored.blue(video_ref), 14],
                [video_path[:48], 50],
                [colored.red('ERROR: Unable to download video'), 50]
            ))