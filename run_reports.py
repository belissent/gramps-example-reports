# -*- coding: utf-8 -*-
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2015 Pierre Bélissent
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA


import sys, os, subprocess, json, re, time, shutil
import cairosvg
from report_set import *
from gramps.gen.plug.report import standalone_categories


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

if not os.path.isdir(GRAMPS_REP_DIR): os.makedirs(GRAMPS_REP_DIR)
if not os.path.isdir(ADDONS_REP_DIR): os.makedirs(ADDONS_REP_DIR)


##################################################################
# Save JS data
##################################################################

def save_jsdata(fname, jsdata, data_name):
    f = open('site/%s.json' % fname, 'w')
    json.dump(jsdata, f, indent=4, sort_keys=True)
    f.close()
    js = open('site/%s.js' % fname, 'w')
    js.write('%s = ' % data_name)
    json.dump(jsdata, js, indent=4, sort_keys=True)
    js.write(';')
    js.close()


##################################################################
### Read the last generated data
##################################################################

def read_jsdata(fname):
    # Load JSON data
    jsdata = {}
    if os.path.exists('site/%s.json' % fname):
        f = open('site/%s.json' % fname, 'r')
        jsdata = json.load(f)
        f.close()
    return jsdata


##################################################################
# Get previously generated data
##################################################################

# Get previous data
flist_name = 'report_list'
fvers_name = 'report_version'
fbuild_name = 'report_build'

list_data = read_jsdata(flist_name)
vers_data = read_jsdata(fvers_name)
build_data = read_jsdata(fbuild_name)


##################################################################
# Check if the reports need to be regenerated
##################################################################

# The report is regenerated when the
# - gramps-example-reports repository changes
# - gramps repository (for the current branch) changes
# - the addon version changes (for addons only)

sha_examples = subprocess.check_output('git rev-parse HEAD', shell = True).decode().strip()
sha_gramps = subprocess.check_output('git rev-parse HEAD', cwd = os.environ['GRAMPS_RESOURCES'], shell = True).decode().strip()
sha_addons = subprocess.check_output('git rev-parse HEAD', cwd = 'sources/addons', shell = True).decode().strip()

if ('gramps-example-reports/master' not in build_data): build_data['gramps-example-reports/master'] = ""
if ('gramps/' + GRAMPS_TARGET_DIR not in build_data): build_data['gramps/' + GRAMPS_TARGET_DIR] = ""
if ('addons/master' not in build_data): build_data['addons/master'] = ""

native_rebuild = (sha_examples == build_data['gramps-example-reports/master']) and (sha_gramps == build_data['gramps/' + GRAMPS_TARGET_DIR])
if (sha_addons == build_data['addons/master']) and not native_rebuild:
    print('No need to regenerate the reports for ' + GRAMPS_TARGET_DIR)
    sys.exit(0)
build_data['gramps-example-reports/master'] = sha_examples
build_data['gramps/' + GRAMPS_TARGET_DIR] = sha_gramps
build_data['addons/master'] = sha_addons


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
    retcode = ULTIMATE_ANSWER
    t0 = time.time()
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for i in range (5 * 60): # 5 minutes timeout
        time.sleep(1.0)
        if process.poll() is not None: break
    t1 = time.time()
    if process.poll() is None:
        # Timeout reached
        try:
            process.kill()
        except OSError as e:
            # Subprocess process may terminate between the process.poll() and process.kill() calls
            if e.errno != errno.ESRCH:
                raise
        log = 'Error: process taking too long to complete (%.0f seconds), terminating' % (t1 - t0)
        print(log)
    else:
        out_str, err_str = process.communicate('')
        out_str = out_str.decode()
        err_str = err_str.decode()
        if out_str != '': print(out_str)
        if err_str != '': print(err_str, file = sys.stderr)
        print('The command exited with %s (execution time: %.0f seconds).' % (str(process.returncode), t1 - t0))
        log = '\n'.join([out_str, err_str])
        # Remove progress (lines with XX%) in the log
        log = re.sub(r'100%\r', r'100%\n', log)
        log = re.sub(r'\d\d%\r', '', log)
        retcode = process.returncode
    return(retcode, log)


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

if GRAMPS_TARGET_DIR not in vers_data: vers_data[GRAMPS_TARGET_DIR] = {}
for report in reports:
    # Check if report is to be rebuilt
    v = ""
    id = report['options']['name']
    if id in vers_data[GRAMPS_TARGET_DIR]: v = vers_data[GRAMPS_TARGET_DIR][id]
    report['rebuilt'] = native_rebuild or ((report['type'] == 'Addon') and (report['version'] != v))
    if not report['rebuilt']: continue
    else:
        vers_data[GRAMPS_TARGET_DIR][id] = report['version']
        # Build parameters string
        params = ['-a', 'report', '-p',
            ','.join([
                (key + '=' + (str(value) if isinstance(value, (int, bool)) else value))
                for (key, value) in report['options'].items()
            ])
        ]
        # Create result directory if needed
        resdir = os.path.dirname(report['result'])
        if not os.path.isdir(resdir): os.makedirs(resdir)
        (r, out) = call([sys.executable, os.path.join(TOP_DIR, 'Gramps.py'), '-q', '-y', '-O', 'example'] + params)
        report['log'] = out
        report['status'] = (r == 0)


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

old_list_data = []
if GRAMPS_TARGET_DIR in list_data: old_list_data = list_data[GRAMPS_TARGET_DIR]
list_data[GRAMPS_TARGET_DIR] = []
for report in reports:
    if not report['rebuilt']:
        list_data[GRAMPS_TARGET_DIR].extend([r for r in old_list_data if r['title'] == report['title']])
        continue
    buildMultiFilesReport(report)
    # check if reports is correctly generated
    status = report['status'] and os.path.exists(report['result'])
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
        'log': report['log'],
        'type': report['type'],
        'category': standalone_categories[report['category']][1],
        'format': report['options']['off'] if 'off' in report['options'] else '',
    })

# Export data
save_jsdata(flist_name, list_data, 'full_report_list')
save_jsdata(fvers_name, vers_data, 'full_report_vers')
save_jsdata(fbuild_name, build_data, 'builds')
