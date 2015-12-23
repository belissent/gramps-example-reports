# -*- coding: utf-8 -*-
#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2014 Pierre Bélissent
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# $Id: $

'''
Dynamic Web Report test sets

Used for: testing and generating report examples
'''


import glob, os, sys

from report_set import *

sys.path.append(os.path.join(os.environ['GRAMPS_PLUGINS'], 'DynamicWeb'))
from dynamicweb import (
    INCLUDE_LIVING_VALUE,
    DEFAULT_SVG_TREE_TYPE,
    DEFAULT_SVG_TREE_SHAPE,
    PAGES_NAMES,
    WEB_TEMPLATE_LIST,
)


#-------------------------------------------------------------------------
#
# Test sets
#
#-------------------------------------------------------------------------


default_options = {
    'name' : 'DynamicWeb',
    'archive': False,
    'archive_file': 'archive.zip',
    # 'filter', self.__filter)
    # 'pid', self.__pid)
    # 'name_format': 0,
    # 'short_name_format': 0,
    'template': 0,
    'copyright': 0,
    'incpriv': True,
    'inc_notes': True,
    'inc_sources': True,
    'inc_addresses': True,
    'living': INCLUDE_LIVING_VALUE,
    'yearsafterdeath': 30,
    'inc_repositories': True,
    'inc_gallery': True,
    'copy_media': True,
    'print_notes_type': True,
    'inc_places': True,
    'placemappages': True,
    'familymappages': True,
    'mapservice': 'Google',
    'tabbed_panels': False,
    'encoding': 'UTF-8',
    'inc_families': True,
    # 'inc_events': True,
    'showbirth': True,
    'showdeath': True,
    'showmarriage': True,
    'showpartner': True,
    'showparents': True,
    'showallsiblings': True,
    # 'birthorder': False,
    'bkref_type': True,
    'inc_gendex': True,
    'inc_pageconf': True,
    'graphgens': 10,
    'svg_tree_type': DEFAULT_SVG_TREE_TYPE,
    'svg_tree_shape': DEFAULT_SVG_TREE_SHAPE,
    'svg_tree_color1': '#EF2929',
    'svg_tree_color2': '#3D37E9',
    'svg_tree_color_dup': '#888A85',
    'headernote': '_header1',
    'footernote': '_footer1',
    'custom_note_0': '_custom1',
    'custom_menu_0': False,
    'pages_number': len(PAGES_NAMES) + 1,
}

def merge_options(x, y = default_options):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


conf_list = [
{
    'title': '"%s" default configuration',
    'options': {
    },
},
{
    'title': '"%s" with full set of features',
    'options': merge_options({
        'archive': True,
        'archive_file': 'archive.zip',
    }),
},
{
    'title':  '"%%s" using template "%s", OpenStreetMap, and tabbed panels' % WEB_TEMPLATE_LIST[1][1],
    'options': merge_options({
        'template': 1,
        'mapservice': 'OpenStreetMap',
        'tabbed_panels': True,
    }),
},
{
    'title': '"%s" with minimal features (without private data, notes, sources, addresses, gallery, places, families)',
    'options': merge_options({
        'incpriv': False,
        'inc_notes': False,
        'inc_sources': False,
        'inc_addresses': False,
        'inc_repositories': False,
        'inc_gallery': False,
        'inc_places': False,
        'inc_families': False,
        # 'inc_events': False,
        'living': LivingProxyDb.MODE_EXCLUDE_ALL,
        'inc_pageconf': False,
    }),
},
]


def addon_set():
    addons = []
    for (i, conf) in enumerate(conf_list):
        opts = {
            'target': os.path.join(ADDONS_REP_DIR, 'example_DynamicWeb%i' % i),
        }
        opts.update(conf['options'])
        addons.append({
            'title': conf['title'],
            'result': os.path.join(ADDONS_REP_DIR, 'example_DynamicWeb%i' % i, 'index.html'),
            'i': 'DynamicWeb',
            'options': opts,
        })
    return addons
