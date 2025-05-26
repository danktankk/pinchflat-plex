# Pinchflat Plex Agent v0.2.0
import os, json, datetime

INFO_SUFFIX  = '.info.json'
THUMB_SUFFIX = '-thumb.jpg'
DEBUG        = True
LOG_TAG      = '[Pinchflat]'

def log(msg, *args):
    if DEBUG:
        Log.Debug('%s %s' % (LOG_TAG, (msg % args)))

def load_json(path):
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, 'r') as fh:
            return json.load(fh)
    except Exception as e:
        Log.Warning('%s cannot read %s – %s' % (LOG_TAG, path, e))
        return {}

def channel_art_from_json(j):
    for key in ('uploader_thumbnail', 'thumbnail'):
        val = j.get(key)
        if val:
            return val
    return None

class PinchflatAgent(Agent.TV_Shows):
    name             = 'Pinchflat Agent'
    languages        = [Locale.Language.NoLanguage, Locale.Language.English]
    primary_provider = True
    contributes_to   = ['com.plexapp.agents.none']

    # one show = one YouTube folder
    def search(self, results, media, lang, manual):
        show_dir = os.path.basename(os.path.dirname(media.filename))
        results.Append(MetadataSearchResult(id=show_dir, name=show_dir,
                                            score=100, lang=lang))

    # fill in show + episode data
    def update(self, metadata, media, lang, force):
        if not media.items or not media.items[0].parts:
            return

        first_part = media.items[0].parts[0].file
        show_root  = os.path.dirname(first_part)
        lib_root   = os.path.dirname(show_root)

        # ---------- SHOW-LEVEL ----------
        show_json = load_json(os.path.splitext(first_part)[0] + INFO_SUFFIX)

        metadata.title   = (show_json.get('uploader')
                            or show_json.get('channel')
                            or os.path.basename(show_root))
        metadata.summary = (show_json.get('uploader_url')
                            or show_json.get('channel_url', ''))
        metadata.studio  = 'YouTube'

        # remote avatar / channel art
        remote_art = channel_art_from_json(show_json)
        if remote_art:
            metadata.posters[remote_art] = Proxy.Media(remote_art)
            metadata.art[remote_art]     = Proxy.Media(remote_art)
            metadata.banners[remote_art] = Proxy.Media(remote_art)

        # single library-wide fallbacks (keep them once in the YouTube root)
        chan_fb = os.path.join(lib_root, 'channel-fallback.jpg')
        back_fb = os.path.join(lib_root, 'backdrop-fallback.jpg')
        if os.path.isfile(chan_fb):
            metadata.posters[chan_fb] = Proxy.LocalFile(chan_fb)
        if os.path.isfile(back_fb):
            metadata.art[back_fb]     = Proxy.LocalFile(back_fb)
            metadata.banners[back_fb] = Proxy.LocalFile(back_fb)

        # ---------- EPISODES ----------
        for season_key in media.seasons:
            for ep_key in media.seasons[season_key].episodes:
                ep_media   = media.seasons[season_key].episodes[ep_key]
                ep_meta    = metadata.seasons[season_key].episodes[ep_key]
                video_path = ep_media.items[0].parts[0].file
                base_path  = os.path.splitext(video_path)[0]
                epi_json   = load_json(base_path + INFO_SUFFIX)

                # text fields
                if epi_json:
                    ep_meta.title   = epi_json.get('title', ep_meta.title)
                    ep_meta.summary = epi_json.get('description',
                                                   ep_meta.summary)

                    date_str = epi_json.get('upload_date')
                    if date_str and len(date_str) == 8:
                        dt = datetime.datetime.strptime(date_str, '%Y%m%d')
                        ep_meta.originally_available_at = dt
                        ep_meta.season = dt.year
                        ep_meta.index  = int(date_str)   # yyyymmdd

                # artwork – prefer local thumb, else remote thumbnail
                local_thumb = base_path + THUMB_SUFFIX
                if os.path.isfile(local_thumb):
                    key = 'local'
                    ep_meta.thumbs[key]  = Proxy.LocalFile(local_thumb)
                    ep_meta.posters[key] = Proxy.LocalFile(local_thumb)
                else:
                    remote_thumb = epi_json.get('thumbnail')
                    if remote_thumb:
                        ep_meta.thumbs[remote_thumb]  = Proxy.Media(remote_thumb)
                        ep_meta.posters[remote_thumb] = Proxy.Media(remote_thumb)

        log('updated show %s', metadata.title)

def Start():
    pass
