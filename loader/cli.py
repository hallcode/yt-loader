import click, csv, re
from .download import downloadVideo

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
    [1] options (see README)
    [2] output sub-directory
    [3] Output filename
    """
    with open(csv_path, newline='') as csvFile:
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
                click.secho('Error: '+e, fg="red")

    return None
