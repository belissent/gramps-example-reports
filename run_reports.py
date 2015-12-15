# -*- coding: utf-8 -*-
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2015 Pierre Bélissent
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA


import sys, os, subprocess, json, re
import cairosvg
from report_set import *


##################################################################
# Get Gramps target version as parameter
##################################################################

ULTIMATE_ANSWER = 42 # Arbitrary non-zero return code upon error
if len(sys.argv) != 2: sys.exit(ULTIMATE_ANSWER)
if sys.argv[1] not in ['40', '41', '42', '50']: sys.exit(ULTIMATE_ANSWER)
GRAMPS_TARGET_DIR = 'gramps' + sys.argv[1]

# sys.argv is reset for Gramps CLI code
del sys.argv[1:]


##################################################################
# Set paths
##################################################################

SITE_DIR = os.path.join(os.path.dirname(__file__), 'site')
TOP_DIR = os.environ['GRAMPS_RESOURCES']
EXAMPLE_XML = os.path.join(TOP_DIR, 'example', 'gramps', 'example.gramps')

sys.path.append(TOP_DIR)


##################################################################
# Check if the reports need to be regenerated
##################################################################

# The report is regenerated when the grampsXX_build.txt file changes

fname_build = os.path.join('site', GRAMPS_TARGET_DIR + '_build.txt')
last_fname_build = os.path.join('downloads', GRAMPS_TARGET_DIR + '_build.txt')
if not os.path.exists(fname_build):
    # Create the file
    fbuild = open(fname_build, 'r')
    fbuild.write('\n')
    fbuild.close()
if os.path.exists(last_fname_build):
    fbuild = open(fname_build, 'r')
    last_fbuild = open(last_fname_build, 'r')
    txt = fbuild.read()
    last_txt = last_fbuild.read()
    fbuild.close()
    last_fbuild.close()
    if txt == last_txt:
        # Same grampsXX_build.txt file contents
        print('No need to regenerate the reports for ' + GRAMPS_TARGET_DIR)
        sys.exit(0)


##################################################################
# Get the report set
##################################################################

reports = build_report_set()


##################################################################
# Function for calling Gramps and getting the results
##################################################################

def call(cmd):
    """
    :type cmd: list
    """
    print(' '.join(cmd))
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_str, err_str = process.communicate('')
    out_str = out_str.decode()
    err_str = err_str.decode()
    if out_str != '': print(out_str)
    if err_str != '': print(err_str, file = sys.stderr)
    print('The command exited with %s.' % str(process.returncode))
    log = '\n'.join([out_str, err_str])
    # Remove progress (lines with XX%) in the log
    log = re.sub(r'\d\d%\n', '', log)
    return(process.returncode, log)


##################################################################
# Create database
##################################################################

# Note: the database is created only once
# This allows to name the database, which is mandatory for some reports
(r, out) = call([sys.executable, os.path.join(TOP_DIR, 'Gramps.py'), '-q', '-y', '-C', 'example', '-i', EXAMPLE_XML])
if r != 0: sys.exit(ULTIMATE_ANSWER)


##################################################################
# Generate reports
##################################################################

# Split reports list in groups of 10 reports
CHUNK_SIZE = 10
chunks=[reports[x : x + CHUNK_SIZE] for x in range(0, len(reports), CHUNK_SIZE)]
# Update with current data
for chunk in chunks:
    params = []
    for report in chunk:
        params += ['-a', 'report', '-p',
            ','.join([
                (key + '=' + (str(value) if isinstance(value, (int, bool)) else value))
                for (key, value) in report['options'].items()
            ])
        ]
    (r, out) = call([sys.executable, os.path.join(TOP_DIR, 'Gramps.py'), '-q', '-y', '-O', 'example'] + params)
    # (r, out) = call([sys.executable, os.path.join(TOP_DIR, 'Gramps.py'), '-d', '', '-q', '-y', '-O', 'example'] + params)
    for report in chunk:
        report['log'] = out
    if r != 0: sys.exit(ULTIMATE_ANSWER)


##################################################################
# Generate HTML page for multi-files reports
##################################################################

def buildMultiFilesReport(report):
    (root, ext) = os.path.splitext(report['result'])
    if (not os.path.exists(root + '-2' + ext)):
        report['thumb'] = buildThumbnail(report['result'])
        return
    base = os.path.basename(root)
    dir = os.path.dirname(report['result'])
    to_root = os.path.relpath(SITE_DIR, dir)
    # Get list of report pages
    pages = []
    for fname in os.listdir(dir):
        (p_base, p_ext) = os.path.splitext(fname)
        mo = re.match(base + '(?:-([0-9]+))?$', p_base)
        if (p_ext == ext and mo):
            th = buildThumbnail(os.path.join(dir, fname))
            if mo.group(1): i = int(mo.group(1))
            else: i = 1
            pages.append({'name': fname, 'index': i, 'thumb': th})
    pages.sort(key = lambda x: x['index'])
    # Create HTML index for all the report pages
    report['result'] = root + ext + '.html'
    report['thumb'] = buildThumbnail(report['result'])
    html = open(report['result'], 'w')
    html.write("""
        <!DOCTYPE html>
        <html>

        <head>
        <meta charset='utf-8'>
        <meta name="description" content="GRAMPS reports examples">

        <link rel="stylesheet" type="text/css" media="screen" href="%s/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" type="text/css" media="screen" href="%s/bootstrap/css/bootstrap-theme.min.css">
        <link rel="stylesheet" type="text/css" media="screen" href="%s/main.css">

        <script language="javascript" charset="UTF-8" src="%s/jquery/jquery.min.js"></script>
        <script language="javascript" charset="UTF-8" src="%s/bootstrap/js/bootstrap.min.js"></script>


        <title>GRAMPS report: %s</title>
        </head>


        <body>
        <h1>%s</h1>
        <table>
    """ % tuple([to_root] * 5 + [report['title']] * 2))
    sep = ''
    for page in pages:
        html.write(sep)
        txt = page['name']
        if page['thumb']:
            txt = '<img src="%s" class="my_thumbnail">' % page['thumb']
            sep = ' '
        else:
            sep = '<br>'
        html.write('<a href="%s">%s</a></td>\n' % (page['name'], txt))
    html.write("""
        </table>
        </body>
        </html>
    """);
    html.close()


##################################################################
# Generate thumbnails for reports
##################################################################

def buildThumbnail(filename):
    (base, ext) = os.path.splitext(filename)
    if (ext == '.svg'):
        png = filename + '.png'
        if os.path.exists(filename):
            f = open(filename, 'r')
            fout = open(png, 'wb')
            cairosvg.svg2png(file_obj = f, write_to = fout, dpi = 19)
            f.close()
            fout.close()
        return(png)
    return(None)


##################################################################
# Generate JSON data for the index page
##################################################################

# Get previous data
flist_name = os.path.join('site', 'report_list.json')
jslist_name = os.path.join('site', 'report_list.js')
list_data = {}
if os.path.exists(flist_name):
    flist = open(flist_name, 'r')
    list_data = json.load(flist)
    flist.close()
if (GRAMPS_TARGET_DIR not in list_data): list_data[GRAMPS_TARGET_DIR] = []
list_data[GRAMPS_TARGET_DIR] = []

fvers_name = os.path.join('site', 'report_version.json')
jsvers_name = os.path.join('site', 'report_version.js')
vers_data = {}
if os.path.exists(fvers_name):
    fvers = open(fvers_name, 'r')
    vers_data = json.load(fvers)
    fvers.close()

for report in reports:
    vers_data[report['options']['name']] = report['version']
    buildMultiFilesReport(report)
    # check if reports is correctly generated
    status = os.path.exists(report['result'])
    if status and os.path.isfile(report['result']):
        sz = os.path.getsize(report['result'])
        if sz == 0: status = False
    # Append report data to index
    list_data[GRAMPS_TARGET_DIR].append({
        'result': os.path.relpath(report['result'], SITE_DIR),
        'name': report['name'],
        'id': report['options']['name'],
        'title': report['title'],
        'version': report['version'],
        'status': status,
        'log': '' if status else report['log'],
        'type': report['type'],
        'category': report['category'],
    })

# Export data
flist = open(flist_name, 'w')
json.dump(list_data, flist, indent=4, sort_keys=True)
flist.close()
jslist = open(jslist_name, 'w')
jslist.write('full_report_list = ')
json.dump(list_data, jslist, indent=4, sort_keys=True)
jslist.write(';')
jslist.close()

fvers = open(fvers_name, 'w')
json.dump(vers_data, fvers, indent=4, sort_keys=True)
fvers.close()
jsvers = open(jsvers_name, 'w')
jsvers.write('full_report_vers = ')
json.dump(vers_data, jsvers, indent=4, sort_keys=True)
jsvers.write(';')
jsvers.close()
