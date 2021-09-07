#!/bin/python
import re
import urllib.request, urllib.parse

# Written by: Phantom Raspberry Blower
# Date: 21-02-2018
# Description: Module for downloading information about ip address

URL = 'https://ipinfo.io/'
API_KEY = 'AIzaSyDIJ9XX2ZvRKCJcFRrl-lRanEtFUow4piM'
IMG_SIZE = '480x390'

class IPInfo:

    def __init__(self, ipaddr='0.0.0.0'):
        self.clear()
        if ipaddr == '0.0.0.0':
            ipaddr = self._wan_ip_addr()
        if ipaddr is not 'Error getting WAN IP Address!':
            self.__ip_addr = ipaddr
            self.get_ip_info(ipaddr)

    @property
    def ip_addr(self):
        return self.__ip_addr

    @property
    def city(self):
        return self.__city

    @property
    def region(self):
        return self.__region

    @property
    def postcode(self):
        return self.__postcode

    @property
    def coordinates(self):
        return self.__coordinates

    @property
    def country(self):
        return self.__country

    @property
    def hostname(self):
        return self.__hostname

    @property
    def addrtype(self):
        return self.__addr_type

    @property
    def asn(self):
        return self.__asn

    @property
    def organization(self):
        return self.__organization

    @property
    def route(self):
        return self.__route

    @property
    def description(self):
        return self.__description

    @property
    def mapimage(self):
        return self.__map_image

    def clear(self):
        self.__ip_addr = '0.0.0.0'
        self.__city = None
        self.__region = None
        self.__postcode = None
        self.__coordinates = None
        self.__country = None
        self.__hostname = None
        self.__addr_type = None
        self.__asn = None
        self.__organization = None
        self.__route = None
        self.__description = None
        self.__map_image = None

    def _regex_from_to(self, text, from_string, to_string, excluding=True):
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


    def _get_url(self, url):
        """
        Download url and remove carriage return
        and tab spaces from page
        """
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        try:
            print(url)
            req = urllib.request.Request(url, headers=hdr)
            resp = urllib.request.urlopen(req)
            return resp.read().decode('utf-8')
        except:
            return 'Error getting URL!'


    def _wan_ip_addr(self):
    # Get the WAN IP address
        try:
            resp = self._get_url('http://ip.42.pl/raw')
            print(resp)
            return resp
        except:
            return 'Error getting WAN IP Address!'


    def _ip_info(self, ipaddr=None):
        text = ''
        """
        Show Location
        """
        try:
            response = self._get_url(URL + ipaddr)
#            address = response.replace('\t', '').replace('\n', '').replace('  ', '')
#            matchrows = re.compile('<dl class="row">(.+?)</dl>').findall(address)
#            for item in matchrows:
#                matchitems = re.compile('<dt class="col-sm-4 mb-md-3">(.+?)</dt>'
#                                        '<dd class="col-sm-8 mb-md-9">(.+?)</dd>').findall(item)
#                for key, value in matchitems:
#                    if '<a' in value:
#                        value = self._regex_from_to(value, '">', '</a>')
#                    text += ('%s: %s\n') % (key, value)
            self.__ip_addr = ipaddr
            lat = self._regex_from_to(response, '"latitude": "', '",')
            lon = self._regex_from_to(response, '"longitude": "', '"')
            self.__coordinates = '%s, %s' % (lat, lon)
#            self.__coordinates = self._regex_from_to(response, 'Coordinates: ', '\n')
            self.__country = self._regex_from_to(response, '"addressCountry": "', '"')
            try:
                self.__postcode = self._regex_from_to(response, '"PostalCode": "', '"')
            except:
                self.__postcode =  ''
#            self.__country = self._regex_from_to(text, 'Country: ', '\n')
            self.__region = self._regex_from_to(response, '"streetAddress": "', '"')
            try:
                self.__hostname = self._regex_from_to(text, 'Hostname: ', '\n')
            except:
                self.__hostname = ''
            self.__asn = self._regex_from_to(text, 'ASN: ', '\n')
            try:
                self.__organization = self._regex_from_to(text, 'Organization: ', '\n')
            except:
                self.__organization = ''
            self.__route = self._regex_from_to(text, 'Route: ', '\n')
            self.__addr_type = self._regex_from_to(text, 'Address type: ', '\n')
            lat_lon = self.__coordinates
            self.__map_image = 'https://maps.googleapis.com/maps/api/staticmap' \
                               '?center=%s&zoom=11&&size=%s&key=%s' % (lat_lon,
                                                                       IMG_SIZE,
                                                                       API_KEY)
            self.__city = self._regex_from_to(text, 'City: ', '\n')
            try:
                url = 'https://en.wikipedia.org/w/api.php?action=query&prop=' \
                      'extracts&titles=%s&exintro=&exsentences=2&explaintext=' \
                      '&redirects=&formatversion=2&format=json' % self.__city
                response = self._get_url(url)
                self.__description = self._regex_from_to(response, ',"extract":"', '"}]}')
            except: pass
            return {'ip_addr': self.__ip_addr,
                    'city': self.__city,
                    'region': self.__region,
                    'postcode': self.__postcode,
                    'coordinates': self.__coordinates,
                    'country': self.__country,
                    'hostname': self.__hostname,
                    'addr_type': self.__addr_type,
                    'asn': self.__asn,
                    'organization': self.__organization,
                    'route': self.__route,
                    'description': self.__description,
                    'map_image': self.__map_image}
        except:
            return 'Error getting IP address info!'


    def get_ip_info(self, ipaddr):
        """
        Return artist information as dictionary. If no result try either
        removing or prefixing the 'the' word.
        """
        self.clear()
        ipi = self._ip_info(ipaddr)
        return ipi
