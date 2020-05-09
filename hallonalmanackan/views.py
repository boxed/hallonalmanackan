from django.http import HttpResponse


def index(request):
    from datetime import date, timedelta
    from dateutil.rrule import rrule, DAILY

    # todo: week number, visually mark week

    first_of_year = date(date.today().year, 1, 1)
    last_of_year = date(date.today().year + 1, 1, 1) - timedelta(days=1)

    days = {}
    week = {}
    for dt in rrule(DAILY, dtstart=first_of_year, until=last_of_year):
        days[(dt.month, dt.day)] = dt.weekday()
        week[(dt.month, dt.day)] = dt.isocalendar()[1]

    weekday_name = {
        0: 'mån',
        1: 'tis',
        2: 'ons',
        3: 'tors',
        4: 'fre',
        5: 'lör',
        6: 'sön',
    }

    today = date.today()
    week_number = date.isocalendar(today)[1]
    year = today.year

    month_names = {i+1: x for i, x in enumerate([
        'Januari',
        'Februari',
        'Mars',
        'April',
        'Maj',
        'Juni',
        'Juli',
        'Augusti',
        'September',
        'Oktober',
        'November',
        'December',
    ])}

    html = '''
    <head>
    <title>
    v''' + str(week_number) + '''
    </title>

    <style>
    .weekday_0 {
        border-top: 1px solid black;
    }
    .weekday_6 {
        color: #e10000;
    }
    .week_0 {
        background: #eeeeee;
    }
    table {
        border-spacing: 10px 0;
    }
    .today {
        background-color: lightcoral;
    }
    .number {
        width: 20px;
        text-align: right;
        display: inline-block;
        font-weight: bold;
    }
    .week_number {
        padding-left: 10px;
        color: #e10000;
    }
    body {
        text-align: center;
    }
    th {
        padding-bottom: 20px;
    }
    </style>
    <body>
    '''

    html += '<h1>' + str(year) + '</h1>'

    html += '<table>'
    html += '<tr>'
    for month in range(1, 13):
        html += '<th>' + month_names[month] + '</th>'
    html += '</tr>'

    for day in range(1, 32):
        html += '<tr>'
        for month in range(1, 13):
            even_odd_week = week.get((month, day), 0) % 2
            weekday = days.get((month, day))
            if weekday is None:
                even_odd_week = 'blank'
            try:
                week_number = str(date(year, month, day).isocalendar()[1])
            except ValueError:
                week_number = None
            today_class = 'today' if month == today.month and day == today.day else ''
            html += f'<td class="weekday_{weekday} week_{even_odd_week} {today_class} w_{week_number}">'
            if weekday is not None:
                html += '<span class="number">' + str(day) + '</span> '
                html += weekday_name[weekday]

            if weekday == 0:
                html += ' <span class="week_number">' + week_number + '</span>'
            html += '</td>'
        html += '</tr>'
    html += '''
    </table>
    
    <script>
    document.addEventListener('click', function(e) {
        // loop parent nodes from the target to the delegation node
        for (var target = e.target; target && target != this; target = target.parentNode) {
            if (target.matches('td')) {
                var td = target;
                if (td.tagName !== 'TD') {
                    td = td.parentNode;
                }
                document.querySelectorAll('.' + td.classList[2]).forEach(function(x) {
                    if (x.classList.contains('today')) {
                        return;
                    }
                    
                    if (x.style.backgroundColor === 'lightpink') {
                        x.style.backgroundColor = 'white';
                    }
                    else {
                        x.style.backgroundColor = 'lightpink';
                    }
                })
                
                break;
            }
        }
    }, false);
    </script>
    </body>
    '''

    return HttpResponse(html)
