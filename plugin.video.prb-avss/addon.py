#!/bin/python
import xbmc

if __name__ == '__main__':
    xbmc.executebuiltin('PlayMedia("udp://224.0.0.1:4569")', True)
