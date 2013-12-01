#!/usr/bin/python

# TO DO:
# 1. Auto email results
# 2. Auto RSS results
# 3. Make github repo
# 4. Set up local_var file
# 5. Fix extra spaces in text output 

from datetime import date

week_abbr = { 0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat' }
mon_abbr = {1: 'Jan.', 2: 'Feb.', 3: 'Mar.', 4: 'Apr.', 5: 'May', 6: 'Jun.', 7: 'Jul.', 8: 'Aug.', 9: 'Sep.', 10: 'Oct.', 11: 'Nov.', 12: 'Dec.'}
additional_info_types = {'sponsor': 'Sponsor: ', 'website': 'Web: ', 'facebook': 'Facebook: ', 'email': 'Email: ', 'phone_number': 'Phone: '}
fields = ['start_date', 'start_time', 'location', 'address', 'event_title', 'event_description', 'sponsor', 'website', 'facebook', 'email', 'phone_number']
title = "Chicago Indymedia Community Calendar" 

import cgi
form = cgi.FieldStorage()
a = form.getvalue('a')
if a == None:
    a = ''

def get_date(start_date):
    s = start_date.split('-')
    return date(int(s[0]), int(s[1]), int(s[2]))

def get_day_of_week(start_date):
    week_abbr = { 0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat' }
    d = get_date(start_date)
    return week_abbr[d.weekday()]

def get_data_dictionary(r):
    d = {}
    for i, f in enumerate(fields):
       if r[i + 1] == None:
           d[f] = ''
       else:
           d[f] = r[i + 1] 
    return d 

def get_date_and_location_line(d):
    temp_date = get_date(d['start_date'])
    day_of_week = get_day_of_week(d['start_date'])
    month = temp_date.month
    day = temp_date.day
    to_return = day_of_week + ", " + mon_abbr[month] + " " + str(day) + " " + d['start_time'] + " -- " + d['location']
    if d['address'] != '':
        to_return = to_return + " (" + d['address'] + ")"
    return to_return

def get_info(d, t, output_type):
    to_return = ''
    line_end = "<BR>\n"
    if output_type == 'text':
        line_end = "\n" 
    try:
        if d[t] != '':
             to_return = additional_info_types[t] + d[t] + line_end 
    except:
        pass
    return to_return

def print_html_head():
    print """Content-type: text/html\n\n
<HTML>
<HEAD><TITLE>%s</TITLE>
</HEAD>
<BODY>
<H1>%s</H1>
    """ % (title, title)

def print_calendar(rows, output_type, css_file):
    # <link charset="utf-8" media="all" type="text/css" href="%s" rel="stylesheet">
    if output_type == 'text':
        print """Content-type: text/html\n\n"""
        print "<HTML><BODY><PRE>"
    else: 
        print_html_head()
        print """<TABLE border=1>"""
    for row in rows:
        d = get_data_dictionary(row)
        date_and_location_line = get_date_and_location_line(d)
        additional_info_line = get_info(d, 'sponsor', output_type) + get_info(d, 'website', output_type) + get_info(d, 'facebook', output_type) + get_info(d, 'email', output_type) + get_info(d, 'phone_number', output_type) 
        if output_type == 'text':
            print """
%s\n%s\n%s\n%s\n\n
            """ % (date_and_location_line, d['event_title'].upper(), d['event_description'], additional_info_line)
        else:
            print """<TR><TD>
%s<BR> 
<B>%s</B><BR>
%s<BR>
%s 
</TD></TR>""" % (date_and_location_line, d['event_title'].upper(), d['event_description'], additional_info_line)
    if output_type == 'text':
        print "</PRE></BODY></HTML>"
    else:
        print """</TABLE>
        </BODY>
        </HTML>""" 

def get_input_page():
    print_html_head()
    print """
<FORM method="POST" action="./community_calendar_input.py">
<TABLE>"""
    for i in fields: 
        print """<TR><TD>%s</TD><TD><input type='text' name='%s' size='15' maxlength='60'/></TD></TR>""" % (i, i)
    print """</TABLE>
<INPUT TYPE=SUBMIT VALUE="Submit">
</FORM>
</BODY>
</HTML>
    """

def get_calendar_entries(a):
    import sqlite3
    from os import listdir
    generate_new_calendar = 0
    if 'community_calendar.db' not in listdir('.'):
        generate_new_calendar = 1
    conn = sqlite3.connect('community_calendar.db')
    c = conn.cursor()
    if generate_new_calendar == 1:
        c.execute('''CREATE TABLE community_calendar (id integer primary key, start_date text, start_time text, location text, address text, event_title text, event_description text, sponsor text, website text, facebook text, email text, phone_number text)''')
        conn.commit()
    rows = c.execute('SELECT * FROM community_calendar WHERE start_date != "" ORDER BY start_date asc, start_time asc')
    print_calendar(rows, a, "community_calendar.css") 
    c.close()

def maestro():
    if a == 'input':
        get_input_page()
    else:
        get_calendar_entries(a)

if __name__ == "__main__":
    maestro()
