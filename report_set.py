# -*- coding: utf-8 -*-

#
# Report test sets for GRAMPS: Generate every report in every format.
#


import os

from gramps.version import VERSION
from gramps.plugins.webreport.narrativeweb import _INCLUDE_LIVING_VALUE

reports = []

##################################################################
# GRAMPS native plugins
##################################################################

GRAMPS_REP_DIR = os.path.join(os.environ['GRAMPS_REPORTS'], 'gramps')

GRPH_FMT = ["odt", "ps", "pdf", "svg"]
# GRPH_FMT = ["svg"]
GRPH_REP = [
    {
        'report': "ancestor_chart",
        'options': {
            'pid': "I0006",
        },
    },
    {
        'report': "descend_chart",
        'options': {
            'pid': "I0104",
        },
    },
    {
        'report': "fan_chart",
        'options': {
            'pid': "I0006",
        },
    },
    {
        'report': "statistics_chart",
        'options': {
       },
    },
    {
        'report': "timeline",
        'options': {
        },
    },
    {
        'report': "calendar",
        'options': {
        },
    },
]

TEXT_FMT = ["ps", "pdf", "html", "odt", "tex", "rtf", "txt"]
# TEXT_FMT = ["html"]
TEXT_REP = [
    {
        'report': "ancestor_report",
        'options': {
            'pid': "I0006",
        },
    },
    {
        'report': "descend_report",
        'options': {
            'pid': "I0104",
        },
    },
    {
        'report': "det_ancestor_report",
        'options': {
            'pid': "I0006",
        },
    },
    {
        'report': "det_descendant_report",
        'options': {
            'pid': "I0104",
        },
    },
    {
        'report': "family_group",
        'options': {
            'family_id': "F0017",
        },
    },
]


# Single run with all graphical reports in all formats
for rep_info in GRPH_REP:
    report = rep_info['report']
    options = rep_info['options']
    for fmt in GRPH_FMT:
        of = os.path.join(GRAMPS_REP_DIR, report + '.' + fmt)
        new_options = {
            'name': report,
            'off': fmt,
            'of': of,
            'scale_tree': 2,
            'maxgen': 6,
            # 'show': 'all',
        }
        new_options.update(options)
        reports.append({
            'title': "Graphical report \"%s\" in format \"%s\"" % (report, fmt),
            'result': of,
            'type': 'Native',
            'version': VERSION,
            'options': new_options,
        })

# Single run with all textual reports in all formats
for rep_info in TEXT_REP:
    report = rep_info['report']
    options = rep_info['options']
    for fmt in TEXT_FMT:
        of = os.path.join(GRAMPS_REP_DIR, report + '.' + fmt)
        new_options = {
            'name': report,
            'off': fmt,
            'of': of,
            'maxgen': 6,
            # 'show': 'all',
        }
        new_options.update(options)
        reports.append({
            'title': "Textual report \"%s\" in format \"%s\"" % (report, fmt),
            'result': of,
            'type': 'Native',
            'version': VERSION,
            'options': new_options,
        })

##################################################################
# GRAMPS addons reports listing
##################################################################

def read_listing(filename):
    listing = []
    fp = open(filename, 'r')
    for line in fp.readlines():
        try:
            plugin_dict = eval(line, {})
            if type(plugin_dict) == type({}): listing.append(plugin_dict)
        except:
            pass
    fp.close()
    return listing

lang = 'en'
listing = read_listing(os.path.join(os.environ['GRAMPS_ADDONS_SOURCE'], 'listings', 'addons-%s.txt' % lang))


##################################################################
# GRAMPS addons reports
##################################################################

ADDONS_REP_DIR = os.path.join(os.environ['GRAMPS_REPORTS'], 'addons')

addons=[]
addons.append({
    'title': 'DynammicWeb report with "Mainz" style',
    'result': os.path.join(ADDONS_REP_DIR, 'example_DynamicWeb', 'index.html'),
    'i': 'DynamicWeb',
    'options': {
        'target': os.path.join(ADDONS_REP_DIR, 'example_DynamicWeb'),
        'template': 1,
        'inc_pageconf': True,
        'incpriv': True,
        'living': _INCLUDE_LIVING_VALUE,
    },
})
# addons=[]
# addons.append({
#     'title': 'DenominoViso with default options',
#     'result': os.path.join(ADDONS_REP_DIR, 'example_denominoviso', 'index.html'),
#     'i': 'denominoviso',
#     'options': {
#         'DNMinc_attributes_m': 'True, ',
#     },
# })
# addons=[]
# for fmt in TEXT_FMT:
#     of = os.path.join(ADDONS_REP_DIR, 'ListeEclair.' + fmt)
#     addons.append({
#         'title': 'Textual report "ListeEclair" in format "%s"' % fmt,
#         'result': of,
#         'i': 'ListeEclair',
#         'options': {
#             'off': fmt,
#             'of': of,
#         },
#     })


reports=[]

for addon in addons:
    addon_id = next(l for l in listing if l['i'] == addon['i'])
    addon['options'].update({
        'name': addon['i'],
    })
    addon.update({
        'type': 'Addon',
        'version': addon_id['v'],
    })
    reports.append(addon)
