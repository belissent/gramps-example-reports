# -*- coding: utf-8 -*-

#
# Report test sets for GRAMPS: Generate every report in every format.
#


import os


reports = []

##################################################################
# GRAMPS native plugins
##################################################################

GRAMPS_REP_DIR = os.path.join(os.environ['GRAMPS_REPORTS'], "gramps")

GRPH_FMT = ["sxw", "ps", "pdf", "svg"]
TEXT_FMT = ["sxw", "ps", "pdf", "kwd", "abw", "rtf", "txt", "html", "tex"]

GRPH_REP = ["ancestor_chart", "descend_chart", "fan_chart", "statistics_chart", "timeline", "calendar"]
TEXT_REP = ["ancestor_report", "descend_report", "det_ancestor_report", "det_descendant_report", "family_group"]


# Single run with all graphical reports in all formats
for report in GRPH_REP:
    for fmt in GRPH_FMT:
        of = os.path.join(GRAMPS_REP_DIR, report + '.' + fmt)
        reports.append({
            'title': "Graphical report \"%s\" in format \"%s\")" % (report, fmt),
            'result': of,
            'options': {
                'name': report,
                'id': "I0044",
                'pid': "I0044",
                'off': fmt,
                'of': of,
                'maxgen': 10,
            }
        })

# Single run with all textual reports in all formats
for report in TEXT_REP:
    for fmt in TEXT_FMT:
        of = os.path.join(GRAMPS_REP_DIR, report + '.' + fmt)
        reports.append({
            'title': "Textual report \"%s\" in format \"%s\")" % (report, fmt),
            'result': of,
            'options': {
                'name': report,
                'id': "I0044",
                'pid': "I0044",
                'off': fmt,
                'of': of,
                'maxgen': 10,
            }
        })

##################################################################
# GRAMPS addons reports
##################################################################

#TODO
