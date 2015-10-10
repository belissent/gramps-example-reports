# -*- coding: utf-8 -*-

#
# Report test sets for GRAMPS: Generate every report in every format.
#


import os

from gramps.version import VERSION

reports = []

##################################################################
# GRAMPS native plugins
##################################################################

GRAMPS_REP_DIR = os.path.join(os.environ['GRAMPS_REPORTS'], "gramps")

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
# GRAMPS addons reports
##################################################################

#TODO
