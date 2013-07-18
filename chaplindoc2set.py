#!/usr/local/bin/python

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag 

db = sqlite3.connect('chaplin.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = 'chaplin.docset/Contents/Resources/Documents'

page = open(os.path.join(docpath,'index.html')).read()
soup = BeautifulSoup(page)

any = re.compile('.*')
for tag in soup.find_all('a', {'href':any}):
    name = tag.text.strip()
    if len(name) > 0:
        path = tag.attrs['href'].strip()
        if path.split('#')[0] not in ('index.html'):
            tag = str(tag)
            docType = 'Guide'
            print '=============================================================================================='
            if re.findall('chaplin.utils|chaplin.helpers|chaplin.event_broker|Chaplin.SyncMachine|Chaplin.support', tag):
                print 'Library: %s' % (name)
                docType = 'Library'

            elif re.findall('event', tag):
                print 'Event: %s' % (name)
                docType = 'Event'

            elif re.findall('chaplin\.', tag):
                print 'Class: %s' % (name)
                docType = 'cl'

            else:
            	print 'Guide: %s' % (name)

            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, docType, path))            

db.commit()
db.close()
