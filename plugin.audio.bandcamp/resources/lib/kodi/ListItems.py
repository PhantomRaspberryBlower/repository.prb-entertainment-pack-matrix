import sys

import xbmcgui
from future.standard_library import install_aliases

install_aliases()
from urllib.parse import urlencode


class ListItems:

    def __init__(self, addon):
        self.addon = addon
        self._download_all_albums = addon.getLocalizedString(30204)

    def _build_url(self, query):
        base_url = sys.argv[0]
        return base_url + '?' + urlencode(query)

    def get_root_items(self, username):
        items = []
        # discover menu
        _discover = self.addon.getLocalizedString(30101)
        li = xbmcgui.ListItem(label=_discover)
        url = self._build_url({'mode': 'list_discover'})
        items.append((url, li, True))
        # collection menu
        # don't add if not configured
        if username == "":
            _add_your_username_to_access_the_collection = self.addon.getLocalizedString(30104)
            li = xbmcgui.ListItem(label=_add_your_username_to_access_the_collection)
            url = self._build_url({'mode': 'settings'})
            items.append((url, li, True))
        else:
            _collection = self.addon.getLocalizedString(30102)
            li = xbmcgui.ListItem(label=_collection)
            url = self._build_url({'mode': 'list_collection'})
            items.append((url, li, True))
            _wishlist = self.addon.getLocalizedString(30105)
            li = xbmcgui.ListItem(label=_wishlist)
            url = self._build_url({'mode': 'list_wishlist'})
            items.append((url, li, True))
        # search all
        _search = self.addon.getLocalizedString(30103)
        li = xbmcgui.ListItem(label=_search)
        url = self._build_url({'mode': 'search', 'action': 'new'})
        items.append((url, li, True))
        return items

    def get_album_items(self, albums):
        items = []
        for album in albums:
            li = xbmcgui.ListItem(label=album.album_name)
            url = self._build_url({'mode': 'list_songs', 'album_id': album.album_id, 'item_type': album.item_type, 'band_id': album.band_id})
            li.setArt({'thumb': album.get_art_img(), 'fanart': album.get_art_img()})
            album_url = self._build_url({'mode': 'download_album', 'album_id': album.album_id, 'item_type': album.item_type, 'band_id': album.band_id})
            cmd = 'Container.Update({album_url})'.format(album_url=album_url)
            _download_album = self.addon.getLocalizedString(30205)
            commands = [(_download_album, cmd)]
            li.addContextMenuItems(commands)
            items.append((url, li, True))
        return items

    def get_genre_items(self, genres):
        items = []
        new_item = []
        _all = self.addon.getLocalizedString(30201)
        li = xbmcgui.ListItem(label=_all)
        url = self._build_url({'mode': 'list_subgenre_songs', 'category': 'all', 'subcategory': 'all'})
        new_item.append((url, li, True))
        for genre in genres:
            li = xbmcgui.ListItem(label=genre['name'])
            url = self._build_url({'mode': 'list_subgenre', 'category': genre['value']})
            items.append((url, li, True))
        return new_item + sorted(items)

    def get_subgenre_items(self, genre, subgenres):
        items = []
        _all = self.ad.getLocalizedString(30201)
        li = xbmcgui.ListItem(label=_all + " " + genre)
        url = self._build_url({'mode': 'list_subgenre_songs', 'category': genre, 'subcategory': 'all'})
        items.append((url, li, True))
        for subgenre in subgenres[genre]:
            li = xbmcgui.ListItem(label=subgenre['name'])
            url = self._build_url({'mode': 'list_subgenre_songs', 'category': genre, 'subcategory': subgenre['value']})
            items.append((url, li, True))
        return sorted(items)

    def get_track_items(self, band, album, tracks, to_album=False, to_band=False):
        items = []
        for track in tracks:
            commands = []
            if album.artist_name == track.artist_name:
                if not album.artist_name or not track.artist_name:
                    title = u"[COLOR orange]{band}[/COLOR] - {track}".format(band=band.band_name, track=track.track_name)
                else:
                    title = u"{track}".format(track=track.track_name)
            else:
                title = u"[COLOR orange]{band}[/COLOR] - {track}".format(band=track.artist_name, track=track.track_name)
            li = xbmcgui.ListItem(label=title)
            li.setInfo('music', {'duration': int(track.duration), 'album': album.album_name, 'genre': album.genre,
                                 'mediatype': 'song', 'tracknumber': track.number, 'title': track.track_name,
                                 'artist': track.artist_name, 'comment': band.band_about, 'year': album.release_year})
            li.setArt({'thumb': album.get_art_img(), 'fanart': album.get_art_img()})
            li.setProperty('IsPlayable', 'true')
            url = self._build_url({'mode': 'stream', 'url': track.file, 'title': title})
            li.setPath(url)
            track_url = self._build_url({'mode': 'download_song',
                                         'url': track.file,
                                         'title': band.band_name.replace(' - ', ': ') + ' - ' + track.track_name.replace(' - ', ': '),
                                         'album_artist': album.artist_name,
                                         'album_name': album.album_name,
                                         'rel_year': album.release_year,
                                         'genre': album.genre,
                                         'track_number': track.number,
                                         'publisher': album.publisher,
                                         'comment': band.band_about,
                                         'image_file': album.get_art_img()})
            cmd = 'Container.Update({track_url})'.format(track_url=track_url)
            _download_album = self.addon.getLocalizedString(30206)
            commands.append((_download_album, cmd))
            if to_album:
                album_url = self._build_url(
                    {'mode': 'list_songs', 'album_id': album.album_id, 'item_type': album.item_type, 'band_id': band.band_id})
                cmd = 'Container.Update({album_url})'.format(album_url=album_url)
                _go_to_the_album = self.addon.getLocalizedString(30202)
                commands.append((_go_to_the_album, cmd))
            if to_band:
                band_url = self._build_url({'mode': 'list_search_albums', 'band_id': band.band_id})
                cmd = 'Container.Update({band_url})'.format(band_url=band_url)
                _go_to_the_artist = self.addon.getLocalizedString(30203) 
                commands.append((_go_to_the_artist, cmd))
            li.addContextMenuItems(commands)
            items.append((url, li, False))
        return items

    def get_band_items(self, bands, from_wishlist=False, from_search=False):
        items = []
        mode = 'list_albums'
        if from_wishlist:
            mode = 'list_wishlist_albums'
        elif from_search:
            mode = 'list_search_albums'
        for band in bands:
            li = xbmcgui.ListItem(label=band.band_name)
            url = self._build_url({'mode': mode, 'band_id': band.band_id})
            li.setArt({'thumb': band.get_art_img(), 'fanart': band.get_art_img(23)})
            band_url = self._build_url({'mode': 'download_all_albums', 'band_id': band.band_id})
            cmd = 'Container.Update({band_url})'.format(band_url=band_url)
            commands = [(self._download_all_albums, cmd)]
            li.addContextMenuItems(commands)
            items.append((url, li, True))
        return items

    def get_label_items(self, labels, from_search=False):
        items = []
        mode = 'list_albums'
        dialog = xbmcgui.Dialog()
        if from_search:
            mode = 'list_search_albums'
        for label in labels:
            li = xbmcgui.ListItem(label=label.label_name + ' [COLOR red][I](record label)[/I][/COLOR]')
            url = self._build_url({'mode': mode, 'band_id': label.label_id})
            li.setArt({'thumb': label.get_art_img(), 'fanart': label.get_art_img(23)})
            label_url = self._build_url({'mode': 'download_all_albums', 'band_id': label.label_id})
            cmd = 'Container.Update({label_url})'.format(label_url=label_url)
            commands = [(self._download_all_albums, cmd)]
            li.addContextMenuItems(commands)
            items.append((url, li, True))
        return items
