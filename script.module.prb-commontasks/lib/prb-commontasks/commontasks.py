#!/bin/python

import os
import re
import time
import xbmc
import xbmcgui
import xbmcvfs
import base64
import requests.utils
from PIL import Image
import shutil


try:
    # Python3
    import urllib.request
    import urllib.parse
except ImportError:
    # Python2
    import urllib

'''
Written by: Phantom Raspberry Blower
Date: 21-08-2017
Description: Common Tasks for Addons
'''

INVALID_FILENAME_CHARS = u'\/:*?"<>|'

def decode(code):
    return base64.b64decode(code)


def encode(plaintext):
    return base64.b64encode(plaintext)


def requote_uri(text):
    resp = requests.utils.requote_uri(text)
    return resp


def quote_plus(text):
    return urllib.parse.quote_plus(text)


def unquote_plus(text):
    return urllib.parse.unquote_plus(text)


def get_url(url):
    try:
        resp = urllib.urlopen(url)
    except:
        resp = urllib.request.urlopen(url)
    return resp.read()


def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search(u'(?i)' + from_string +
                      u'([\S\s]+?)' +
                      to_string, text).group(1)
    else:
        r = re.search(u'(?i)(' +
                      from_string +
                      u'[\S\s]+?' +
                      to_string +
                      u')', text).group(1)
    return r


def remove_tree(dir_path):
    shutil.rmtree(dir_path, ignore_errors=True)


def xbmc_version():
    return float(xbmc.getInfoLabel("System.BuildVersion")[:4])


def notification(title, message, icon, duration):
    # Display notification to user
    dialog = xbmcgui.Dialog()
    dialog.notification(title,
                        message.encode('ascii', errors='ignore'),
                        icon,
                        duration)


def message(message, title):
    # Display message to user
    dialog = xbmcgui.Dialog()
    dialog.ok(title, message)


def remove_from_list(list, file):
    list = list.replace(u'<>Ungrouped', '').replace(u'All Songs', '')
    index = find_list(list, file)
    if index >= 0:
        content = read_from_file(file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(file, s)
        if u'song' not in file and u'album' not in file:
            pass


def find_list(query, search_file):
    try:
        content = read_from_file(search_file)
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1


def add_to_list(list, file, refresh):
    if find_list(list, file) >= 0:
        return
    if os.path.isfile(file):
        content = read_from_file(file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % list
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(file, s)

    if refresh:
        xbmc.executebuiltin("Container.Refresh")


def read_from_file(path):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        return None


def write_to_file(path, content, append=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        return False


def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path


def remove_old_temp_files(file_path, days=28):
    '''
    Remove temp files from directory that are older
    than the specified number of days
    '''
    SECONDS_PER_HOUR = 3600
    current_time = time.time()
    for f in os.listdir(file_path):
        creation_time = os.path.getctime(file_path + '/' + f)
        if ((current_time - creation_time) // (24 * SECONDS_PER_HOUR)) >= int(days):
            os.unlink(file_path + '/' + f)


def resize_image(image_file, width, height):
    # Resize images
    size = height, width
    img = Image.open(image_file)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(image_file)


def validate_filename(filename):
    # Remove invalid characters from file name
    valid_filename = dict((ord(char), None) for char in INVALID_FILENAME_CHARS)
    file_name = filename.decode('ascii', errors='ignore')
    return file_name.translate(valid_filename)


def getLibrarySources(db_type):
    # Returns the paths of library sources both music and videos
    json_request = u'{ "jsonrpc" : "2.0", "method": "Files.GetSources", "id": 1, "params" : '+\
    '{"media":  "' + db_type + u'"}}'
    response = xbmc.executeJSONRPC(json_request)
    response = eval(response)
    return [source['file'] for source in response['result']['sources']]


def install_addon(addon, stealth=False):
    # Install addon if not already there
    addon_path = os.path.join(xbmcvfs.translatePath('special://home/addons'), addon)
    if not os.path.exists(addon_path) == True:
        xbmc.executebuiltin('InstallAddon(%s)' % (addon))
        if stealth == True:
            xbmc.executebuiltin('SendClick(11)')
            __addon__.openSettings()
        return True
    else:
        return False
