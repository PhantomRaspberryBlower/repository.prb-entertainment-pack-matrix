import xbmcgui
import xbmcvfs
import xbmc
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import mutagen
from PIL import Image

from ..bandcamp_api import bandcamp

class Downloads:

    def __init__(self, addon):
        self.addon = addon
        self.music_dir = addon.getSetting('music_dir')
        self._download_complete = addon.getLocalizedString(30211)
        self._downloading = addon.getLocalizedString(30213)
        self._downloaded = addon.getLocalizedString(30214)
        self._n_of_n_tracks_downloaded = addon.getLocalizedString(30212)

    def download_all_albums(self, band_id=1):
        _n_of_n_albums_downloaded = self.addon.getLocalizedString(30215)
        _discography = self.addon.getLocalizedString(30216)
        band, albums = bandcamp.Bandcamp(None).get_band(band_id=band_id)
        dialog = xbmcgui.Dialog()
        pDialog = xbmcgui.DialogProgressBG()
        num_albums = len(albums)
        number = 1

        pDialog.create("%s: %s" % (band.band_name, _discography), self._downloading)
        percentage = 0

        try:
            for album in albums:
                text = _n_of_n_albums_downloaded % (int(number), int(num_albums))
                percentage = (float(number)/float(num_albums)) * 100
                pDialog.update(int(percentage), '%s: %s' % (band.band_name, _discography),
                               text.replace(self._downloading, self._downloaded))
                self.download_album(album.album_id, album.item_type, band.band_id, update_library=False)
                number += 1
            pDialog.close()
            dialog.notification("%s: %s" % (band.band_name, _discography),
                                self._download_complete,
                                band.get_art_img(),
                                3000)
            # Verify Library source exists
            for item in self.getLibrarySources('music'):
                # Verify download location is included in Library
                if item == self.music_dir:
                    filepath = self.validate_filepathname(self.music_dir + '%s' % band.band_name.rstrip('.'))
                    xbmc.executebuiltin('UpdateLibrary(music, %s)' % str(filepath))
        except Exception as e:
            pDialog.close()
            xbmc.log("ERROR %s in download_all_albums" % str(e), level=xbmc.LOGWARNING)

    def download_album(self, album_id, item_type, band_id=1, update_library=False):
        genres_lst = xbmcvfs.translatePath('special://home/addons/plugin.audio.bandcamp/resources/music_genres.lst')
        band, album, tracks = bandcamp.Bandcamp(None).get_album(album_id=album_id,
                                                                item_type=item_type,
                                                                band_id=band_id,
                                                                genres_lst=genres_lst)
        dialog = xbmcgui.Dialog()
        pDialog = xbmcgui.DialogProgressBG()
        num_dl_tracks = album.num_downloadable_tracks
        if update_library:
            pDialog.create('%s: %s' % (band.band_name, album.album_name), self._downloading)
            percentage = 0

        try:
            filepath = self.validate_filepathname(self.music_dir + "%s" % band.band_name.rstrip('.'))
            xbmcvfs.mkdir(filepath)
        except:
            pass
        try:
            filepath = self.validate_filepathname(self.music_dir + "%s/%s" % (band.band_name.rstrip('.'),
                                                                              album.album_name.replace(' / ', ' - ').rstrip('.')))
            xbmcvfs.mkdir(filepath)
            imagefile = album.get_art_img()
            response_img = requests.get(imagefile)
            open(filepath + '/Folder.jpg', 'wb').write(response_img.content)
            self.resize_image(filepath + '/Folder.jpg', 256, 256)

            for track in tracks:
                file = track.file
                name = track.track_name
                number = track.number
                if number is None:
                    number = 1
                response = requests.get(file)
                # Need to add images of artist
                filename = filepath + "/"+ self.validate_filename('%d. %s.mp3' % (number, name))
                text = self._n_of_n_tracks_downloaded % (number, num_dl_tracks)
                if update_library:
                    percentage = (float(number)/float(num_dl_tracks)) * 100
                    pDialog.update(int(percentage),
                                   '%s: %s' % (band.band_name, album.album_name),
                                   text.replace(self._downloading,
                                                self._downloaded))
                open(filename, "wb").write(response.content)

                self.ID3_tags(filepath, filename, name, track.artist_name, album.album_name, album.artist_name,
                              album.release_year, album.genre, str(number), band.band_about, album.publisher)
            if update_library:
                pDialog.close()
                dialog.notification("%s: %s" % (band.band_name, album.album_name),
                                    self._download_complete,
                                    filepath + '/Folder.jpg',
                                    3000)
                # Verify Library source exists
                for item in self.getLibrarySources('music'):
                    # Verify download location is included in Library
                    if item == self.music_dir:
                        xbmc.executebuiltin('UpdateLibrary(music, %s)' % str(filepath))
        except Exception as e:
            if update_library:
                pDialog.close()
            xbmc.log("ERROR %s in download_album" % str(e), level=xbmc.LOGWARNING)

    def download_song(self, track_file, title, album_artist, album_name, rel_year, genre,
                      track_number, publisher=None, comment=None, image_file=None):
        artist, song = title.split(' - ')
        dialog = xbmcgui.Dialog()
        pDialog = xbmcgui.DialogProgressBG()
        num_dl_tracks = 1
        pDialog.create('%s: %s' % (artist, song), self._downloading)
        percentage = 0
        try:
            filepath = self.validate_filepathname(self.music_dir + "%s" % artist.rstrip('.'))
            xbmcvfs.mkdir(filepath)
        except:
            pass
        try:
            filepath = self.validate_filepathname(self.music_dir + "%s/%s" % (artist.rstrip('.'),
                                                                         album_name.rstrip('.')))
            xbmcvfs.mkdir(filepath)
            response_img = requests.get(image_file)
            open(filepath + '/Folder.jpg', 'wb').write(response_img.content)
            self.resize_image(filepath + '/Folder.jpg', 256, 256)
            number = 1
            if track_number:
                number = int(track_number)
            response = requests.get(track_file)
            # Need to add images of artist
            filename = filepath + "/"+ self.validate_filename('%d. %s.mp3' % (number, song))
            text = self._n_of_n_tracks_downloaded % (number, num_dl_tracks)
            percentage = (float(number)/float(num_dl_tracks)) * 100
            pDialog.update(int(percentage), '%s: %s' % (artist, song), text.replace(self._downloading,
                                                                                    self._downloaded))
            open(filename, "wb").write(response.content)
            self.ID3_tags(filepath, filename, song, artist, album_name, album_artist, rel_year, genre, str(number), comment, publisher)
            pDialog.close()
            dialog.notification("%s: %s" % (artist, song),
                                self._download_complete,
                                filepath + '/Folder.jpg',
                                3000)
            # Verify Library source exists
            for item in self.getLibrarySources('music'):
                # Verify download location is included in Library
                if item == self.music_dir:
                    xbmc.executebuiltin('UpdateLibrary(music, %s)' % str(filepath))
        except Exception as e:
            if update_library:
                pDialog.close()
            xbmc.log("ERROR %s in download_song" % str(e), level=xbmc.LOGWARNING)

    def ID3_tags(self, filepath, filename, title, artist, album, albumartist, date, genre,
                 tracknumber, comment=None, organization=None):
        EasyID3.RegisterTextKey('comment', 'COMM')
        if xbmcvfs.exists(filename):
            try:
                tag = EasyID3(filename)
            except:
                tag = mutagen.File(filename, easy=True)
                tag.add_tags()
            tag["title"] = title
            tag["artist"] = artist
            tag["album"] = album
            tag["albumartist"] = albumartist # band.band_name #tralbum_artist
            tag["date"] = date
            tag["genre"] = genre
            tag["tracknumber"] = tracknumber
            if comment:
                tag['comment'] = comment
            #tags[u"USLT::'eng'"] = (USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics)) # Used for adding Lyrics
            if organization:
                tag["organization"] = organization
            else:
                tag["organization"] = artist
            tag.save(v2_version=3)
            try:
                tag = ID3(filename)
                tag.delall("APIC")
                with open(filepath + '/Folder.jpg', 'rb') as albumart:
                    tag['APIC'] = APIC(encoding=3,
                                       mime='image/jpeg',
                                       type=3, desc=u'Cover',
                                       data=albumart.read())
                tag.save()
            except:
                pass

    def resize_image(self, image_file, width, height):
        # Resize images
        size = height, width
        img = Image.open(image_file)
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(image_file)

    def validate_filename(self, filename):
        INVALID_FILENAME_CHARS = u'\/:*?"<>|'
        # Remove invalid characters from file name
        valid_filename = dict((ord(char), None) for char in INVALID_FILENAME_CHARS)
        return filename.translate(valid_filename)

    def validate_filepathname(self, filepathname):
        INVALID_FILEPATH_CHARS = u':*?"<>|'
        # Remove invalid characters from file name
        valid_filepathname = dict((ord(char), None) for char in INVALID_FILEPATH_CHARS)
        return filepathname.translate(valid_filepathname)

    def getLibrarySources(self, db_type):
        # Returns the paths of library sources both music and videos
        json_request = '{ "jsonrpc" : "2.0", "method": "Files.GetSources", "id": 1, "params" : '+\
        '{"media":  "' + db_type + '"}}'
        response = xbmc.executeJSONRPC(json_request)
        response = eval(response)
        return [source['file'] for source in response['result']['sources']]

