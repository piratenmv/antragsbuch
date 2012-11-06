#!/usr/bin/env python3

import urllib.request
import json
import os
import time
import locale
from datetime import date, timedelta, datetime

locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

def antragslink(id):
    return '\\hyperref[chap:' + str(id) + ']{Antrag ' + str(id) + '}'

def niceliste(list):
    if len(list) == 1:
        return list[0]
    if len(list) == 2:
        return " und ".join(list)
    if len(list) > 2:
        return ", ".join(list[0:-1]) + " und " + list[-1]

print('Lade Anträge...')
u = urllib.request.urlopen('https://redmine.piratenpartei-mv.de/projects/lpt/issues.json?limit=1000').read()
issues = json.loads(u.decode('utf-8'))

print('Schreibe Latex-Dateien...')

# write date of update
f = open('all-meta.tex', 'w+')
z = time.strftime("%-d. %B %Y, %-H:%M Uhr", time.localtime())
f.write("\\newcommand{\\LPTupdate}{" + z + "}")
f.close()

for issue in issues['issues']:
    print('Antrag', issue['id'])

    # write issue to textile file
    f = open(str(issue['id']) + '.textile', 'w+')
    f.write(issue['description'])
    f.close()

    # fix blockquotes
    cmd = "gsed -i 's|^> |bq. |g' " + str(issue['id']) + '.textile'
    os.system(cmd)

    # translate from textile to latex
    cmd = 'pandoc ' + str(issue['id']) + '.textile -f textile -o ' + str(issue['id']) + '.tex -t latex --reference-links --normalize --smart --no-wrap'
    os.system(cmd)

    # fix stuff that is accidentially taken as strikethrough and replaced by \sout{}
    cmd = "gsed -i 's|\\\\sout{\([^}]*\)}|-\\1-|' " + str(issue['id']) + '.tex'
    os.system(cmd)

    # remove "bq." remainders
    cmd = "gsed -i 's/\\\\\\\\bq. /\\n/g' " + str(issue['id']) + '.tex'
    os.system(cmd)

    # replace ".h2" remainders
    cmd = "gsed -i 's|h2\\. \(.*\)$|\\\\minisec{\\1}|g' " + str(issue['id']) + '.tex'
    os.system(cmd)

    # put named links into footnotes
    cmd = "gsed -i 's|\\\\href{\\([^}]*\\))}{\\([^}]*\\)}|\\2\\\\footnote{\\\\url{\\1}})|g' " + str(issue['id']) + '.tex'
    os.system(cmd)
    cmd = "gsed -i 's|\\\\href{\\([^}]*\\):}{\\([^}]*\\)}|\\2\\\\footnote{\\\\url{\\1}}:|g' " + str(issue['id']) + '.tex'
    os.system(cmd)
    cmd = "gsed -i 's|\\\\href{\\([^}]*\\)}{\\([^}]*\\)}|\\2\\\\footnote{\\\\url{\\1}}|g' " + str(issue['id']) + '.tex'
    os.system(cmd)


    # put metadata into extra file
    f = open(str(issue['id']) + '-meta.tex', 'w+')
    f.write('\\renewcommand{\\LPTantragsteller}{' + issue['custom_fields'][0]['value'] + '}\n')

    # exclamation marks in title break the index generation
    f.write('\\renewcommand{\\LPTtitel}{' + issue['subject'].replace("!", "") + '}\n\n')

    # get related tickets
    u = urllib.request.urlopen('https://redmine.piratenpartei-mv.de/issues/' + str(issue['id']) + '.json?include=relations').read()
    related = json.loads(u.decode('utf-8'))
    relations_list = list()
    relations_latex = ""
    if 'relations' in related['issue']:
        relations_konkurrierend = list()
        relations_voraussetzung = list()
        relations_vorausgesetzt = list()
        for relation in related['issue']['relations']:
            if relation['issue_to_id'] == issue['id']:
                if relation['relation_type'] == 'relates':
                    relations_konkurrierend.append(antragslink(relation['issue_id']))
                    relations_list.append('konkurrierend zu ' + antragslink(relation['issue_id']))
                if relation['relation_type'] == 'blocks':
                    relations_list.append('setzt Annahme von ' + antragslink(relation['issue_id']) + ' voraus')
                    relations_vorausgesetzt.append(antragslink(relation['issue_id']))
            else:
                if relation['relation_type'] == 'relates':
                    relations_konkurrierend.append(antragslink(relation['issue_to_id']))
                    relations_list.append('konkurrierend zu ' + antragslink(relation['issue_to_id']))
                if relation['relation_type'] == 'blocks':
                    relations_list.append('Voraussetzung für ' + antragslink(relation['issue_to_id']))
                    relations_voraussetzung.append(antragslink(relation['issue_to_id']))
                    
        relations_texts = list()
        if len(relations_vorausgesetzt) != 0:
            relations_texts.append("setzt Annahme von " + niceliste(relations_vorausgesetzt) + " voraus")
        if len(relations_voraussetzung) != 0:
            relations_texts.append("Voraussetzung für " + niceliste(relations_voraussetzung))
        if len(relations_konkurrierend) != 0:
            relations_texts.append("konkurrierend zu " + niceliste(relations_konkurrierend))

        f.write('\\setboolean{LPTrelated}{true}\n')
        f.write('\\renewcommand{\\LPTrelations}{' + ", ".join(relations_texts) + '}\n')    
    else:
        f.write('\\setboolean{LPTrelated}{false}\n')

    # check if there is a LQFB initiative
    if 'value' in issue['custom_fields'][2] and issue['custom_fields'][2]['value'] != '':
        f.write('\\input{./antraege/' + str(issue['id']) + '-lqfb.tex}\n')
#        lqfb_id = int(issue['custom_fields'][2]['value'])
#        u = urllib.request.urlopen('http://opendata.piratenpartei-mv.de/lqfb/mv/' + str(lqfb_id)).read()
#        lqfb_ini = json.loads(u.decode('utf-8'))
#        lqfb_ini = lqfb_ini[0]
#
#        # skip LQFB initiatives that have not been finished
#        if lqfb_ini['agreed'] == None or lqfb_ini['issue_closed'] == '':
#            # not yet closed
#            f.write('\\setboolean{LPTlqfb}{true}\n')
#            f.write('\\renewcommand{\\LPTlqfbinitiative}{' + str(lqfb_id) + '}\n')
#            f.write('\\renewcommand{\\LPTlqfbvote}{noch kein Abstimmungsergebnis}\n')
#            f.write('\\renewcommand{\\LPTlqfbarea}{LQFB-Initiative im Bereich ' + str(lqfb_ini['area_name']) + '}\n')
#
#            if lqfb_ini['issue_fully_frozen'] == '':
#                # in discussion
#                t = time.strptime(lqfb_ini['issue_accepted'], "%Y-%m-%d %H:%M:%S")
#                days_till_vote = int(lqfb_ini['issue_discussion_time'].replace(' days', '')) + int(lqfb_ini['issue_verification_time'].replace(' days', ''))
#                t2 = datetime.fromtimestamp(time.mktime(t)) + timedelta(days=days_till_vote)
#                f.write('\\renewcommand{\\LPTlqfbsummary}{in Diskussion seit ' + time.strftime("%-d. %B %Y", t) + ', Abstimmung ab ' + time.strftime("%-d. %B %Y", t2.timetuple()) + '}\n')
#            else:
#                # in voting
#                t = time.strptime(lqfb_ini['issue_fully_frozen'], "%Y-%m-%d %H:%M:%S")    
#                days_till_vote = int(lqfb_ini['issue_verification_time'].replace(' days', ''))
#                t2 = datetime.fromtimestamp(time.mktime(t)) + timedelta(days=days_till_vote)
#                f.write('\\renewcommand{\\LPTlqfbsummary}{in Abstimmung von ' + time.strftime("%-d. %B %Y", t) + ' bis ' + time.strftime("%-d. %B %Y", t2.timetuple()) + '}\n')
#
#            continue
#
#        else:
#            # agreed initiative
#            t = time.strptime(lqfb_ini['issue_closed'], "%Y-%m-%d %H:%M:%S")
#            tot = lqfb_ini['issue_voter_count']
#            pos = lqfb_ini['positive_votes']
#            neg =  lqfb_ini['negative_votes']
#            dc = tot - pos - neg
#            pos_p = int(round ((pos/(tot-dc))*100 ,0))
#            neg_p = int(round ((neg/(tot-dc))*100 ,0))
#
#            verdict = ''
#            if lqfb_ini['agreed'] == True:
#                verdict = 'Angenommen auf Platz ' + str(lqfb_ini['rank'])
#            else:
#                verdict = 'Abgelehnt'
#
#            f.write('\\setboolean{LPTlqfb}{true}\n')
#            f.write('\\renewcommand{\\LPTlqfbinitiative}{' + str(lqfb_id) + '}\n')
#            f.write('\\renewcommand{\\LPTlqfbvote}{Abstimmung: Ja: ' + str(pos) + ' (' + str(pos_p) + '\,\%) ' + ' $-$ Enthaltung: ' + str(dc) + ' $-$ Nein: ' + str(neg) + ' (' + str(neg_p) + '\,\%)' + '}\n')
#            f.write('\\renewcommand{\\LPTlqfbsummary}{' + verdict + ' am ' + time.strftime("%-d. %B %Y", t) + '}\n')
#            f.write('\\renewcommand{\\LPTlqfbarea}{LQFB-Initiative im Bereich ' + str(lqfb_ini['area_name']) + '}\n')
    else:
       f.write('\\setboolean{LPTlqfb}{false}\n')

    f.close()
