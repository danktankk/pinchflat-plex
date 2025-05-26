#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pinchflat Series Scanner – Recursively maps YouTube channel folders to Plex episodes.
- Each channel folder under the library root becomes a TV show.
- Supports videos inside subfolders (e.g. date-named or "Season XX" folders).
- Episode title derived from filename (with any leading date removed).
- All videos are initially assigned to Season 1 (agent will regroup by year later).
Compatible with Plex 1.41+ (Python 2.7).
"""
import os, re
import Media, VideoFiles, Stack

# Define video file extensions to recognize
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv', '.wmv', '.mpg', '.mpeg', '.m4v'}

# Pattern to detect a leading date (YYYYMMDD or YYYY-MM-DD) in file or folder names
DATE_PREFIX_RE = re.compile(r'^[0-9]{4}[-]?(?:[0-9]{2})[-]?(?:[0-9]{2})[ _-]+')

def Scan(path, files, mediaList, subdirs, language=None, root=None):
    # If at library root, do nothing (let Plex scan channel subfolders next)
    if root is None or path == root:
        return

    # Determine the channel (show) name from this folder
    show_name = os.path.basename(path)
    # We will treat all episodes as Season 1 initially
    season_num = 1
    episode_index = 1

    # If this directory has subdirectories, we will handle them here (to catch nested videos) and prevent deeper scanning.
    # We'll gather videos from all subdirs and include them as episodes.
    # After that, we clear subdirs list to stop Plex from scanning further (to avoid duplicates).
    for subdir in list(subdirs):
        sub_path = os.path.join(path, subdir)
        # Recurse into subdirectory to find video files
        for dirpath, _, filenames in os.walk(sub_path):
            for fname in filenames:
                ext = os.path.splitext(fname)[1].lower()
                if ext in VIDEO_EXTENSIONS:
                    file_path = os.path.join(dirpath, fname)
                    # Derive episode title from filename (strip extension and any leading date prefix)
                    title = os.path.splitext(fname)[0]
                    title = re.sub(DATE_PREFIX_RE, '', title).strip() or title
                    episode = Media.Episode(show_name, season_num, episode_index, title, None)
                    episode.parts.append(file_path)
                    mediaList.append(episode)
                    episode_index += 1
        # Remove the subdir from further processing (we've handled its content)
        subdirs.remove(subdir)

    # Also consider video files directly in the current directory
    files.sort()  # sort files for consistent order
    for file_path in files:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in VIDEO_EXTENSIONS:
            continue
        fname = os.path.basename(file_path)
        title = os.path.splitext(fname)[0]
        title = re.sub(DATE_PREFIX_RE, '', title).strip() or title
        episode = Media.Episode(show_name, season_num, episode_index, title, None)
        episode.parts.append(file_path)
        mediaList.append(episode)
        episode_index += 1

    # (No need to descend further; subdirs have been handled above)
    # End of Scan function.
