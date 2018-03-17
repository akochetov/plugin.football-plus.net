# -*- coding: utf-8 -*-

import urllib
try:
    from urllib.parse import parse_qs
except ImportError:
     from urlparse import parse_qs
from urllib import urlencode
import sys
import json

#kodi libs import
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

#fp custom lib import
import fp

#constants
_Addon = xbmcaddon.Addon(id='plugin.football-plus.net')
__language__ = _Addon.getLocalizedString

addon_icon = _Addon.getAddonInfo('icon')
addon_fanart = _Addon.getAddonInfo('fanart')
addon_path = _Addon.getAddonInfo('path')
addon_type = _Addon.getAddonInfo('type')
addon_id = _Addon.getAddonInfo('id')
addon_author = _Addon.getAddonInfo('author')
addon_name = _Addon.getAddonInfo('name')
addon_version = _Addon.getAddonInfo('version')
print(sys.argv)
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = {}
if len(sys.argv)>1:
    args = parse_qs(sys.argv[2][1:])
print("Parameters: "+str(args))

def build_url(params):
    return '%s?%s' % (base_url, urllib.urlencode(params))

def showMessage(heading, message, times=3000, pics=addon_icon):
    try:
        xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (
        heading.encode('utf-8'), message.encode('utf-8'), times, pics.encode('utf-8')))
    except Exception as e:
        xbmc.log('[%s]: showMessage: Transcoding UTF-8 failed [%s]' % (addon_id, e), 2)
        try:
            xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading, message, times, pics))
        except Exception as e:
            xbmc.log('[%s]: showMessage: exec failed [%s]' % (addon_id, e), 3)

#plugin functions
##########################################################

def mainMenu(args):
    li = xbmcgui.ListItem(u'Последние матчи', iconImage=addon_icon, thumbnailImage=addon_icon)

    uri = build_url({
        'func': 'openLeague',
        'mpath': fp.getLastMatchesURL().encode('utf-8')
        })
    li.setProperty('fanart_image', addon_fanart)
    xbmcplugin.addDirectoryItem(addon_handle, uri, li, True)

    hits = fp.getMenuItems()

    for hit in hits:
        print('[%s]: mainMenu: hit [%s] image [%s] url [%s]' % (addon_id, hit.title().encode('utf-8'), hit.image().encode('utf-8'), hit.url().encode('utf-8')))
        li = xbmcgui.ListItem(hit.title(), iconImage=hit.image(), thumbnailImage=hit.image())

        uri = build_url({
            'func': 'openMenu',
            'mtitle': hit.title().encode('utf-8'),
            'mimage': hit.image().encode('utf-8'),
            'mpath': hit.url().encode('utf-8')
        })

        li.setInfo(type='Video', infoLabels={'title': hit.title(), 'plot': hit.title()})
        li.setProperty('fanart_image', addon_fanart)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(addon_handle, uri, li, True)

    xbmcplugin.setContent(addon_handle, 'movies')
    xbmcplugin.endOfDirectory(addon_handle)

def openMenu(args):
    hits = fp.openMenu(args['mpath'][0])

    for hit in hits:
        print('[%s]: mainMenu: hit [%s] image [%s] url [%s]' % (addon_id, hit.title().encode('utf-8'), hit.image().encode('utf-8'), hit.url().encode('utf-8')))
        li = xbmcgui.ListItem(hit.title(), iconImage=hit.image(), thumbnailImage=hit.image())

        uri = build_url({
            'func': 'openLeague',
            'mtitle': hit.title().encode('utf-8'),
            'mimage': hit.image().encode('utf-8'),
            'mpath': hit.url().encode('utf-8')
        })

        li.setInfo(type='Video', infoLabels={'title': hit.title(), 'plot': hit.title()})
        li.setProperty('fanart_image', addon_fanart)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(addon_handle, uri, li, True)

    xbmcplugin.setContent(addon_handle, 'movies')
    xbmcplugin.endOfDirectory(addon_handle)

def openLeague(args):
    hits = fp.openLeague(args['mpath'][0])

    for hit in hits:
        print('[%s]: openLeague: hit [%s] image [%s] url [%s]' % (addon_id, hit.title().encode('utf-8'), hit.image().encode('utf-8'), hit.url().encode('utf-8')))
        li = xbmcgui.ListItem(hit.title(), iconImage=hit.image(), thumbnailImage=hit.image())

        uri = None
        if hit.title() == fp.getPrevTitle() or hit.title() == fp.getNextTitle():
            uri = build_url({
            'func': 'openLeague',
            'mtitle': hit.title().encode('utf-8'),
            'mimage': hit.image().encode('utf-8'),
            'mpath': hit.url().encode('utf-8')
            })
        else:
            uri = build_url({
            'func': 'openMatch',
            'mtitle': hit.title().encode('utf-8'),
            'mimage': hit.image().encode('utf-8'),
            'mpath': hit.url().encode('utf-8')
            })

        li.setInfo(type='Video', infoLabels={'title': hit.title(), 'plot': hit.title()})
        li.setProperty('fanart_image', addon_fanart)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(addon_handle, uri, li, True)

    xbmcplugin.setContent(addon_handle, 'movies')
    xbmcplugin.endOfDirectory(addon_handle)

def openMatch(args):
    hits = fp.openMatch(args['mpath'][0])

    for hit in hits:
        print('[%s]: openMatch: hit [%s] image [%s] url [%s]' % (addon_id, hit.title().encode('utf-8'), hit.image().encode('utf-8'), hit.url().encode('utf-8')))
        li = xbmcgui.ListItem(hit.title(), iconImage=hit.image(), thumbnailImage=hit.image())

        uri = build_url({
            'func': 'openVideo',
            'mtitle': hit.title().encode('utf-8'),
            'mimage': hit.image().encode('utf-8'),
            'mpath': hit.url().encode('utf-8')
        })

        li.setInfo(type='Video', infoLabels={'title': hit.title(), 'plot': hit.title()})
        li.setProperty('fanart_image', addon_fanart)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(addon_handle, uri, li, False)

    xbmcplugin.setContent(addon_handle, 'movies')
    xbmcplugin.endOfDirectory(addon_handle)

def openVideo(args):
    item = xbmcgui.ListItem(path=args['mpath'][0])
    xbmcplugin.setResolvedUrl(addon_handle, True, item)

def run_settings(params):
    _Addon.openSettings()

#main program
func = args.get('func', None)

if func is None:
    xbmc.log('[%s]: Primary input' % addon_id, 1)
    mainMenu(args)
else:
    globals()[func[0]](args)

