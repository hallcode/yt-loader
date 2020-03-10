import click, csv, re
from .download import download_video

# Dont hate me
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

@click.command()
@click.argument('csv_path', type=click.Path(exists=True))
def main(csv_path):
    """
    Uses a CSV file to download multiple YouTube videos at once.

    The columns in the CSV file should be as follows. Only the first column is required:

    /b
    [0] YouTube URL (or video hash)
    [1] output sub-directory
    [2] options (see README)
    [3] Output filename
    """
    with open(csv_path, newline='') as csvFile:
        csv_object = csv.reader(csvFile, delimiter=',')

        for row in csv_object:
            # Get URL
            # Check that the URL contains correct domain, otherwise add it
            url_regex = r"v=([^&]+)"
            youtube_url = "https://youtu.be/"
            match = re.search(url_regex, row[0])

            if match:
                video_ref = match.group(1)
            else:
                video_ref = row[0]

            video_url = youtube_url + video_ref

            try:
                download_video(video_url, video_ref, row)
            except Exception as e:
                click.secho('Error: '+e.message, fg="red")

    return None
