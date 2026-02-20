# -*- coding: utf-8 -*-

def classFactory(iface):
    from .geopacker import Geopacker
    return Geopacker(iface)
