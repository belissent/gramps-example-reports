# -*- coding: utf-8 -*-

#
# Report test sets for GRAMPS: Generate every report in every format.
#


import os

from gramps.version import VERSION
from gramps.plugins.webreport.narrativeweb import _INCLUDE_LIVING_VALUE, CSS

reports = []

##################################################################
# GRAMPS native plugins
##################################################################

GRAMPS_REP_DIR = os.path.join(os.environ['GRAMPS_REPORTS'], 'gramps')

# GRPH_FMT = ["odt", "ps", "pdf", "svg"]
GRPH_FMT = ["pdf", "svg"]
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
        'report': "family_descend_chart",
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
    {
        'report': "familylines_graph",
        'options': {
            'gidlist': "I0104 I0045",
            'limitchildren': True,
            'maxchildren': 20,
        },
    },
    {
        'report': "hourglass_graph",
        'options': {
            'pid': 'I0044',
            'maxascend': 2,
            'maxdescend': 2,
        },
    },
    {
        'report': "rel_graph",
        'options': {
            'pid': 'I0044',
            'filter': 3,
            'event_choice': 2,
        },
    },
]

# TEXT_FMT = ["ps", "pdf", "html", "odt", "tex", "rtf", "txt"]
TEXT_FMT = ["html", "pdf", 'txt']
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
    {
        'report': "birthday_report",
        'options': {},
    },
    {
        'report': "endofline_report",
        'options': {
            'pid': "I0006",
        },
    },
    {
        'report': "indiv_complete",
        'options': {},
    },
    {
        'report': "kinship_report",
        'options': {
            'pid': 'I0044',
        },
    },
    {
        'report': "tag_report",
        'options': {
            'tag': 'ToDo',
        },
    },
    {
        'report': "number_of_ancestors",
        'options': {
            'pid': "I0006",
        },
    },
    {
        'report': "place_report",
        'options': {
            'places': 'P1678 P1679 P1680',
        },
    },
    {
        'report': "summary",
        'options': {},
    },
    {
        'report': "records",
        'options': {},
    },
    {
        'report': "notelinkreport",
        'options': {},
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
# GRAMPS native web reports
##################################################################

full_options = {
    'linkhome': True,
    'showdeath': True,
    'showpartner': True,
    'showparents': True,
    'showhalfsiblings': True,
    'inc_families': True,
    'inc_repository': True,
    'inc_gendex': True,
    'inc_addressbook': True,
    'placemappages': True,
    'familymappages': True,
}

for (i, css, full) in enumerate([
    ["default", False],
    ["Mainz", True],
]):
    opts = {
        'name': 'navwebpage',
        'target': os.path.join(ADDONS_REP_DIR, 'example_NAVWEB%i' % i),
        'css':  CSS[css]["id"],
        'living': _INCLUDE_LIVING_VALUE,
    }
    if (full): opts.update(full_options)
    reports.append({
        'title': 'NarrativeWeb report example %i' % i,
        'result': os.path.join(ADDONS_REP_DIR, 'example_NAVWEB%i' % i, 'index.html'),
        'type': 'Native',
        'version': VERSION,
        'options': opts,
    })


full_options = {
    'alive': False,
    'fullyear': True,
    'makeoneday': True,
    'link_to_narweb': True,
}

for (i, css, full) in enumerate([
    ["default", False],
    ["Mainz", True],
]):
    opts = {
        'name': 'WebCal',
        'target': os.path.join(ADDONS_REP_DIR, 'example_WebCal%i' % i),
        'css':  CSS[css]["id"],
        'home_link': '../../example_NAVWEB%i/index.html' % i
        'prefix': '../../example_NAVWEB%i/' % i
    }
    if (full): opts.update(full_options)
    reports.append({
        'title': 'Web Calendar report example %i' % i,
        'result': os.path.join(ADDONS_REP_DIR, 'example_WebCal%i' % i, 'index.html'),
        'type': 'Native',
        'version': VERSION,
        'options': opts,
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


########## AncestorFill

for fmt in TEXT_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'AncestorFill.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'AncestorFill',
        'options': {
            'off': fmt,
            'of': of,
        },
    })


########## d3-ancestralcollapsibletree

addons.append({
    'title': '"%%s" report example',
    'result': os.path.join(ADDONS_REP_DIR, 'd3-ancestralcollapsibletree', 'index.html'),
    'i': 'd3-ancestralcollapsibletree',
    'options': {
        'dest_path': os.path.join(ADDONS_REP_DIR, 'd3-ancestralcollapsibletree'),
        'dest_file': 'index.html'),
        'pid': 'I0006',
        'maxgen': 6,
    },
})


########## d3-ancestralfanchart

addons.append({
    'title': '"%%s" report example',
    'result': os.path.join(ADDONS_REP_DIR, 'd3-ancestralfanchart', 'index.html'),
    'i': 'd3-ancestralfanchart',
    'options': {
        'dest_path': os.path.join(ADDONS_REP_DIR, 'd3-ancestralfanchart'),
        'dest_file': 'index.html'),
        'pid': 'I0006',
        'maxgen': 6,
    },
})


########## d3-descendantindentedtree

addons.append({
    'title': '"%%s" report example',
    'result': os.path.join(ADDONS_REP_DIR, 'd3-descendantindentedtree', 'index.html'),
    'i': 'd3-descendantindentedtree',
    'options': {
        'dest_path': os.path.join(ADDONS_REP_DIR, 'd3-descendantindentedtree'),
        'dest_file': 'index.html'),
        'pid': 'I0104',
        'max_gen': 6,
        'inc_private': True,
        'inc_living': _INCLUDE_LIVING_VALUE,
    },
})


########## denominoviso

for (i, mode, type, dir, pid, full) in enumerate([
    [0, 0, 0, 'I0001', True],
    [0, 3, 2, 'I0001', False],
    [0, 4, 2, 'I0001', False],
    [1, 0, 0, 'I0044', True],
    [1, 1, 0, 'I0044', False],
]):
    addons.append({
        'title': '"%%s" report example %i' % i,
        'result': os.path.join(ADDONS_REP_DIR, 'DenominoViso%i.xhtml' % i),
        'i': 'denominoviso',
        'options': {
            'DNMfilename': os.path.join(ADDONS_REP_DIR, 'DenominoViso%i.xhtml' % i),
            'DNMchart_mode': mode,
            'DNMpid': pid,
            'DNMchart_type': type,
            'DNMinc_attributes_m': '"True, "',
            'DNMinc_addresses': full,
            'DNMinc_notes': full,
            'DNMinc_url': full,
            'DNMinc_url_desc': full,
            'DNMinc_sources': full,
            'DNMinc_img': full,
            'DNMcopy_img_m': '"%s, %s%i"' % (str(full), os.path.join(ADDONS_REP_DIR, 'DenominoViso'), i),
        },
    })


########## DescendantBook

for fmt in TEXT_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'DescendantBook.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'DescendantBook',
        'options': {
            'off': fmt,
            'of': of,
        },
    })

for fmt in TEXT_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'DetailedDescendantBook.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'DetailedDescendantBook',
        'options': {
            'off': fmt,
            'of': of,
        },
    })


########## Descendants Lines

for fmt in GRPH_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'DescendantsLines.' + fmt)
    addons.append({
        'title': 'Graphical report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'Descendants Lines',
        'options': {
            'off': fmt,
            'of': of,
            'pid': 'I0006',
        },
    })


########## database-differences-report

for fmt in ["html"]:
    of = os.path.join(ADDONS_REP_DIR, 'database-differences-report.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'database-differences-report',
        'options': {
            'off': fmt,
            'of': of,
            'filename': os.path.join(os.environ['GRAMPS_RESOURCES'], "example", "gramps", "example.gramps"),
        },
    })


########## DynamicWeb

full_options = {
    'archive': True,
    'archive_file': "archive.zip",
    'incpriv': True,
    'inc_notes': True,
    'inc_sources': True,
    'inc_addresses': True,
    'living': INCLUDE_LIVING_VALUE,
    'inc_repositories': True,
    'inc_gallery': True,
    'copy_media': True,
    'print_notes_type': True,
    'inc_places': True,
    'placemappages': True,
    'familymappages': True,
    'mapservice': "Google",
    'tabbed_panels': False,
    'encoding': "UTF-8",
    'inc_families': True,
    'showbirth': True,
    'showdeath': True,
    'showmarriage': True,
    'showpartner': True,
    'showparents': True,
    'showallsiblings': True,
    'bkref_type': True,
    'inc_gendex': True,
    'inc_pageconf': True,
    'headernote': "_header1",
    'footernote': "_footer1",
    'custom_note_0': "_custom1",
    'pages_number': len(PAGES_NAMES) + 1,
}

for (i, template, full) in enumerate([
    [0, True],
    [1, False],
]):
    opts = {
        'target': os.path.join(ADDONS_REP_DIR, 'example_DynamicWeb%i' % i),
        'template': template,
    }
    if (full): opts.update(full_options)
    addons.append({
        'title': '"%%s" report example %i' % i,
        'result': os.path.join(ADDONS_REP_DIR, 'example_DynamicWeb%i' % i, 'index.html'),
        'i': 'DynamicWeb',
        'options': opts,
    })


########## FamilyTree

for fmt in GRPH_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'FamilyTree.' + fmt)
    addons.append({
        'title': 'Graphical report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'FamilyTree',
        'options': {
            'off': fmt,
            'of': of,
            'pid': 'I0006',
            'max_ancestor_generations': 3,
            'max_descendant_generations': 3,
            'papero': 1,
            'protect_private': False,
            'color': 1,
        },
    })


########## LastChangeReport

for fmt in ["html"]:
    of = os.path.join(ADDONS_REP_DIR, 'LastChangeReport.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'LastChangeReport',
        'options': {
            'off': fmt,
            'of': of,
            'what_types': '"True,True,True,True,True,True"'
        },
    })


########## LinesOfDescendency

for fmt in ["html"]:
    of = os.path.join(ADDONS_REP_DIR, 'LinesOfDescendency.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'LinesOfDescendency',
        'options': {
            'off': fmt,
            'of': of,
            'pid': 'I0006',
            'ancestor': 'I0104',
        },
    })


########## ListeEclair

for fmt in TEXT_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'ListeEclair.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'ListeEclair',
        'options': {
            'off': fmt,
            'of': of,
        },
    })


########## PedigreeChart

for fmt in GRPH_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'PedigreeChart.' + fmt)
    addons.append({
        'title': 'Graphical report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'PedigreeChart',
        'options': {
            'off': fmt,
            'of': of,
            'maxgen': 6,
            'pid': 'I0006',
        },
    })


########## PersonEverythingReport

for fmt in TEXT_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'PersonEverythingReport.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'PersonEverythingReport',
        'options': {
            'off': fmt,
            'of': of,
        },
    })


########## Repositories Report

for fmt in TEXT_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'RepositoriesReportOptions.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'Repositories Report Options',
        'options': {
            'off': fmt,
            'of': of,
        },
    })

for fmt in TEXT_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'RepositoriesReport.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'Repositories Report',
        'options': {
            'off': fmt,
            'of': of,
        },
    })


########## TodoReport

for fmt in TEXT_FMT:
    of = os.path.join(ADDONS_REP_DIR, 'TodoReport.' + fmt)
    addons.append({
        'title': 'Textual report "%%s" in format "%s"' % fmt,
        'result': of,
        'i': 'TodoReport',
        'options': {
            'off': fmt,
            'of': of,
            'tag': 'ToDo',
        },
    })


########## Check if addon exists in the addons listings

# reports=[]

for addon in addons:
    try:
        addon_id = next(l for l in listing if l['i'] == addon['i'])
    except:
        continue
    addon['title'] = addon['title'] % addon_id['n']
    addon['options'].update({
        'name': addon['i'],
    })
    addon.update({
        'type': 'Addon',
        'version': addon_id['v'],
    })
    reports.append(addon)
