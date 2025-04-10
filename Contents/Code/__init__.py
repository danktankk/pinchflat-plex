#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
import json
import os
import re
import ssl
import sys
from io import open
import urllib2

try:
    from ssl import PROTOCOL_TLS as SSL_PROTOCOL
except ImportError:
    from ssl import PROTOCOL_SSLv23 as SSL_PROTOCOL  # Python < 2.7.13
try:
    from urllib.request import HTTPError, Request, urlopen  # Python >= 3.0
except ImportError:
    from urllib2 import HTTPError, Request, urlopen  # Python 2.x

PF_CONFIG = {}
PLUGIN_PATH = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), "..", ".."))
PLEX_ROOT = os.path.abspath(os.path.join(PLUGIN_PATH, "..", ".."))
CachePath = os.path.join(PLEX_ROOT, "Plug-in Support", "Data", "com.plexapp.agents.pinchflat-agent", "DataItems")
PLEX_LIBRARY = {}
PLEX_LIBRARY_URL = "http://localhost:32400/library/sections/"
SOURCE = "Pinchflat Agent"
CON_AGENTS = ["com.plexapp.agents.none"]
REF_AGENTS = ["com.plexapp.agents.localmedia"]
LANGUAGES = [Locale.Language.NoLanguage, Locale.Language.English]

SSL_CONTEXT = ssl.SSLContext(SSL_PROTOCOL)
FILTER_CHARS = "\\/:*?<>|;"

# (Other functions remain as in the previous update.)
# For brevity, please refer to the previously provided updated agent code.
# It replaces all "TubeArchivist" strings with "Pinchflat" and renames TA_CONFIG → PF_CONFIG.
