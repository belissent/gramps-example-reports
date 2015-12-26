# -*- coding: utf-8 -*-
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2015 Pierre Bélissent
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

#
# Report test sets for GRAMPS: Generate every report in every format.
#


import os

from gramps.version import VERSION
from gramps.plugins.webreport.narrativeweb import _INCLUDE_LIVING_VALUE
from gramps.gen.plug import PluginRegister, BasePluginManager
from gramps.gen.dbstate import DbState
from gramps.cli.grampscli import CLIManager
from gramps.gen.proxy import LivingProxyDb
from gramps.gen.lib.date import Today

GRAMPS_REP_DIR = os.path.normpath(os.path.abspath(os.path.join(os.environ['GRAMPS_REPORTS'], 'gramps')))
ADDONS_REP_DIR = os.path.normpath(os.path.abspath(os.path.join(os.environ['GRAMPS_REPORTS'], 'addons')))

import report_set_DynamicWeb

def build_report_set():

    reports = []

    ##################################################################
    # Load plugins
    ##################################################################

    dbstate = DbState()
    climanager = CLIManager(dbstate, setloader = True, user = None)
    climanager.do_reg_plugins(dbstate, uistate = None)
    gpr = PluginRegister.get_instance()

    PLUGMAN = BasePluginManager.get_instance()
    CSS = PLUGMAN.process_plugin_data('WEBSTUFF')

    ##################################################################
    # GRAMPS native plugins
    ##################################################################

    # GRPH_FMT = ['odt', 'ps', 'pdf', 'svg']
    GRPH_FMT = ['pdf', 'svg']
    # GRPH_FMT = ['svg']
    GRPH_REP = [
        {
            'report': 'ancestor_chart',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
                'pid': 'I0006',
            },
        },
        {
            'report': 'descend_chart',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
                'pid': 'I0104',
            },
        },
        {
            'report': 'family_descend_chart',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
                'pid': 'I0104',
            },
        },
        {
            'report': 'fan_chart',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
                'pid': 'I0006',
            },
        },
        {
            'report': 'statistics_chart',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
           },
        },
        {
            'report': 'timeline',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
            },
        },
        {
            'report': 'calendar',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
            },
        },
        {
            'report': 'familylines_graph',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
                'gidlist': 'I0104 I0045',
                'limitchildren': True,
                'maxchildren': 20,
            },
        },
        {
            'report': 'hourglass_graph',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
                'pid': 'I0044',
                'maxascend': 2,
                'maxdescend': 2,
            },
        },
        {
            'report': 'rel_graph',
            'options': {
                'scale_tree': 2,
                'maxgen': 6,
                'pid': 'I0044',
                'filter': 3,
                'event_choice': 2,
            },
        },
    ]

    # TEXT_FMT = ['ps', 'pdf', 'html', 'odt', 'tex', 'rtf', 'txt']
    TEXT_FMT = ['html', 'pdf', 'txt']
    # TEXT_FMT = ['html', 'txt']
    TEXT_REP = [
        {
            'report': 'ancestor_report',
            'options': {
                'maxgen': 6,
                'pid': 'I0006',
            },
        },
        {
            'report': 'descend_report',
            'options': {
                'pid': 'I0104',
            },
        },
        {
            'report': 'det_ancestor_report',
            'options': {
                'pid': 'I0006',
            },
        },
        {
            'report': 'det_descendant_report',
            'options': {
                'pid': 'I0104',
            },
        },
        {
            'report': 'family_group',
            'options': {
                'family_id': 'F0017',
            },
        },
        {
            'report': 'birthday_report',
            'options': {},
        },
        {
            'report': 'endofline_report',
            'options': {
                'pid': 'I0006',
            },
        },
        {
            'report': 'indiv_complete',
            'options': {},
        },
        {
            'report': 'kinship_report',
            'options': {
                'pid': 'I0044',
            },
        },
        {
            'report': 'tag_report',
            'options': {
                'tag': 'ToDo',
            },
        },
        {
            'report': 'number_of_ancestors',
            'options': {
                'pid': 'I0006',
            },
        },
        {
            'report': 'place_report',
            'options': {
                'places': 'P1678 P1679 P1680',
            },
        },
        {
            'report': 'summary',
            'options': {},
        },
        {
            'report': 'records',
            'options': {},
        },
        {
            'report': 'notelinkreport',
            'options': {},
        },
    ]


    # Single run with all native reports (except web) in all formats
    for (rep_list, formats) in [
        (TEXT_REP, TEXT_FMT),
        (GRPH_REP, GRPH_FMT),
    ]:
        for rep_info in TEXT_REP:
            report = rep_info['report']
            options = rep_info['options']
            plugin = gpr.get_plugin(report)
            if not plugin:
                print('Unknown plugin: %s' % report)
                continue
            for fmt in TEXT_FMT:
                of = os.path.join(GRAMPS_REP_DIR, report + '.' + fmt)
                new_options = {
                    'name': report,
                    'off': fmt,
                    'of': of,
                    # 'show': 'all',
                }
                new_options.update(options)
                reports.append({
                    'title': '"%s" in format "%s"' % (plugin.name, fmt),
                    'name': plugin.name,
                    'result': of,
                    'type': 'Native',
                    'category': plugin.category,
                    'version': plugin.version,
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

    for (i, (css, full)) in enumerate([
        ['default', False],
        ['Mainz', True],
    ]):
        report = 'navwebpage'
        plugin = gpr.get_plugin(report)
        opts = {
            'name': report,
            'target': os.path.join(GRAMPS_REP_DIR, 'example_NAVWEB%i' % i),
            'css':  CSS[css]['id'],
            'living': _INCLUDE_LIVING_VALUE,
        }
        if (full): opts.update(full_options)
        reports.append({
            'title': '"%s" report example %i' % (plugin.name, i),
            'name': report,
            'result': os.path.join(GRAMPS_REP_DIR, 'example_NAVWEB%i' % i, 'index.html'),
            'type': 'Native',
            'category': plugin.category,
            'version': VERSION,
            'options': opts,
        })


    full_options = {
        'alive': False,
        'fullyear': True,
        'makeoneday': True,
        'link_to_narweb': True,
    }

    for (i, (css, full)) in enumerate([
        ['default', False],
        ['Mainz', True],
    ]):
        report = 'WebCal'
        plugin = gpr.get_plugin(report)
        opts = {
            'name': report,
            'target': os.path.join(GRAMPS_REP_DIR, 'example_WebCal%i' % i),
            'css':  CSS[css]['id'],
            'home_link': '../../example_NAVWEB%i/index.html' % i,
            'prefix': '../../example_NAVWEB%i/' % i,
        }
        page = 'January.html'
        if (full):
            opts.update(full_options)
            page = 'fullyearlinked.html'
        reports.append({
            'title': '"%s" report example %i' % (plugin.name, i),
            'name': report,
            'result': os.path.join(GRAMPS_REP_DIR, 'example_WebCal%i' % i, str(Today().get_year()), page),
            'type': 'Native',
            'category': plugin.category,
            'version': VERSION,
            'options': opts,
        })


    ##################################################################
    # GRAMPS addons reports
    ##################################################################


    addons=[]


    ########## AncestorFill

    for fmt in TEXT_FMT:
        of = os.path.join(ADDONS_REP_DIR, 'AncestorFill.' + fmt)
        addons.append({
            'title': '"%%s" in format "%s"' % fmt,
            'result': of,
            'i': 'AncestorFill',
            'options': {
                'off': fmt,
                'of': of,
            },
        })


    ########## d3-ancestralcollapsibletree

    addons.append({
        'title': '"%s" report example',
        'result': os.path.join(ADDONS_REP_DIR, 'd3-ancestralcollapsibletree', 'index.html'),
        'i': 'd3-ancestralcollapsibletree',
        'options': {
            'dest_path': os.path.join(ADDONS_REP_DIR, 'd3-ancestralcollapsibletree'),
            'dest_file': 'index.html',
            'pid': 'I0006',
            'maxgen': 6,
        },
    })


    ########## d3-ancestralfanchart

    addons.append({
        'title': '"%s" report example',
        'result': os.path.join(ADDONS_REP_DIR, 'd3-ancestralfanchart', 'index.html'),
        'i': 'd3-ancestralfanchart',
        'options': {
            'dest_path': os.path.join(ADDONS_REP_DIR, 'd3-ancestralfanchart'),
            'dest_file': 'index.html',
            'pid': 'I0006',
            'maxgen': 6,
        },
    })


    ########## d3-descendantindentedtree

    addons.append({
        'title': '"%s" report example',
        'result': os.path.join(ADDONS_REP_DIR, 'd3-descendantindentedtree', 'index.html'),
        'i': 'd3-descendantindentedtree',
        'options': {
            'dest_path': os.path.join(ADDONS_REP_DIR, 'd3-descendantindentedtree'),
            'dest_file': 'index.html',
            'pid': 'I0104',
            'max_gen': 6,
            'inc_private': True,
            'inc_living': _INCLUDE_LIVING_VALUE,
        },
    })


    ########## denominoviso

    for (i, (mode, type, dir, pid, full)) in enumerate([
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
            'title': '"%%s" in format "%s"' % fmt,
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
            'title': '"%%s" in format "%s"' % fmt,
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
            'title': '"%%s" in format "%s"' % fmt,
            'result': of,
            'i': 'Descendants Lines',
            'options': {
                'off': fmt,
                'of': of,
                'pid': 'I0006',
            },
        })


    ########## database-differences-report

    for fmt in ['html']:
        of = os.path.join(ADDONS_REP_DIR, 'database-differences-report.' + fmt)
        addons.append({
            'title': '"%%s" in format "%s"' % fmt,
            'result': of,
            'i': 'database-differences-report',
            'options': {
                'off': fmt,
                'of': of,
                'filename': os.path.join(os.environ['GRAMPS_RESOURCES'], 'example', 'gramps', 'example.gramps'),
            },
        })


    ########## DynamicWeb

    addons.extend(report_set_DynamicWeb.addon_set())


    ########## FamilyTree

    for fmt in GRPH_FMT:
        of = os.path.join(ADDONS_REP_DIR, 'FamilyTree.' + fmt)
        addons.append({
            'title': '"%%s" in format "%s"' % fmt,
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

    for fmt in ['html']:
        of = os.path.join(ADDONS_REP_DIR, 'LastChangeReport.' + fmt)
        addons.append({
            'title': '"%%s" in format "%s"' % fmt,
            'result': of,
            'i': 'LastChangeReport',
            'options': {
                'off': fmt,
                'of': of,
                'what_types': '"True,True,True,True,True,True"'
            },
        })


    ########## LinesOfDescendency

    for fmt in ['html']:
        of = os.path.join(ADDONS_REP_DIR, 'LinesOfDescendency.' + fmt)
        addons.append({
            'title': '"%%s" in format "%s"' % fmt,
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
            'title': '"%%s" in format "%s"' % fmt,
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
            'title': '"%%s" in format "%s"' % fmt,
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
            'title': '"%%s" in format "%s"' % fmt,
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
            'title': '"%%s" in format "%s"' % fmt,
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
            'title': '"%%s" in format "%s"' % fmt,
            'result': of,
            'i': 'Repositories Report',
            'options': {
                'off': fmt,
                'of': of,
            },
        })


    ########## TodoReport

    reports=[]
    addons=[]
    for fmt in TEXT_FMT:
        of = os.path.join(ADDONS_REP_DIR, 'TodoReport.' + fmt)
        addons.append({
            'title': '"%%s" in format "%s"' % fmt,
            'result': of,
            'i': 'TodoReport',
            'options': {
                'off': fmt,
                'of': of,
                'tag': 'ToDo',
            },
        })


    ########## Check if addon exists in the addons listings

    for addon in addons:
        plugin = gpr.get_plugin(addon['i'])
        if not plugin:
            print('Unknown plugin: %s' % addon['i'])
            continue
        addon['options'].update({
            'name': addon['i'],
        })
        addon.update({
            'title': addon['title'] % plugin.name,
            'name': plugin.name,
            'type': 'Addon',
            'category': plugin.category,
            'version': plugin.version,
        })
        del addon['i']
        reports.append(addon)

    return reports
