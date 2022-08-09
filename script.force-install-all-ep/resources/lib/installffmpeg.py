#!/bin/python

from subprocess import check_call, Popen, PIPE
import os
import errno

# Written by: Phantom Raspberry Blower (The PRB)
# Date: 01-10-2018
# Description: Script for installing FFmpeg

class InstallFFmpeg():

    @property
    def is_user_root(self):
        # Is current user root
        if os.geteuid() == 0:
            return True
        else:
            return False


    def get_ffmpeg(self):
        version = ''
        if self.is_tool_installed('ffmpeg') is False:
            if self.is_user_root:
                self.install_tool('ffmpeg')
        command = 'ffmpeg -version'
        output = Popen(command.split(), stdout=PIPE).communicate()[0]
        results = str(output)
        if 'Copyright' in results:
            version = results[results.index('ffmpeg ')+7:results.index(' Copyright')]
        return version


    # Check tool is installed
    def is_tool_installed(self, name):
        try:
            devnull = open(os.devnull)
            Popen([name],
                  stdout=devnull,
                  stderr=devnull).communicate()
        except OSError as e:
            if e.errno == errno.ENOENT:
                return False
        return True


    # Install FFmpeg
    def install_tool(self, name):
        # Install tool and suppress output
        devnull = open(os.devnull, 'w')
        check_call(["sudo",
                    "apt-get",
                    "install",
                    "-y",
                    "-qq",
                    name], stdout=devnull, stderr=devnull)


# Check if running stand-alone or imported
if __name__ == u'__main__':
    if platform.system() != u'Windows':
        import installffmpeg
        si = InstallFFmpeg()
        info = si.get_ffmpeg()
        print(info)
    else:
        print(u'This script does not work with a Windows operating system. :( - Yet!')
