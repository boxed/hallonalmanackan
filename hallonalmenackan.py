from datetime import date, timedelta
from itertools import zip_longest
from dateutil.rrule import rrule, DAILY
from collections import defaultdict

# todo: week number, visually mark week

first_of_year = date(date.today().year, 1, 1)
last_of_year = date(date.today().year+1, 1, 1) - timedelta(days=1)

days = {}
week = {}
for dt in rrule(DAILY, dtstart=first_of_year, until=last_of_year):
    days[(dt.month, dt.day)] = dt.weekday()
    week[(dt.month, dt.day)] = dt.isocalendar()[1]
    
weekday_name = {
    0: 'måndag',
    1: 'tisdag',
    2: 'onsdag',
    3: 'torsdag',
    4: 'fredag',
    5: 'lördag',
    6: 'söndag',
}


html = '''

<style>
.weekday_6 {
    color: red;
}
.weekday_0 {
    /*border-top: 1px solid black;*/
}
.week_0 {
    background: #ddd;
}
table {
    border-spacing: 5px 0;
}
</style>

'''
html += '<table>'
html += '<tr>'
html += '<th>' + '' + '</th>'
for month in range(1, 13):
    html += '<th>' + str(month) + '</th>'
html += '</tr>'

for day in range(1, 32):
    html += '<tr>'
    html += '<th>' + str(day) + '</th>'
    for month in range(1, 13):
        even_odd_week = week.get((month, day), 0) % 2
        weekday = days.get((month, day))
        if weekday is None:
            even_odd_week = 'blank'
        html += '<td class="weekday_'+str(weekday)+' week_'+str(even_odd_week)+'">' 
        if weekday is not None:
            html += weekday_name[weekday]
        html += '</td>'
    html += '</tr>'
html += '</table'
