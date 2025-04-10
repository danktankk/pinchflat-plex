import os
import Media, VideoFiles, Stack

# List of video file extensions we will recognize as episodes
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv', '.wmv', '.mpg', '.mpeg', '.m4v'}

def Scan(path, files, media, dirs, language=None, root=None):
    """
    Custom Plex scanner for YouTube channel folders (Pinchflat downloads).
    - Each folder under the library root is treated as a TV series (show) named after that folder.
    - All video files in a folder become episodes in Season 1 of that series.
    - Episode title is the filename (without extension).
    - Non-video files (e.g., .jpg thumbnails) are ignored.
    """
    # If at the root of the library (no subpath yet), do nothing special
    if not path or path == "":
        # Let Plex continue into subdirectories (channel folders)
        return

    # Determine the show (series) name from the folder name
    show_name = os.path.basename(path)
    season_num = 1  # we place all episodes in Season 1

    # Sort the files for consistent episode ordering (alphabetical by filename)
    files.sort()
    episode_number = 1

    for file in files:
        # Get file extension and check if it's a recognized video format
        ext = os.path.splitext(file)[1].lower()
        if ext not in VIDEO_EXTENSIONS:
            # Skip non-video files (thumbnails, subtitles, etc.)
            continue

        # Derive episode title from filename (without extension)
        episode_title = os.path.splitext(os.path.basename(file))[0]

        # Create a new Episode media object
        # Use show_name as series title, season_num as season number, episode_number as episode
        # and episode_title as the title. We don't have a year, so pass None.
        episode = Media.Episode(show_name, season_num, episode_number, episode_title, None)
        episode.parts.append(file)  # attach the video file to this episode

        media.append(episode)
        episode_number += 1

    # If any subdirectories exist, let Plex know to descend into them (though in our case, 
    # channel folders typically contain no further subfolders for seasons)
    for d in dirs:
        dirs.remove(d)  # We handle all episodes directly in the channel folder, no deeper scan needed
