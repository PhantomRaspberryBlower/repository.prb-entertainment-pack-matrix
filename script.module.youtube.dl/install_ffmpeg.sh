#!/bin/bash
# Script for installing FFmpeg onto a Raspberry Pi
# Need to make it executable and run as root ie.
# sudo chmod +x install_ffmpeg.sh
# followed by
# sudo bash install_ffmpeg.sh
# Written by: Phantom Raspberry Blower
# Date August 2021

if [ "$EUID" -ne 0 ]
  then echo "Needs to be run as root! Type in: sudo bash install_ffmpeg.sh"
  exit
fi
WORK_DIR=/home/osmc
echo "-----------------------------------"
echo "       Installing OS updates"
echo "-----------------------------------"
apt-get -y update
echo "-----------------------------------"
echo "     Upgrading OS installation"
echo "-----------------------------------"
apt-get -y upgrade
echo "-----------------------------------"
echo "         Installing FFmpeg"
echo "-----------------------------------"
# Encodes audio & videos files
apt-get -y install ffmpeg
echo "-----------------------------------"
echo "       Cleanup installation"
echo "-----------------------------------"
apt -y autoremove
echo "==================================="
echo "           Completed :)"
echo "==================================="
echo ""
