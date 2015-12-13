# -*- coding: utf-8 -*-


import sys, os, subprocess, json, re
import cairosvg

from report_set import *


CWD = os.path.dirname(__file__)
if CWD == '': CWD = '.'
TOP_DIR = os.environ['GRAMPS_RESOURCES']
EXAMPLE_XML = os.path.join(TOP_DIR, "example", "gramps", "example.gramps")

sys.path.append(TOP_DIR)

def call(cmd):
    """
    :type cmd: list
    """
    print(" ".join(cmd))
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result_str, err_str = process.communicate("")
    result_str = result_str.decode()
    err_str = err_str.decode()
    print(result_str)
    print(sys.stderr, err_str)

##################################################################
# Create database
##################################################################

# Note: the database is created only once
# This allows to name the database, which is mandatory for some reports
call([sys.executable, os.path.join(TOP_DIR, "Gramps.py"), "-q", "-y", "-C", "example", "-i", EXAMPLE_XML])


##################################################################
# Generate reports
##################################################################

params = []
for report in reports:
    params += ["-a", "report", "-p",
        ",".join([
            (key + "=" + (str(value) if isinstance(value, (int, bool)) else value))
            for (key, value) in report['options'].items()
        ])
    ]
call([sys.executable, os.path.join(TOP_DIR, "Gramps.py"), "-q", "-O", "example"] + params)


##################################################################
# Generate HTML page for multi-files reports
##################################################################

def buildMultiFilesReport(report):
    (root, ext) = os.path.splitext(report['result'])
    if (not os.path.exists(root + "-2" + ext)):
        report['thumb'] = buildThumbnail(report['result'])
        return
    base = os.path.basename(root)
    dir = os.path.dirname(report['result'])
    to_root = os.path.relpath(CWD, dir)
    # Get list of report pages
    pages = []
    for fname in os.listdir(dir):
        (p_base, p_ext) = os.path.splitext(fname)
        mo = re.match(base + "(?:-([0-9]+))?$", p_base)
        if (p_ext == ext and mo):
            th = buildThumbnail(os.path.join(dir, fname))
            if mo.group(1): i = int(mo.group(1))
            else: i = 1
            pages.append({'name': fname, 'index': i, 'thumb': th})
    pages.sort(key = lambda x: x['index'])
    # Create HTML index for all the report pages
    report['result'] = root + ext + ".html"
    report['thumb'] = buildThumbnail(report['result'])
    html = open(report['result'], "w")
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
flist_name = "report_list.json"
jslist_name = "report_list.js"
list_data = {}
if os.path.exists(flist_name):
    flist = open(flist_name, "r")
    list_data = json.load(flist)
    flist.close()
if ('gramps50' not in list_data): list_data['gramps50'] = []
list_data['gramps50'] = []

fvers_name = "report_version.json"
jsvers_name = "report_version.js"
vers_data = {}
if os.path.exists(fvers_name):
    fvers = open(fvers_name, "r")
    vers_data = json.load(fvers)
    fvers.close()

# Update with current data
for report in reports:
    vers_data[report['options']['name']] = report['version']
    buildMultiFilesReport(report)
    list_data['gramps50'].append({
        'result': os.path.relpath(report['result'], CWD),
        'name': report['options']['name'],
        'title': report['title'],
        'version': report['version'],
        'status': (os.path.exists(report['result'])),
        'type': report['type'],
    })

# Export data
flist = open(flist_name, "w")
json.dump(list_data, flist, indent=4, sort_keys=True)
flist.close()
jslist = open(jslist_name, "w")
jslist.write("full_report_list = ")
json.dump(list_data, jslist, indent=4, sort_keys=True)
jslist.write(";")
jslist.close()

fvers = open(fvers_name, "w")
json.dump(vers_data, fvers, indent=4, sort_keys=True)
fvers.close()
jsvers = open(jsvers_name, "w")
jsvers.write("full_report_vers = ")
json.dump(vers_data, jsvers, indent=4, sort_keys=True)
jsvers.write(";")
jsvers.close()
