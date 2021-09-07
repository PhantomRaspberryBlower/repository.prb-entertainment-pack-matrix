import urllib.request, urllib.parse, urllib.error
import os
import re
import requests
import xbmc
import xbmcgui
import xbmcvfs
from threading import Thread
from resources.lib.net import Net

from resources.lib import settings
from resources.lib import commontasks
from resources.lib.setid3tags import Setid3Tags
from resources.lib.artistinfo import ArtistInfo

'''
Written by: Phantom Raspberry Blower
Date: 21-08-2017
Description: Addon for streaming / downloading music
             and artwork. Derived from plugin.audio.mp3streams
'''

# Get addon details
__addon__ = settings.addon()
__download_list__ = settings.download_list()
__id3tags_list__ = settings.id3tags_list()
__music_dir__ = settings.music_dir()
__queue_downloads__ = settings.queue_downloads()
__show_progress__ = settings.show_progress()
__artist_art__ = settings.artist_icons()

# Get localized language text
__language__ = __addon__.getLocalizedString
_downloads = __language__(30005)
_unlocked = __language__(30016)
_download_added = __language__(30045)
_err_downloading = __language__(30088)
_album_download_in_progress = __language__(30021)
_please_wait_for_current_download = __language__(30022)
_downloading = __language__(30055)
_n_of_n_tracks_downloaded = __language__(30056)
_download_started = __language__(30014)
_album_download_finished = __language__(30015)
_something_wicked_happened = __language__(30090)

cookie_jar = settings.cookie_jar()
net = Net()

MUSIC_DIR_URL = 'https://mp3music.ru'
MUSIC_LISTEN_URL = 'https://listen.musicmp3.ru/'

g_downloads_in_progress = False
g_error_report = []


resources = xbmcvfs.translatePath(os.path.join('special://home/addons/'
                                               'plugin.audio.mp3music',
                                               'resources'))
fanart = xbmcvfs.translatePath(os.path.join(resources, 'fanart.jpg'))
iconart = xbmcvfs.translatePath(os.path.join(resources, 'icon.png'))
download_lock = os.path.join(__music_dir__,  'downloading.txt')


def get_current_artist_images(artistname=None, artistinfo=None):
    '''
    Discover artist name, download image and return the image path.
    If no image can be found return the default image instead
    '''
    fanartimage = ''
    thumb = ''
    days = 28
    if len(artistname) > 1:
        # Find the artist information
        if artistinfo == None:
            artist_info = ArtistInfo(artistname)
        else:
            artist_info = artistinfo
        try:
            # Download artist thumbnail image
            icon_path = os.path.join(__music_dir__ + artistname, artistname + '.jpg')
            if (not os.path.exists(icon_path) and not artist_info.artist_thumb == None):
                urllib.request.urlretrieve(artist_info.artist_thumb, icon_path)
                commontasks.resize_image(icon_path, 256, 256)
            else:
                thumb = artist_info.artist_thumb
        except:
            # Use MP3 Music default thumbnail
            thumb = iconart
        try:
            # Download artist fanart image
            fanart_path = os.path.join(__music_dir__ + artistname, artistname + '_fanart.jpg')
            if (not os.path.exists(fanart_path) and not artist_info.fanart == None):
                urllib.request.urlretrieve(artist_info.fanart, fanart_path)
                commontasks.resize_image(icon_path, 1280, 720)
            else:
                fanartimage = artist_info.fanart
        except:
            # Use MP3 Music default fanart
            fanartimage = fanart
    return thumb, fanartimage


def clear_lock(path):
    if os.path.exists(path):
        os.remove(path)
        commontasks.notification(_downloads, _unlocked, iconart, 3000)
        xbmc.executebuiltin("Container.Refresh")


def get_url(url):
    header_dict = {}
    link = ''
    if 'mp3music' in url:
        header_dict['Accept'] = ('audio/webm,audio/ogg,udio/wav,audio/'
                                 '*;q=0.9,application/ogg;q=0.7,video/'
                                 '*;q=0.6,*/*;q=0.5')
        header_dict['User-Agent'] = 'AppleWebKit/<WebKit Rev>'
        header_dict['Host'] = 'mp3music.ru'
        header_dict['Referer'] = MUSIC_DIR_URL + '/'
        header_dict['Connection'] = 'keep-alive'
    if 'goldenmp3' in url:
        header_dict['Accept'] = ('text/html,application/xhtml+xml,'
                                 'application/xml;q=0.9,*/*;q=0.8')
        header_dict['User-Agent'] = ('Mozilla/5.0 (Windows NT 6.1; rv:35.0) '
                                     'Gecko/20100101 Firefox/35.0')
        header_dict['Host'] = 'www.goldenmp3.ru'
        header_dict['Referer'] = ('http://www.goldenmp3.ru/compilations/'
                                  'events/albums')
        header_dict['Connection'] = 'keep-alive'
    net.set_cookies(cookie_jar)
    try:
        link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
        net.save_cookies(cookie_jar)
        link = link.decode('utf-8')
    except:
        msg = "Error getting cookie"
        commontasks.notification(msg, _something_wicked_happened,iconart, 5000)
    return link


def remove_from_download_list(name, url, dir, text):
    if os.path.isfile(__download_list__):
        s = commontasks.read_from_file(__download_list__)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                splitlist = list.split('<>')
                artist = splitlist[2]
                album = splitlist[3]
                trackname = splitlist[4]
                year = splitlist[5]
                if len(trackname) < 1:
                    title = '%s - %s (%s)' % (artist, album, year)
                else:
                    title = '%s - %s (%s)' % (artist, trackname, year)
                if title == name:
                    commontasks.remove_from_list(list, __download_list__)
                    xbmc.executebuiltin('Container.Refresh')


def start_download(url, name, songname, artist, album, iconimage, year, genre, downloadtype):
    # Check download path exists
    if not os.path.isdir(__music_dir__):
        commontasks.message('Download location:\n%s\ndoes not exist' % __music_dir__, "Pennie plug it in!")
        return

    # Don't add further downloads until current download completes 
    check_downloads = os.path.join(__music_dir__, 'downloading.txt')
    if os.path.exists(check_downloads):
        dialog = xbmcgui.Dialog()
        dialog.ok(_album_download_in_progress,
                  _please_wait_for_current_download)
        return

    # Check wether to add to download queue or download immediately
    if __queue_downloads__ and not g_downloads_in_progress:
        if downloadtype == 'album':
            try:
                artist = name.split(' - ')[0]
                album = name.split(' - ')[1].split('(')[0]
                year = name[name.find("(")+1:name.find(")")]
            except:
                artist = "Various Artists"
                album = name
                year = year
        _add_to_download_list(url, songname, artist, album, iconimage, year, genre, downloadtype)
    else:
        # Stop futher downloads until the current download completes
        download_lock = commontasks.create_file(__music_dir__, "downloading.txt")

        if downloadtype == 'song':
            album_path = _download_song(url, name, songname, artist, album, iconimage, year, genre)
        elif downloadtype == 'album':
            album_path = _download_album(url, name, artist, album, iconimage, year, genre)

        # Remove download lock
        if os.path.exists(download_lock):
            os.remove(download_lock)

        # Verify Library source exists
        for item in commontasks.getLibrarySources('music'):
            # Verify download location is included in Library
            if item == __music_dir__:
                xbmc.executebuiltin('UpdateLibrary(music, %s)' % str(album_path))


def start_downloads_queue():
    global g_downloads_in_progress
    global g_error_report
    g_error_report = []
    g_downloads_in_progress = True
    dlThread = StartDownloads()
    dlThread.start()
    # Check if error occurred during download
    if len(g_error_report) > 0:
        text = ''
        for item in g_error_report:
            text += '%s\n' % item
        # Display error report
        commontasks.message(text, _err_downloading)


class StartDownloads(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global g_downloads_in_progress
        if os.path.isfile(__download_list__):
            s = commontasks.read_from_file(__download_list__)
            search_list = s.split('\n')
            for list in search_list:
                if list != '':
                    splitlist = list.split('<>')
                    url = splitlist[0]
                    # Remove invalid characters from file name
                    file_name = commontasks.validate_filename(str(splitlist[4]))
                    filename = os.path.join(splitlist[1], file_name).strip()
                    artist = splitlist[2]
                    album = splitlist[3]
                    trackname = splitlist[4]
                    year = splitlist[5]
                    genre =  splitlist[6].strip()
                    try:
                        iconimage = splitlist[7]
                    except:
                        iconimage = iconart
                    download_type = splitlist[8]
                    try:
                        start_download(url, filename, trackname, artist, album, iconimage, year, genre, download_type)
                        commontasks.remove_from_list(list, __download_list__)
                    except:
                        pass
        g_downloads_in_progress = False


def _add_to_download_list(url, songname, artist, album, iconimage, year, genre, downloadtype):
    album_path = os.path.join(__music_dir__, '%s/%s' % (artist, album))
    list_data = "%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s<>%s" % (url,
                                                        album_path.strip(),
                                                        artist.strip(),
                                                        album.strip(),
                                                        songname.strip(),
                                                        year,
                                                        urllib.parse.unquote(genre).replace('&amp;', '&'),
                                                        iconimage,
                                                        downloadtype)
    commontasks.add_to_list(list_data, __download_list__, False)
    if songname == '':
        song_album = album
    else:
        song_album = songname
    commontasks.notification('[COLOR orange]%s: %s[/COLOR]' % (artist, song_album), _download_added, iconimage, 5000)


def _download_music(url, album_path, artist, album, track, songname, year, genre, retry=True):
    global g_error_report
    list_data = "%s<>%s<>%s<>%s<>%s%s<>%s<>%s" % (album_path.strip(),
                                                  artist.strip(),
                                                  album.strip(),
                                                  track,
                                                  songname.strip(),
                                                  '.mp3',
                                                  year,
                                                  urllib.parse.unquote(genre).replace('&amp;', '&'))
    # Remove invalid characters from file name
    filename = commontasks.validate_filename(songname)
    local_filename = os.path.join(album_path.strip(), filename + '.mp3')
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'AppleWebKit/<WebKit Rev>')
    try:
        resp = urllib.request.urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            text = 'Failed to reach server. Reason: %s' % e.reason
        elif hasattr(e, 'code'):
            text = 'Server unable to complete request. Code: %s' % e.code
        # Add error to error report
        g_error_report.append('%s %s %s\n' % (artist, songname, text))
        commontasks.notification('[COLOR red]%s %s[/COLOR]' % (artist, songname), text, iconart, 5000)
    else:
        try:
            # Start Download
            headers = {'Host': 'listen.musicmp3.ru',
                       'Range': 'bytes=0-',
                       'User-Agent': 'AppleWebKit/<WebKit Rev>',
                       'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'}
            resp = requests.get(url, headers=headers, stream=True)
            _urlretrieve(resp, local_filename)
            # Add meta data to downloaded music
            commontasks.add_to_list(list_data, __id3tags_list__, False)
            _id3_tags()
        except:
            if retry == True:
                _download_music(url, album_path, artist, album, track, songname, year, genre, retry=False)
            else:
                # Add error to error report
                g_error_report.append('%s %s %s\n' % (artist, songname, _err_downloading))
                commontasks.notification('[COLOR red]%s %s[/COLOR]' % (artist, songname), _err_downloading, iconart, 5000)


def _download_album(url, name, artist, album, iconimage, year, genre):
    url = url.replace('mp3music', 'www.goldenmp3').replace('ru/compilation/', 'ru/compilations/')
    link = get_url(url)
    filtered_url = commontasks.regex_from_to(link,'<tbody>','</tbody>')
    std = ('href="#" rel="(.+?)" title="Listen the song in low quality">(.+?)</a>'
           '</td><td><div class="title_td_wrap">(.+?)<span itemprop="name">(.+?)<'
           '/span>(.+?)<div ')
    match = re.compile(std).findall(filtered_url)
    nSong = len(match)
    dialog = xbmcgui.Dialog()

    # Show download progress
    if __show_progress__:
        pDialog = xbmcgui.DialogProgressBG()
        pDialog.create(name, _downloading)
        percentage = 0

    playlist = []
    link = get_url(url)
    commontasks.notification('[COLOR orange]%s: %s[/COLOR]' % (artist, album), _download_started, iconimage, 3000)
    artist = artist.replace('&amp;', 'and')
    album = album.replace('&amp;', 'and')
    # Create artist path
    artist_path = commontasks.create_directory(__music_dir__, artist)
    # Download and save artist image to directory
    get_current_artist_images(artistname=artist)
    # Create album path
    album_path = commontasks.create_directory(artist_path, album)
    # Check for iconimage
    if iconimage.find('no_image') >0:
        iconimage = iconart
    # Download album cover artwork
    urllib.request.urlretrieve(iconimage, album_path + '/' + "Folder.jpg")
    # Fetch links for each song on the album
    for (song_id, crap1, track, songname, dur) in match:
        track = track.replace('.&ensp;', '')
        text = _n_of_n_tracks_downloaded % (track, nSong)
        if __show_progress__:
            pDialog.update(int(percentage), '%s: %s' % (artist, album), text.replace('downloaded', 'downloading'))
        url = MUSIC_LISTEN_URL + song_id
        songname = songname.replace('&amp;', 'and')
        title = "%s. %s" % (track, songname)
        dur = dur.replace('.ensp;', '')
        playlist.append(songname)
        title = "%s. %s" % (track.replace('track', ''), songname)
        try:
            # Download music
            _download_music(url, album_path, artist, album, track, title, year, genre)
            commontasks.notification('[COLOR orange]%s: %s[/COLOR]' % (artist, album), text, iconimage, 3000)
        except:
            pass
        # Update progress
        percentage = (float(track)/float(nSong)) * 100
    commontasks.notification('[COLOR orange]%s: %s[/COLOR]' % (artist, album),
                             _album_download_finished,
                             iconimage,
                             3000)
    # Remove progress bar
    if __show_progress__:
        pDialog.close()

    return album_path


def _download_song(url, name, songname, artist, album, iconimage, year, genre):
    try:
        track = int(songname[:songname.find('.')])
    except:
        track = 0

    # Show download progress
    if __show_progress__:
        pDialog = xbmcgui.DialogProgressBG()
        pDialog.create('%s: %s' % (artist, songname), _downloading)
        percentage = 0

    # Create artist and album directories
    artist_path = commontasks.create_directory(__music_dir__, artist)
    # Download and save artist image to directory
    get_current_artist_images(artistname=artist)
    # Create album path
    album_path = commontasks.create_directory(artist_path, album)

    # Download music
    try:
        _download_music(url, album_path, artist, album, track, songname, year, genre)
    except:
        pass

    # Close progress dialog
    if __show_progress__:
        pDialog.close()

    return album_path


def _urlretrieve(urlfile, fpath):
    with open(fpath, 'wb') as f:
        for chunk in urlfile.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
#    f.close()


def _id3_tags():
    id3Thread = Setid3Tags(__id3tags_list__)
    id3Thread.start()
