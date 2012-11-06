#!/usr/bin/env python3

import urllib.request
import json
import os
import time
import locale
from datetime import date, timedelta, datetime

locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

print('Lade Anträge...')
u = urllib.request.urlopen('https://redmine.piratenpartei-mv.de/projects/lpt/issues.json?limit=1000').read()
issues = json.loads(u.decode('utf-8'))

# write date of update
f = open('openslides.csv', 'w+')

f.write('''"Number","Title","Text","Reason","Submitter (First Name)","Submitter (Last Name)"\n''')
for issue in issues['issues']:
    f.write("\"" + str(issue['id']) + "\",\"" + issue['subject'] + "\",\"" + issue['custom_fields'][1]['value'] + "\",\"\",\"" + issue['custom_fields'][0]['value'].split()[0] + "\",\"" + issue['custom_fields'][0]['value'].split()[1].replace(",", "") + "\"\n")

f.close()
