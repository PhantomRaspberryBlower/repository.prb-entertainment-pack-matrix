#!/bin/python

from subprocess import check_call, Popen, PIPE
import os

# Written by: Phantom Raspberry Blower (The PRB)
# Date: 01-10-2018
# Description: Script for installing FFmpeg

def install_ffmpeg():
    results = []
    if is_tool_installed('ffmpeg') is False:
        if is_user_root:
            install_tool('ffmpeg')
        else:
            return results
    command = 'ffmpeg -version'
    output = Popen(command.split(), stdout=PIPE).communicate()[0]
    for line in output.split('\n'):
        for item in desc:
            if line[0:len(item)] == item:
                results.append(line[len(item):].strip())
    return results

# Check tool is installed
def is_tool_installed(name):
    try:
        devnull = open(os.devnull)
        Popen([name],
              stdout=devnull,
              stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True

# Install FFmpeg
def install_tool(name):
    # Install tool and suppress output
    devnull = open(os.devnull, 'w')
    check_call(["sudo",
                "apt-get",
                "install",
                "-y",
                "-qq",
                name], stdout=devnull, stderr=devnull)
