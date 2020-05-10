from datetime import date, datetime
from json import loads

from requests import get
from django.http import HttpResponse

from .models import Holiday


def fill_holidays(year):
    days = loads(get(f'https://api.dryg.net/dagar/v2.1/{year}').text)['dagar']
    holidays = [
        dict(
            name=x['helgdag'],
            date=datetime.strptime(x['datum'], '%Y-%m-%d'),
        )
        for x in days
        if 'helgdag' in x
    ]
    for x in holidays:
        if x['name'] == 'Annandag pingst':
            continue
        Holiday.objects.create(name=x['name'], year=x['date'].year, month=x['date'].month, day=x['date'].day)


def get_holidays(year, fill=True):
    holidays = {
        date(x.year, x.month, x.day): x.name
        for x in Holiday.objects.filter(year=year)
    }
    if not holidays and year > 1990:
        assert fill
        fill_holidays(year)
        return get_holidays(year, fill=False)
    return holidays


holiday_short_names = {
    'Nyårsdagen': 'Nyår',
    'Trettondedag jul': '13',
    'Långfredagen': 'Lång',
    'Påskafton': 'Påsk',
    'Påskdagen': 'Påsk',
    'Annandag påsk': 'Påsk',
    'Första Maj': '1 maj',
    'Kristi himmelsfärdsdag': 'Kristi',
    'Pingstdagen': 'Pingst',
    'Sveriges nationaldag': '🇸🇪',
    'Midsommarafton': 'Mids',
    'Midsommardagen': 'Mids',
    'Alla helgons dag': 'Helgon',
    'Julafton': 'Jul 🎅',
    'Juldagen': 'Jul',
    'Annandag jul': 'Annan',
    'Nyårsafton': 'Nyår',
}


def index(request):
    from datetime import date, timedelta
    from dateutil.rrule import rrule, DAILY

    if 'year' in request.GET:
        year = int(request.GET['year'])
    else:
        year = date.today().year

    today = date.today()
    week_number = date.isocalendar(date.today())[1]

    first_of_year = date(year, 1, 1)
    last_of_year = date(year + 1, 1, 1) - timedelta(days=1)

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
    .weekday_6, .holiday {
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
    a {
        color: gray;
        text-decoration: none;
    }
    td {
        min-width: 90px;
    }
    </style>
    <body>
    '''

    html += f'<h1><a href="?year={year-1}">&lt;</a> {year}  <a href="?year={year+1}">&gt;</a></h1>'

    html += '<table>'
    html += '<tr>'
    for month in range(1, 13):
        html += '<th>' + month_names[month] + '</th>'
    html += '</tr>'

    holidays = get_holidays(year)

    for day in range(1, 32):
        html += '<tr>'
        for month in range(1, 13):
            even_odd_week = week.get((month, day), 0) % 2
            weekday = days.get((month, day))
            if weekday is None:
                even_odd_week = 'blank'
            try:
                d = date(year, month, day)
                week_number = str(d.isocalendar()[1])
            except ValueError:
                week_number = None
                d = None
            today_class = 'today' if year == today.year and month == today.month and day == today.day else ''
            holiday_class = 'holiday' if d in holidays else ''
            alt = holidays.get(d, '')
            html += f'<td class="weekday_{weekday} week_{even_odd_week} {today_class} w_{week_number} {holiday_class}" title="{alt}">'
            if weekday is not None:
                html += f'<span class=\"number\">{day}</span> '
                if month == 2 and day == 14:
                    html += '❤️'
                elif d in holidays:
                    html += holiday_short_names[holidays[d]]
                else:
                    html += weekday_name[weekday]

            if weekday == 0:
                html += f' <span class=\"week_number\">{week_number}</span>'
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
