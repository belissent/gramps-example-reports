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

SITE_DIR = os.path.join(os.path.dirname(__file__), 'gh-pages')
TOP_DIR = os.environ['GRAMPS_RESOURCES']
EXAMPLE_XML = os.path.join(TOP_DIR, 'example', 'gramps', 'example.gramps')

sys.path.append(TOP_DIR)

if not os.path.isdir(GRAMPS_REP_DIR): os.makedirs(GRAMPS_REP_DIR)
if not os.path.isdir(ADDONS_REP_DIR): os.makedirs(ADDONS_REP_DIR)


##################################################################
# Save JS data
##################################################################

def save_jsdata(fname, jsdata, data_name):
    f = open(os.path.join(SITE_DIR, '%s.json' % fname), 'w')
    json.dump(jsdata, f, indent=4, sort_keys=True)
    f.close()
    js = open(os.path.join(SITE_DIR, '%s.js' % fname), 'w')
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
    if os.path.exists(os.path.join(SITE_DIR, '%s.json' % fname)):
        f = open(os.path.join(SITE_DIR, '%s.json' % fname), 'r')
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

if GRAMPS_TARGET_DIR not in build_data: build_data[GRAMPS_TARGET_DIR] = {}
build_data_tgt = build_data[GRAMPS_TARGET_DIR]
if ('gramps-example-reports/master' not in build_data_tgt): build_data_tgt['gramps-example-reports/master'] = ""
if ('gramps/' + GRAMPS_TARGET_DIR not in build_data_tgt): build_data_tgt['gramps/' + GRAMPS_TARGET_DIR] = ""
if ('addons/master' not in build_data_tgt): build_data_tgt['addons/master'] = ""

native_rebuild = (sha_examples != build_data_tgt['gramps-example-reports/master']) or (sha_gramps != build_data_tgt['gramps/' + GRAMPS_TARGET_DIR])
if (sha_addons == build_data_tgt['addons/master']) and not native_rebuild:
    print('No need to regenerate the reports for ' + GRAMPS_TARGET_DIR)
    sys.exit(0)
build_data_tgt['gramps-example-reports/master'] = sha_examples
build_data_tgt['gramps/' + GRAMPS_TARGET_DIR] = sha_gramps
build_data_tgt['addons/master'] = sha_addons
build_data_tgt['user'] = re.sub('/.*', '', os.environ['EXAMPLES_REPO_SLUG'])
build_data_tgt['travis_build_id'] = os.environ['TRAVIS_BUILD_ID']
build_data_tgt['travis_build_number'] = os.environ['TRAVIS_BUILD_NUMBER']


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
    log = ' '.join(cmd)
    print(log)
    retcode = ULTIMATE_ANSWER
    t0 = time.time()
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for i in range (5 * 60 * 10): # 5 minutes timeout
        time.sleep(0.1)
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
        s = 'Error: process taking too long to complete (%.0f seconds), terminating' % (t1 - t0)
        print(s)
        log += '\n' + s
    else:
        out_str, err_str = process.communicate('')
        out_str = out_str.decode()
        err_str = err_str.decode()
        if out_str != '': print(out_str)
        if err_str != '': print(err_str, file = sys.stderr)
        s = 'The command exited with %s (execution time: %.0f seconds).' % (str(process.returncode), t1 - t0)
        print(s)
        log = '\n'.join([log, out_str, err_str, s])
        # Remove progress (lines with XX%) in the log
        log = re.sub(r'100%\r', r'100%\n', log)
        log = re.sub(r'\d\d%\r', '', log)
        retcode = process.returncode
    return(retcode, log, t1 - t0)


##################################################################
# Create database
##################################################################

# Note: the database is created only once
# This allows to name the database, which is mandatory for some reports
(r, out, dt) = call([sys.executable, os.path.join(TOP_DIR, 'Gramps.py'), '-q', '-y', '-C', 'example', '-i', EXAMPLE_XML])
if r != 0: sys.exit(ULTIMATE_ANSWER)


##################################################################
# Generate reports
##################################################################

def clean_report(respath):
    # Clean a rport results
    # Deletes:
    #  - the result file
    #  - the result file parent and grand-parent directories if used only for this report
    respath = os.path.normpath(os.path.abspath(respath))
    if os.path.exists(respath):
        subprocess.check_output('rm -rf %s' % respath, shell = True)
    for resdir in (
        os.path.dirname(respath),
        os.path.dirname(os.path.dirname(respath)),
    ):
        if os.path.exists(resdir):
            reports_with_same_parent_directory = [
                r for r in reports if
                os.path.commonprefix([resdir, os.path.dirname(os.path.normpath(os.path.abspath(r['result'])))]) == resdir
            ]
            if len(reports_with_same_parent_directory) == 1:
                subprocess.check_output('rm -rf %s' % resdir, shell = True)


if GRAMPS_TARGET_DIR not in vers_data: vers_data[GRAMPS_TARGET_DIR] = {}
for report in reports:
    # Check if report is to be rebuilt
    v = ""
    id = report['options']['name']
    if id in vers_data[GRAMPS_TARGET_DIR]: v = vers_data[GRAMPS_TARGET_DIR][id]
    report['rebuilt'] = native_rebuild or ((report['type'] == 'Addon') and (report['version'] != v))
    if not report['rebuilt']:
        print('No need to regenerate the report \"\", for %s' % (report['title'], GRAMPS_TARGET_DIR))
        continue
    else:
        vers_data[GRAMPS_TARGET_DIR][id] = report['version']
        # Clean previous report results
        clean_report(report['result'])
        # Build parameters string
        params = ['-a', 'report', '-p',
            ','.join([
                (key + '=' + (str(value) if isinstance(value, (int, bool)) else value))
                for (key, value) in report['options'].items()
            ])
        ]
        # Create result directory if needed
        resdir = os.path.dirname(os.path.normpath(os.path.abspath(report['result'])))
        if not os.path.isdir(resdir): os.makedirs(resdir)
        (r, out, dt) = call([sys.executable, os.path.join(TOP_DIR, 'Gramps.py'), '-q', '-y', '-O', 'example'] + params)
        report['log'] = out
        report['status'] = (r == 0)
        report['time'] = dt


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

# Clean the old reports that are not in the list anymore
for old_repdata in old_list_data:
    respath = os.path.normpath(os.path.abspath(os.path.join(SITE_DIR, old_repdata['result'])))
    reports_with_same_respath = [
        r for r in reports
        if respath == os.path.normpath(os.path.abspath(r['result']))
    ]
    if len(reports_with_same_respath) == 0:
        clean_report(respath)


list_data[GRAMPS_TARGET_DIR] = []
for report in reports:
    result_path = os.path.relpath(report['result'], SITE_DIR)
    # Get previous data if report is not rebuilt
    if not report['rebuilt']:
        list_data[GRAMPS_TARGET_DIR].extend([r for r in old_list_data if r['result'] == result_path])
        continue
    # Manage multi-files reports (SVG format for example)
    buildMultiFilesReport(report)
    # check if reports is correctly generated
    status = report['status'] and os.path.exists(report['result'])
    if status and os.path.isfile(report['result']):
        sz = os.path.getsize(report['result'])
        if sz == 0: status = False
    # Append report data to index
    list_data[GRAMPS_TARGET_DIR].append({
        'title': report['title'],
        'name': report['name'],
        'result': result_path,
        'type': report['type'],
        'category': standalone_categories[report['category']][1],
        'version': report['version'],
        'id': report['options']['name'],
        'status': status,
        'log': report['log'],
        'time': '%.1f' % report['time'],
        'format': report['options']['off'] if 'off' in report['options'] else '',
        'commit_gramps': sha_gramps,
        'commit_addons': sha_addons,
        'commit_examples': sha_examples,
        'travis_build_id': build_data_tgt['travis_build_id'],
        'travis_build_number': build_data_tgt['travis_build_number'],
    })

# Export data
save_jsdata(flist_name, list_data, 'full_report_list')
save_jsdata(fvers_name, vers_data, 'full_report_vers')
save_jsdata(fbuild_name, build_data, 'builds')
