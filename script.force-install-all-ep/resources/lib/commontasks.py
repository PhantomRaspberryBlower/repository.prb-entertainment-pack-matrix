import os
import xbmc
import xbmcgui
import xbmcvfs
import shutil
import re

'''
Written by: Phantom Raspberry Blower
Date: 21-08-2017
Description: Common Tasks for Addons
'''

INVALID_FILENAME_CHARS = '\/:*?"<>|'


def remove_tree(dir_path):
    shutil.rmtree(dir_path, ignore_errors=True)


def xbmc_version():
    return float(xbmc.getInfoLabel("System.BuildVersion")[:4])


def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" +
                        title + "," +
                        message + "," +
                        ms + "," + nart + ")")


def message(message, title):
    # Display message to user
    dialog = xbmcgui.Dialog()
    dialog.ok(title, message)


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


def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string +
                      "([\S\s]+?)" +
                      to_string, text).group(1)
    else:
        r = re.search("(?i)(" +
                      from_string +
                      "[\S\s]+?" +
                      to_string +
                      ")", text).group(1)
    return r

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
