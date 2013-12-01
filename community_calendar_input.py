#!/usr/bin/python

import cgi
import sqlite3
form = cgi.FieldStorage()

import local_var

d = {}
for field in local_var.fields:
    if form.getvalue(field) == None:
        d[field] = ''
    else:
        d[field] = form.getvalue(field)

conn = sqlite3.connect('./community_calendar.db')
c = conn.cursor()
c.execute("INSERT INTO community_calendar (start_date, start_time, location, address, event_title, event_description, sponsor, website, facebook, email, phone_number) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (d['start_date'], d['start_time'], d['location'], d['address'], d['event_title'], d['event_description'], d['sponsor'], d['website'], d['facebook'], d['email'], d['phone_number'], ) )
conn.commit()
conn.close()

print "Content-type: text/html\n\n"
print """<meta HTTP-EQUIV='REFRESH' content='0; url=http://www.szcz.org/cc/community_calendar.py'>"""
