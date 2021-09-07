import xbmcgui
import xbmcplugin
import xbmcaddon
import sys
import urllib.request, urllib.parse, urllib.error
import datetime
import re

# Written by:   Phantom Raspberry Blower
# Date:     21-02-2017
# Description:  Addon for listening to BBC Radio live broadcasts

# Get addon details
__addon_id__ = 'plugin.audio.bbc-radio'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
__fanart__ = __addon__.getAddonInfo('fanart')
__author__ = "Phantom Raspberry Blower"
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])

# Get localized language words
__language__ = __addon__.getLocalizedString
_national_radio = __language__(30001)
_nations_and_regions = __language__(30002)
_local_radio = __language__(30003)
_nationwide_radio_stations = __language__(30004)
_national_and_regional_radio_stations = __language__(30005)
_local_radio_stations = __language__(30006)
_bbc_radio_1_desc = __language__(30007)
_bbc_radio_1_extra_desc = __language__(30008)
_bbc_radio_2_desc = __language__(30009)
_bbc_radio_3_desc = __language__(30010)
_bbc_radio_4_desc = __language__(30011)
_bbc_radio_4_extra_desc = __language__(30012)
_bbc_radio_5_live_desc = __language__(30013)
_bbc_radio_5_live_extra_desc = __language__(30014)
_bbc_radio_6_music_desc = __language__(30015)
_bbc_asian_network_desc = __language__(30016)
_bbc_radio_cymru_desc = __language__(30017)
_bbc_radio_foyle_desc = __language__(30018)
_bbc_radio_nan_gaidheal_desc = __language__(30019)
_bbc_radio_scotland_desc = __language__(30020)
_bbc_radio_ulster_desc = __language__(30021)
_bbc_radio_wales_desc = __language__(30022)
_internet_radio = __language__(30023)


_something_wicked_happened = __language__(30721)
_error = __language__(30722)

image_path = 'special://home/addons/' + __addon_id__ + '/resources/media/'

category_list = [_national_radio,
                 _nations_and_regions,
                 _local_radio]

station_list_nr = ['BBC Radio 1',
                   'BBC Radio 1xtra',
                   'BBC Radio 2',
                   'BBC Radio 3',
                   'BBC Radio 4',
                   'BBC Radio 4 Extra',
                   'BBC Radio 5 Live',
                   'BBC Radio 5 Live Sports Extra',
                   'BBC Radio 6 Music',
                   'BBC Asian Network',
                   'BBC World Service']

station_list_nar = ['Radio Cymru',
                    'BBC Radio Foyle',
                    'BBC Radio nan Gaidheal',
                    'BBC Radio Scotland',
                    'BBC Radio Ulster',
                    'BBC Radio Wales']

station_list_lr = ['BBC Radio Berkshire',
                   'BBC Radio Bristol',
                   'BBC Radio Cambridgeshire',
                   'BBC Radio Cornwall',
                   'BBC Coventry & Warwickshire',
                   'BBC Radio Cumbria',
                   'BBC Radio Derby',
                   'BBC Radio Devon',
                   'BBC Essex',
                   'BBC Radio Gloucestershire',
                   'BBC Radio Guernsey',
                   'BBC Hereford & Worcester',
                   'BBC Radio Humberside',
                   'BBC Radio Jersey',
                   'BBC Radio Kent',
                   'BBC Radio Lancashire',
                   'BBC Radio Leeds',
                   'BBC Radio Leicester',
                   'BBC Radio Lincolnshire',
                   'BBC Radio London',
                   'BBC Radio Manchester',
                   'BBC Radio Merseyside',
                   'BBC Newcastle',
                   'BBC Radio Norfolk',
                   'BBC Radio Northampton',
                   'BBC Radio Nottingham',
                   'BBC Radio Oxford',
                   'BBC Radio Sheffield',
                   'BBC Radio Shropshire',
                   'BBC Radio Solent',
                   'BBC Somerset',
                   'BBC Radio Stoke',
                   'BBC Radio Suffolk',
                   'BBC Surrey',
                   'BBC Sussex',
                   'BBC Tees',
                   'BBC Three Counties Radio',
                   'BBC Wiltshire',
                   'BBC WM 95.6',
                   'BBC Radio York']

categories = {_national_radio: {'thumb': image_path + 'bbc-national-radio-logo.png',
                                 'fanart': image_path + 'bbc-national-radio.jpg',
                                 'desc': _nationwide_radio_stations
                                 },
              _nations_and_regions: {'thumb': image_path + 'bbc-nations-radio-logo.png',
                                      'fanart': image_path + 'bbc-nations-radio.jpg',
                                      'desc': _national_and_regional_radio_stations
                                      },
              _local_radio: {'thumb': image_path + 'bbc-local-radio-logo.png',
                              'fanart': image_path + 'bbc-local-radio.jpg',
                              'desc': _local_radio_stations}
              }

base_url = 'http://as-hls-ww-live.akamaized.net/pool_904/live/'

stations = {'BBC Radio 1': {'url': base_url + 'ww/bbc_radio_one/bbc_radio_one.isml/bbc_radio_one-audio%3d48000.norewind.m3u8',
                            'thumb': image_path + 'bbc-radio-1-logo.png',
                            'fanart': image_path + 'bbc-radio-1.jpg',
                            'desc': _bbc_radio_1_desc},
            'BBC Radio 1xtra': {'url': base_url + 'ww/bbc_1xtra/bbc_1xtra.isml/bbc_1xtra-audio%3d48000.norewind.m3u8',
                                  'thumb': image_path + 'bbc-radio-1xtra-logo.png',
                                  'fanart': image_path + 'bbc-radio-1xtra.jpg',
                                  'desc': _bbc_radio_1_extra_desc},
            'BBC Radio 2': {'url': base_url + 'ww/bbc_radio_two/bbc_radio_two.isml/bbc_radio_two-audio%3d48000.norewind.m3u8',
                            'thumb': image_path + 'bbc-radio-2-logo.png',
                            'fanart': image_path + 'bbc-radio-2.jpg',
                            'desc': _bbc_radio_2_desc},
            'BBC Radio 3': {'url': base_url + 'ww/bbc_radio_three/bbc_radio_three.isml/bbc_radio_three-audio%3d48000.norewind.m3u8',
                            'thumb': image_path + 'bbc-radio-3-logo.png',
                            'fanart': image_path + 'bbc-radio-3.jpg',
                            'desc': _bbc_radio_3_desc},
            'BBC Radio 4': {'url': base_url + 'ww/bbc_radio_fourfm/bbc_radio_fourfm.isml/bbc_radio_fourfm-audio%3d48000.norewind.m3u8',
                            'thumb': image_path + 'bbc-radio-4-logo.png',
                            'fanart': image_path + 'bbc-radio-4.jpg',
                            'desc': _bbc_radio_4_desc},
            'BBC Radio 4 Extra': {'url': base_url + 'ww/bbc_radio_four_extra/bbc_radio_four_extra.isml/bbc_radio_four_extra-audio%3d48000.norewind.m3u8',
                                  'thumb': image_path + 'bbc-radio-4-extra-logo.png',
                                  'fanart': image_path + 'bbc-radio-4-extra.jpg',
                                  'desc': _bbc_radio_4_extra_desc},
            'BBC Radio 5 Live': {'url': base_url + 'ww/bbc_radio_five_live/bbc_radio_five_live.isml/bbc_radio_five_live-audio%3d48000.norewind.m3u8',
                                 'thumb': image_path + 'bbc-radio-5-live-logo.png',
                                 'fanart': image_path + 'bbc-radio-5-live.jpg',
                                 'desc': _bbc_radio_5_live_desc},
            'BBC Radio 5 Live Sports Extra': {'url': base_url + '/uk/bbc_radio_five_live_sports_extra/bbc_radio_five_live_sports_extra.isml/bbc_radio_five_live_sports_extra-audio%3d48000.norewind.m3u8',
                                              'thumb': image_path + 'bbc-radio-5-live-sports-extra-logo.png',
                                              'fanart': image_path + 'bbc-radio-5-live-sports-extra.jpg',
                                              'desc': _bbc_radio_5_live_extra_desc},
            'BBC Radio 6 Music': {'url': base_url + 'ww/bbc_6music/bbc_6music.isml/bbc_6music-audio%3d48000.norewind.m3u8',
                                  'thumb': image_path + 'bbc-radio-6-music-logo.png',
                                  'fanart': image_path + 'bbc-radio-6-music.jpg',
                                  'desc': _bbc_radio_6_music_desc},
            'BBC Asian Network': {'url': base_url + 'ww/bbc_asian_network/bbc_asian_network.isml/bbc_asian_network-audio%3d48000.norewind.m3u8',
                                  'thumb': image_path + 'bbc-asian-network-logo.png',
                                  'fanart': image_path + 'bbc-asian-network.jpg',
                                  'desc': _bbc_asian_network_desc},
            'BBC World Service': {'url': base_url + 'ww/bbc_world_service/bbc_world_service.isml/bbc_world_service-audio%3d48000.norewind.m3u8',
                                  'thumb': image_path + 'bbc-world-service-logo.png',
                                  'fanart': image_path + 'bbc-world-service.jpg',
                                  'desc': ''},
            'Radio Cymru': {'url': base_url + 'ww/bbc_radio_cymru/bbc_radio_cymru.isml/bbc_radio_cymru-audio%3d48000.norewind.m3u8',
                            'thumb': image_path + 'radio-cymru-logo.png',
                            'fanart': image_path + 'radio-cymru.jpg',
                            'desc': _bbc_radio_cymru_desc},
            'BBC Radio Foyle': {'url': base_url + 'ww/bbc_radio_foyle/bbc_radio_foyle.isml/bbc_radio_foyle-audio%3d48000.norewind.m3u8',
                                'thumb': image_path + 'bbc-radio-foyle-logo.png',
                                'fanart': image_path + 'bbc-radio-foyle.jpg',
                                'desc': _bbc_radio_foyle_desc},
            'BBC Radio nan Gaidheal': {'url': base_url + 'ww/bbc_radio_nan_gaidheal/bbc_radio_nan_gaidheal.isml/bbc_radio_nan_gaidheal-audio%3d48000.norewind.m3u8',
                                       'thumb': image_path + 'bbc-radio-nan-gaidheal-logo.png',
                                       'fanart': image_path + 'bbc-radio-nan-gaidheal.jpg',
                                       'desc': _bbc_radio_nan_gaidheal_desc},
            'BBC Radio Scotland': {'url': base_url + 'ww/bbc_radio_scotland_fm/bbc_radio_scotland_fm.isml/bbc_radio_scotland_fm-audio%3d48000.norewind.m3u8',
                                   'thumb': image_path + 'bbc-radio-scotland-logo.png',
                                   'fanart': image_path + 'bbc-radio-scotland.jpg',
                                   'desc': _bbc_radio_scotland_desc},
            'BBC Radio Ulster': {'url': base_url + 'ww/bbc_radio_ulster/bbc_radio_ulster.isml/bbc_radio_ulster-audio%3d48000.norewind.m3u8',
                                 'thumb': image_path + 'bbc-radio-ulster-logo.png',
                                 'fanart': image_path + 'bbc-radio-ulster.jpg',
                                 'desc': _bbc_radio_ulster_desc},
            'BBC Radio Wales': {'url': base_url + 'ww/bbc_radio_wales_fm/bbc_radio_wales_fm.isml/bbc_radio_wales_fm-audio%3d48000.norewind.m3u8',
                                'thumb': image_path + 'bbc-radio-wales-logo.png',
                                'fanart': image_path + 'bbc-radio-wales.jpg',
                                'desc': _bbc_radio_wales_desc},
            'BBC Radio Berkshire': {'url': base_url + 'ww/bbc_radio_berkshire/bbc_radio_berkshire.isml/bbc_radio_berkshire-audio%3d48000.norewind.m3u8',
                                    'thumb': image_path + 'bbc-radio-berkshire-logo.png',
                                    'fanart': image_path + 'bbc-radio-berkshire.jpg',
                                    'desc': ''},
            'BBC Radio Bristol': {'url': base_url + 'ww/bbc_radio_bristol/bbc_radio_bristol.isml/bbc_radio_bristol-audio%3d48000.norewind.m3u8',
                                  'thumb': image_path + 'bbc-radio-bristol-logo.png',
                                  'fanart': image_path + 'bbc-radio-bristol.jpg',
                                  'desc': ''},
            'BBC Radio Cambridgeshire': {'url': base_url + 'ww/bbc_radio_cambridge/bbc_radio_cambridge.isml/bbc_radio_cambridge-audio%3d48000.norewind.m3u8',
                                         'thumb': image_path + 'bbc-radio-cambridgeshire-logo.png',
                                         'fanart': image_path + 'bbc-radio-cambridgeshire.jpg',
                                         'desc': ''},
            'BBC Radio Cornwall': {'url': base_url + 'ww/bbc_radio_cornwall/bbc_radio_cornwall.isml/bbc_radio_cornwall-audio%3d48000.norewind.m3u8',
                                   'thumb': image_path + 'bbc-radio-cornwall-logo.png',
                                   'fanart': image_path + 'bbc-radio-cornwall.jpg',
                                   'desc': ''},
            'BBC Coventry & Warwickshire': {'url': base_url + 'ww/bbc_radio_coventry_warwickshire/bbc_radio_coventry_warwickshire.isml/bbc_radio_coventry_warwickshire-audio%3d48000.norewind.m3u8',
                                            'thumb': image_path + 'bbc-coventry-warwickshire-logo.png',
                                            'fanart': image_path + 'bbc-coventry-warwickshire.jpg',
                                            'desc': ''},
            'BBC Radio Cumbria': {'url': base_url + 'ww/bbc_radio_cumbria/bbc_radio_cumbria.isml/bbc_radio_cumbria-audio%3d48000.norewind.m3u8',
                                  'thumb': image_path + 'bbc-radio-cumbria-logo.png',
                                  'fanart': image_path + 'bbc-radio-cumbria.jpg',
                                  'desc': ''},
            'BBC Radio Derby': {'url': base_url + 'ww/bbc_radio_derby/bbc_radio_derby.isml/bbc_radio_derby-audio%3d48000.norewind.m3u8',
                                'thumb': image_path + 'bbc-radio-derby-logo.png',
                                'fanart': image_path + 'bbc-radio-derby.jpg',
                                'desc': ''},
            'BBC Radio Devon': {'url': base_url + 'ww/bbc_radio_devon/bbc_radio_devon.isml/bbc_radio_devon-audio%3d48000.norewind.m3u8',
                                'thumb': image_path + 'bbc-radio-devon-logo.png',
                                'fanart': image_path + 'bbc-radio-devon.jpg',
                                'desc': ''},
            'BBC Essex': {'url': base_url + 'ww/bbc_radio_essex/bbc_radio_essex.isml/bbc_radio_essex-audio%3d48000.norewind.m3u8',
                          'thumb': image_path + 'bbc-essex-logo.png',
                          'fanart': image_path + 'bbc-essex.jpg',
                          'desc': ''},
            'BBC Radio Gloucestershire': {'url': base_url + 'ww/bbc_radio_gloucestershire/bbc_radio_gloucestershire.isml/bbc_radio_gloucestershire-audio%3d48000.norewind.m3u8',
                                          'thumb': image_path + 'bbc-radio-gloucestershire-logo.png',
                                          'fanart': image_path + 'bbc-radio-gloucestershire.jpg',
                                          'desc': ''},
            'BBC Radio Guernsey': {'url': base_url + 'ww/bbc_radio_guernsey/bbc_radio_guernsey.isml/bbc_radio_guernsey-audio%3d48000.norewind.m3u8',
                                   'thumb': image_path + 'bbc-radio-guernsey-logo.png',
                                   'fanart': image_path + 'bbc-radio-guernsey.jpg',
                                   'desc': ''},
            'BBC Hereford & Worcester': {'url': base_url + 'ww/bbc_radio_hereford_worcester/bbc_radio_hereford_worcester.isml/bbc_radio_hereford_worcester-audio%3d48000.norewind.m3u8',
                                         'thumb': image_path + 'bbc-hereford-worcester-logo.png',
                                         'fanart': image_path + 'bbc-hereford-worcester.jpg',
                                         'desc': ''},
            'BBC Radio Humberside': {'url': base_url + 'ww/bbc_radio_humberside/bbc_radio_humberside.isml/bbc_radio_humberside-audio%3d48000.norewind.m3u8',
                                     'thumb': image_path + 'bbc-radio-humberside-logo.png',
                                     'fanart': image_path + 'bbc-radio-humberside.jpg',
                                     'desc': ''},
            'BBC Radio Jersey': {'url': base_url + 'ww/bbc_radio_jersey/bbc_radio_jersey.isml/bbc_radio_jersey-audio%3d48000.norewind.m3u8',
                                 'thumb': image_path + 'bbc-radio-jersey-logo.png',
                                 'fanart': image_path + 'bbc-radio-jersey.jpg',
                                 'desc': ''},
            'BBC Radio Kent': {'url': base_url + 'ww/bbc_radio_kent/bbc_radio_kent.isml/bbc_radio_kent-audio%3d48000.norewind.m3u8',
                               'thumb': image_path + 'bbc-radio-kent-logo.png',
                               'fanart': image_path + 'bbc-radio-kent.jpg',
                               'desc': ''},
            'BBC Radio Lancashire': {'url': base_url + 'ww/bbc_radio_lancashire/bbc_radio_lancashire.isml/bbc_radio_lancashire-audio%3d48000.norewind.m3u8',
                                     'thumb': image_path + 'bbc-radio-lancashire-logo.png',
                                     'fanart': image_path + 'bbc-radio-lancashire.jpg',
                                     'desc': ''},
            'BBC Radio Leeds': {'url': base_url + 'ww/bbc_radio_leeds/bbc_radio_leeds.isml/bbc_radio_leeds-audio%3d48000.norewind.m3u8',
                                'thumb': image_path + 'bbc-radio-leeds-logo.png',
                                'fanart': image_path + 'bbc-radio-leeds.jpg',
                                'desc': ''},
            'BBC Radio Leicester': {'url': base_url + 'ww/bbc_radio_leicester/bbc_radio_leicester.isml/bbc_radio_leicester-audio%3d48000.norewind.m3u8',
                                    'thumb': image_path + 'bbc-radio-leicester-logo.png',
                                    'fanart': image_path + 'bbc-radio-leicester.jpg',
                                    'desc': ''},
            'BBC Radio Lincolnshire': {'url': base_url + 'ww/bbc_radio_lincolnshire/bbc_radio_lincolnshire.isml/bbc_radio_lincolnshire-audio%3d48000.norewind.m3u8',
                                       'thumb': image_path + 'bbc-radio-lincolnshire-logo.png',
                                       'fanart': image_path + 'bbc-radio-lincolnshire.jpg',
                                       'desc': ''},
            'BBC Radio London': {'url': base_url + '/ww/bbc_london/bbc_london.isml/bbc_london-audio%3d48000.norewind.m3u8',
                                 'thumb': image_path + 'bbc-radio-london-logo.png',
                                 'fanart': image_path + 'bbc-radio-london.jpg',
                                 'desc': ''},
            'BBC Radio Manchester': {'url': base_url + 'ww/bbc_radio_manchester/bbc_radio_manchester.isml/bbc_radio_manchester-audio%3d48000.norewind.m3u8',
                                     'thumb': image_path + 'bbc-radio-manchester-logo.png',
                                     'fanart': image_path + 'bbc-radio-manchester.jpg',
                                     'desc': ''},
            'BBC Radio Merseyside': {'url': base_url + 'ww/bbc_radio_merseyside/bbc_radio_merseyside.isml/bbc_radio_merseyside-audio%3d48000.norewind.m3u8',
                                     'thumb': image_path + 'bbc-radio-merseyside-logo.png',
                                     'fanart': image_path + 'bbc-radio-merseyside.jpg',
                                     'desc': ''},
            'BBC Newcastle': {'url': base_url + 'ww/bbc_radio_newcastle/bbc_radio_newcastle.isml/bbc_radio_newcastle-audio%3d48000.norewind.m3u8',
                              'thumb': image_path + 'bbc-newcastle-logo.png',
                              'fanart': image_path + 'bbc-newcastle.jpg',
                              'desc': ''},
            'BBC Radio Norfolk': {'url': base_url + 'ww/bbc_radio_norfolk/bbc_radio_norfolk.isml/bbc_radio_norfolk-audio%3d48000.norewind.m3u8',
                                  'thumb': image_path + 'bbc-radio-norfolk-logo.png',
                                  'fanart': image_path + 'bbc-radio-norfolk.jpg',
                                  'desc': ''},
            'BBC Radio Northampton': {'url': base_url + 'ww/bbc_radio_northampton/bbc_radio_northampton.isml/bbc_radio_northampton-audio%3d48000.norewind.m3u8',
                                      'thumb': image_path + 'bbc-radio-northampton-logo.png',
                                      'fanart': image_path + 'bbc-radio-northampton.jpg',
                                      'desc': ''},
            'BBC Radio Nottingham': {'url': base_url + 'ww/bbc_radio_nottingham/bbc_radio_nottingham.isml/bbc_radio_nottingham-audio%3d48000.norewind.m3u8',
                                     'thumb': image_path + 'bbc-radio-nottingham-logo.png',
                                     'fanart': image_path + 'bbc-radio-nottingham.jpg',
                                     'desc': ''},
            'BBC Radio Oxford': {'url': base_url + 'ww/bbc_radio_oxford/bbc_radio_oxford.isml/bbc_radio_oxford-audio%3d48000.norewind.m3u8',
                                 'thumb': image_path + 'bbc-radio-oxford-logo.png',
                                 'fanart': image_path + 'bbc-radio-oxford.jpg',
                                 'desc': ''},
            'BBC Radio Sheffield': {'url': base_url + 'ww/bbc_radio_sheffield/bbc_radio_sheffield.isml/bbc_radio_sheffield-audio%3d48000.norewind.m3u8',
                                    'thumb': image_path + 'bbc-radio-sheffield-logo.png',
                                    'fanart': image_path + 'bbc-radio-sheffield.jpg',
                                    'desc': ''},
            'BBC Radio Shropshire': {'url': base_url + 'ww/bbc_radio_shropshire/bbc_radio_shropshire.isml/bbc_radio_shropshire-audio%3d48000.norewind.m3u8',
                                     'thumb': image_path + 'bbc-radio-shropshire-logo.png',
                                     'fanart': image_path + 'bbc-radio-shropshire.jpg',
                                     'desc': ''},
            'BBC Radio Solent': {'url': base_url + 'ww/bbc_radio_solent/bbc_radio_solent.isml/bbc_radio_solent-audio%3d48000.norewind.m3u8',
                                 'thumb': image_path + 'bbc-radio-solent-logo.png',
                                 'fanart': image_path + 'bbc-radio-solent.jpg',
                                 'desc': ''},
            'BBC Somerset': {'url': base_url + 'ww/bbc_radio_somerset_sound/bbc_radio_somerset_sound.isml/bbc_radio_somerset_sound-audio%3d48000.norewind.m3u8',
                             'thumb': image_path + 'bbc-somerset-logo.png',
                             'fanart': image_path + 'bbc-somerset.jpg',
                             'desc': ''},
            'BBC Radio Stoke': {'url': base_url + 'ww/bbc_radio_stoke/bbc_radio_stoke.isml/bbc_radio_stoke-audio%3d48000.norewind.m3u8',
                                'thumb': image_path + 'bbc-radio-stoke-logo.png',
                                'fanart': image_path + 'bbc-radio-stoke.jpg',
                                'desc': ''},
            'BBC Radio Suffolk': {'url': base_url + 'ww/bbc_radio_suffolk/bbc_radio_suffolk.isml/bbc_radio_suffolk-audio%3d48000.norewind.m3u8',
                                  'thumb': image_path + 'bbc-radio-suffolk-logo.png',
                                  'fanart': image_path + 'bbc-radio-suffolk.jpg',
                                  'desc': ''},
            'BBC Surrey': {'url': base_url + 'ww/bbc_radio_surrey/bbc_radio_surrey.isml/bbc_radio_surrey-audio%3d48000.norewind.m3u8',
                           'thumb': image_path + 'bbc-surrey-logo.png',
                           'fanart': image_path + 'bbc-surrey.jpg',
                           'desc': ''},
            'BBC Sussex': {'url': base_url + 'ww/bbc_radio_sussex/bbc_radio_sussex.isml/bbc_radio_sussex-audio%3d48000.norewind.m3u8',
                           'thumb': image_path + 'bbc-sussex-logo.png',
                           'fanart': image_path + 'bbc-sussex.jpg',
                           'desc': ''},
            'BBC Tees': {'url': base_url + 'ww/bbc_tees/bbc_tees.isml/bbc_tees-audio%3d48000.norewind.m3u8',
                         'thumb': image_path + 'bbc-tees-logo.png',
                         'fanart': image_path + 'bbc-tees.jpg',
                         'desc': ''},
            'BBC Three Counties Radio': {'url': base_url + 'ww/bbc_three_counties_radio/bbc_three_counties_radio.isml/bbc_three_counties_radio-audio%3d48000.norewind.m3u8',
                                         'thumb': image_path + 'bbc-three-counties-radio-logo.png',
                                         'fanart': image_path + 'bbc-three-counties-radio.jpg',
                                         'desc': ''},
            'BBC Wiltshire': {'url': base_url + 'ww/bbc_radio_wiltshire/bbc_radio_wiltshire.isml/bbc_radio_wiltshire-audio%3d48000.norewind.m3u8',
                              'thumb': image_path + 'bbc-wiltshire-logo.png',
                              'fanart': image_path + 'bbc-wiltshire.jpg',
                              'desc': ''},
            'BBC WM 95.6': {'url': base_url + 'ww/bbc_wm/bbc_wm.isml/bbc_wm-audio%3d48000.norewind.m3u8',
                            'thumb': image_path + 'bbc-wm956-logo.png',
                            'fanart': image_path + 'bbc-wm956.jpg',
                            'desc': ''},
            'BBC Radio York': {'url': base_url + 'ww/bbc_radio_york/bbc_radio_york.isml/bbc_radio_york-audio%3d48000.norewind.m3u8',
                               'thumb': image_path + 'bbc-radio-york-logo.png',
                               'fanart': image_path + 'bbc-radio-york.jpg',
                               'desc': ''}
           }

def list_categories():
    """
    Create the list of playable videos in the Kodi interface.
    :return: None
    """
    for item in category_list:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=item)
        addDir(item,
               __url__,
               1,
               categories[item]['thumb'],
               categories[item]['fanart'],
               categories[item]['desc'],
               isFolder=True)


def get_links(name, url, icon, fanart):
    """
    Create the list of playable audio links
    """
    if name == _national_radio:
        cur_list = station_list_nr
    elif name == _nations_and_regions:
        cur_list = station_list_nar
    elif name == _local_radio:
        cur_list = station_list_lr

    for item in cur_list:
        # Create a list ite with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=item)
        addDir(item,
               stations[item]['url'],
               2,
               stations[item]['thumb'],
               stations[item]['fanart'],
               stations[item]['desc'],
               isFolder=False)


def play_audio(name, url, icon, fanart):
    """
    Create a list item to the audio stream and
    start playing the audio stream.
    """
    if xbmc.Player().isPlayingAudio:
        xbmc.Player().stop()
    liz = xbmcgui.ListItem(name)
    # Set fanart image for the list item.
    liz.setArt({'fanart': fanart, 'thumb': icon})
    xbmc.Player().play(url, liz, False)
    xbmc.executebuiltin('Action(Fullscreen)')


def addDir(name, url, mode, icon, fanart, desc, isFolder=False):
    """
    Display a list of links
    """
    u = (sys.argv[0] + '?url=' + urllib.parse.quote_plus(url) +
         '&mode=' + str(mode) + '&name=' + urllib.parse.quote_plus(name) +
         '&icon=' + str(icon) + '&fanart=' + str(fanart))
    ok = True
    liz = xbmcgui.ListItem(name)
    # Set fanart and thumb images for the list item.
    if not fanart:
        # Set fanart to default image
        fanart = __fanart__
    if not icon:
        # Set icon to default image
        icon = __icon__

    liz.setArt({'fanart': fanart, 'thumb': icon})
    # Set additional info for the list item.
    liz.setInfo(type='music',
                infoLabels={'title': name,
                            'album': __addonname__,
                            'artist': name,
                            'genre': _internet_radio,
                            'year': 2015
                            })
    liz.setInfo(type='video',
                infoLabels={'title': name,
                            'genre': _internet_radio,
                            'plot': desc,
                            'year': 2015,
                            'status': 'Live',
                            'mediatype': 'musicvideo'
                            })
    ok = xbmcplugin.addDirectoryItem(handle=__handle__,
                                     url=u,
                                     listitem=liz,
                                     isFolder=isFolder)
    return ok


def get_params():
    """
    Get the current parameters
    :return: param[]
    """
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring[1:])>=1:
        params=paramstring[1:]
        pairsofparams=params.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param


def msg_notification(heading, message, icon, duration):
    # Show message notification
    dialog = xbmcgui.Dialog()
    dialog.notification(heading, message, icon, duration)


def message(message, title):
    # Display message to user
    dialog = xbmcgui.Dialog()
    dialog.ok(title, message)


# Define local variables
params = get_params()
url = None
name = None
mode = None
icon = None
fanart = None

# Parse the url, name, mode, icon and fanart parameters
try:
    url = urllib.parse.unquote_plus(params['url'])
except:
    pass
try:
    name = urllib.parse.unquote_plus(params['name'])
except:
    pass
try:
    mode = int(params['mode'])
except:
    pass
try:
    icon = urllib.parse.unquote_plus(params['icon'])
except:
    pass
try:
    fanart = urllib.parse.unquote_plus(params['fanart'])
except:
    pass

# Route the request based upon the mode number
if mode is None or url is None or len(url) < 1:
    list_categories()
elif mode == 1:
    _default_image = fanart
    get_links(name, url, icon, fanart)
elif mode == 2:
    play_audio(name, url, icon, fanart)

xbmcplugin.endOfDirectory(__handle__)
