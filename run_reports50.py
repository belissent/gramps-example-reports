# -*- coding: utf-8 -*-


import sys, os, subprocess, json

from report_set import *


CWD = os.path.dirname(__file__)
TOP_DIR = os.environ['GRAMPS_RESOURCES']
EXAMPLE_XML = os.path.join(TOP_DIR, "example", "gramps", "example.gramps")


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

# Generate reports

params = []
for report in reports:
    params += ["-a", "report", "-p",
        ",".join([
            (key + "=" + (str(value) if isinstance(value, (int, bool)) else value))
            for (key, value) in report['options'].items()
        ])
    ]
call([sys.executable, os.path.join(TOP_DIR, "Gramps.py"), "-q", "-i", EXAMPLE_XML] + params)


##################################################################
# Generate JSON data for the index page
##################################################################

# Get previous data
jfname = "report_list.json"
jdata = {}
if os.path.exists(jfname):
    jf = open(jfname, "r")
    jdata = json.load(jf)
jdata['gramps50'] = []

# Update with current data
for report in reports:
    jdata['gramps50'].append({
        "result": os.path.relpath(report['result'], CWD),
        "name": report['options']['name'],
        'title': report['title'],
        "version": "?",
        "status": (os.path.exists(report['result'])),
    })

# Export data
jf = open(jfname, "w")
json.dump(jdata, jf, indent=4)
