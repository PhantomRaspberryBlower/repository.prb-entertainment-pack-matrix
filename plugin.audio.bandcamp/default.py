# https://docs.python.org/2.7/
import sys

from future.standard_library import install_aliases

install_aliases()
from future.utils import (PY3)

if PY3:
    from urllib.parse import parse_qs
else:
    from urlparse import parse_qs

import xbmcvfs
import xbmcgui
import xbmcplugin
import xbmcaddon
import random
import xbmc
from resources.lib.bandcamp_api import bandcamp
from resources.lib.bandcamp_api.bandcamp import Band, Album, Track, Label
from resources.lib.kodi.ListItems import ListItems
from resources.lib.downloads.downloads import Downloads

try:
    import StorageServer
except:
    from resources.lib.cache import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("plugin.audio.bandcamp", 24)  # (Your plugin name, Cache time in hours)


def build_main_menu():
    root_items = list_items.get_root_items(username)
    xbmcplugin.addDirectoryItems(addon_handle, root_items, len(root_items))
    xbmcplugin.endOfDirectory(addon_handle)


def build_band_list(bands, from_wishlist=False):
    band_list = list_items.get_band_items(bands, from_wishlist)
    xbmcplugin.addDirectoryItems(addon_handle, band_list, len(band_list))
    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(addon_handle)


def build_album_list(albums):
    albums_list = list_items.get_album_items(albums)
    xbmcplugin.addDirectoryItems(addon_handle, albums_list, len(albums_list))
    xbmcplugin.endOfDirectory(addon_handle)


def build_genre_list():
    genre_list = list_items.get_genre_items(cache.cacheFunction(bandcamp.get_genres))
    xbmcplugin.addDirectoryItems(addon_handle, genre_list, len(genre_list))
    xbmcplugin.endOfDirectory(addon_handle)


def build_subgenre_list(genre):
    subgenre_list = list_items.get_subgenre_items(genre, cache.cacheFunction(bandcamp.get_subgenres))
    xbmcplugin.addDirectoryItems(addon_handle, subgenre_list, len(subgenre_list))
    xbmcplugin.endOfDirectory(addon_handle)


def build_song_list(band, album, tracks, autoplay=False):
    track_list = list_items.get_track_items(band=band, album=album, tracks=tracks, to_band=True)
    if autoplay:
        ## Few hacks, check for more info: https://forum.kodi.tv/showthread.php?tid=354733&pid=2952379#pid2952379
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=track_list[0][1])
        xbmc.sleep(2000)
        for url, list_item, folder in track_list[1:]:
            playlist.add(url, list_item)
    else:
        xbmcplugin.addDirectoryItems(addon_handle, track_list, len(track_list))
        xbmcplugin.setContent(addon_handle, 'songs')
        xbmcplugin.endOfDirectory(addon_handle)


def build_search_result_list(items):
    item_list = []
    for item in items:
        if isinstance(item, Band):
            item_list += list_items.get_band_items([item], from_search=True)
        elif isinstance(item, Album):
            item_list += list_items.get_album_items([item])
        elif isinstance(item, Label):
            item_list += list_items.get_label_items([item], from_search=True)            
    xbmcplugin.addDirectoryItems(addon_handle, item_list, len(item_list))
    xbmcplugin.endOfDirectory(addon_handle)


def build_featured_list(bands):
    for band in bands:
        for album in bands[band]:
            track_list = list_items.get_track_items(band=band, album=album, tracks=bands[band][album], to_album=True, to_band=True)
            xbmcplugin.addDirectoryItems(addon_handle, track_list, len(track_list))
    xbmcplugin.setContent(addon_handle, 'songs')
    xbmcplugin.endOfDirectory(addon_handle)


def play_song(url):
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)


def search(query, query_type=None):
    build_search_result_list(bandcamp.search(query, query_type))


def download_all_albums(band_id=1):
    Downloads(addon).download_all_albums(band_id=band_id)

def download_album(album_id, item_type, band_id=1):
    Downloads(addon).download_album(album_id=album_id, item_type=item_type,
                                    band_id=band_id, update_library=True)


def download_song(track_file, title, album_artist, album_name, rel_year, genre,
                  track_number, publisher=None, comment=None, image_file=None):
    Downloads(addon).download_song(track_file, title, album_artist, album_name, rel_year, genre, track_number, publisher, comment, image_file)


def main():
    args = parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)
    # For testing purposes
    #dialog = xbmcgui.Dialog()
    #dialog.ok("Mode", str(mode))

    if mode is None:
        build_main_menu()
    elif mode[0] == 'stream':
        play_song(args['url'][0])
    elif mode[0] == 'list_discover':
        build_genre_list()
    elif mode[0] == 'list_collection':
        build_band_list(bandcamp.get_collection(bandcamp.get_fan_id()))
    elif mode[0] == 'list_wishlist':
        build_band_list(bandcamp.get_wishlist(bandcamp.get_fan_id()), from_wishlist=True)
    elif mode[0] == 'list_wishlist_albums':
        bands = bandcamp.get_wishlist(bandcamp.get_fan_id())
        band = Band(band_id=args.get('band_id', None)[0])
        build_album_list(bands[band])
    elif mode[0] == 'list_search_albums':
        band, albums = bandcamp.get_band(args.get('band_id', None)[0])
        build_album_list(albums)
    elif mode[0] == 'list_albums':
        bands = bandcamp.get_collection(bandcamp.get_fan_id())
        band = Band(band_id=args.get('band_id', None)[0])
        build_album_list(bands[band])
    elif mode[0] == 'list_songs':
        album_id = args.get('album_id', None)[0]
        item_type = args.get('item_type', None)[0]
        genres_lst = xbmcvfs.translatePath('special://home/addons/plugin.audio.bandcamp/resources/music_genres.lst')
        build_song_list(*bandcamp.get_album(album_id=album_id, item_type=item_type, genres_lst=genres_lst))
    elif mode[0] == 'list_subgenre':
        genre = args.get('category', None)[0]
        build_subgenre_list(genre)
    elif mode[0] == 'list_subgenre_songs':
        genre = args.get('category', None)[0]
        subgenre = args.get('subcategory', None)[0]
        slices = []
        if addon.getSetting('slice_top') == 'true':
            slices.append("top")
        if addon.getSetting('slice_new') == 'true':
            slices.append("new")
        if addon.getSetting('slice_rec') == 'true':
            slices.append("rec")
        discover_dict = {}
        for slice in slices:
            discover_dict.update(bandcamp.discover(genre, subgenre, slice))
        shuffle_list = list(discover_dict.items())
        random.shuffle(shuffle_list)
        discover_dict = dict(shuffle_list)
        build_featured_list(discover_dict)
    elif mode[0] == 'search':
        action = args.get("action", None)[0]
        query = args.get("query", [""])[0]
        if action == 'new':
            options = [addon.getLocalizedString(30207),
                       addon.getLocalizedString(30208),
                       addon.getLocalizedString(30209),
                       addon.getLocalizedString(30210)]
            index = xbmcgui.Dialog().select('Search', list=options)
            query = xbmcgui.Dialog().input(addon.getLocalizedString(30103))
            if query:
                # Search band
                if index == 0:
                    search(query, 'b')
                # Search album
                if index == 1:
                    search(query, 'a')
                # Search track
                if index == 2:
                    search(query, 't')
                # Search everything
                if index == 3:
                    search(query)
    elif mode[0] == 'url':
        url = args.get("url", None)[0]
        build_song_list(*bandcamp.get_album_by_url(url), autoplay=True)
    elif mode[0] == 'settings':
        addon.openSettings()
    elif mode[0] == 'download_all_albums':
        band_id = args.get('band_id', None)[0]
        download_all_albums(band_id=band_id)
    elif mode[0] == 'download_album':
        album_id = args.get('album_id', None)[0]
        item_type = args.get('item_type', None)[0]
        band_id = args.get('band_id', None)[0]
        download_album(album_id=album_id, item_type=item_type)
    elif mode[0] == 'download_song':
        url = args.get('url', None)[0]
        title = args.get('title', None)[0]
        album_artist = args.get('album_artist', None)[0]
        album_name = args.get('album_name', None)[0]
        rel_year = args.get('rel_year', None)[0]
        genre = args.get('genre', None)[0]
        track_number = args.get('track_number', None)[0]
        publisher = args.get('publisher', None)[0]
        comment = args.get('comment', None)[0]
        image_file = args.get('image_file', None)[0]
        download_song(track_file=url, title=title, album_artist=album_artist, album_name=album_name,
                      rel_year=rel_year, genre=genre, track_number=track_number, publisher=publisher,
                      comment=comment, image_file=image_file)

if __name__ == '__main__':
    xbmc.log("sys.argv:" + str(sys.argv), xbmc.LOGDEBUG)
    addon = xbmcaddon.Addon()
    list_items = ListItems(addon)
    username = addon.getSetting('username')
    bandcamp = bandcamp.Bandcamp(username)
    addon_handle = int(sys.argv[1])
    main()
