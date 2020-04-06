import json
import datetime

def get_data():
    with open('data.json') as f:
        data = json.load(f)
        return data
    return False


msg_start = """<b>Welcome to The India Covid-19 Tracker Bot! 🦠</b>
(<i>a crowdsouced initiative</i>)

The first Indian bot in telegram that can track the coronavirus (COVID-19) outbreak in real-time.


<b><u>Commands:</u></b>

/count
Total cases identified COVID-19 cases in India.

/today
Cases identified as of today.

/statewise
List of statewise cases in India.

/about
Info about the bot and the source.


Note: Open source community generated bot for the people to stay informed. No legal obligation. Community generated data from <a href='https://covid19india.org'>covid19india.org</a>.

Government Updates: @MyGovCoronaNewsdesk
by <a href='https://twitter.com/akigugale'>@akigugale</a>\n\n


"""



msg_about = """<b>This is the India Covid-19 Tracker Bot! 🦠 🇮🇳</b>
(<i>a crowdsouced initiative</i>)

The first Indian bot in telegram that can track the coronavirus (COVID-19) outbreak in real-time.

Built by - <a href="https://twitter.com/akigugale">@akigugale</a>

Data from - https://covid19india.org

Official Indian Govt. Telegram Channel: @MyGovCoronaNewsdesk

Contribute at - https://github.com/akigugale/covid19india-telegram-bot


------------x x x ------------
Made for public information, no legal obligation.
"""

def pretty_date_time(date_time):
    date_time_obj = datetime.datetime.strptime(date_time, "%d/%m/%Y %H:%M:%S")
    formatted_date_time = date_time_obj.strftime("%d %b, %H:%M IST")
    return formatted_date_time


def get_lastupdated_msg():
    data = get_data()
    last_updated_time = data['statewise'][0]['lastupdatedtime']
    msg_lastupdated = """Last Updated on <b>{0}</b>""".format(pretty_date_time(last_updated_time))
    return msg_lastupdated



def get_count_msg():
    data = get_data()
    total = data['statewise'][0]
    msg = """<b>Number of Covid-19 cases in India:</b>

😷 Confirmed: <b>{confirmed}</b>  [+{deltaconfirmed}]
🔴 Active: <b>{active}</b>
💚 Recovered: <b>{recovered}</b>  [+{deltarecovered}]
💀 Deceased: <b>{deaths}</b>  [+{deltadeaths}]

Updated on {updated_on}
    """.format(confirmed=total["confirmed"], deltaconfirmed=total["deltaconfirmed"], active=total['active'], recovered=total['recovered'], deltarecovered=total['recovered'], deaths=total['deaths'], deltadeaths=total['deltadeaths'], updated_on=pretty_date_time(total['lastupdatedtime']))
    return msg



def get_today_msg():
    data = get_data()
    total = data['statewise'][0]
    updated_on=pretty_date_time(total['lastupdatedtime'])
    msg = """<b>New Covid-19 cases in India on {date} till {time}:</b>

😷 Confirmed: +{deltaconfirmed}
💚 Recovered: +{deltarecovered}
💀 Deceased:  +{deltadeaths}

Updated on {updated_on}
    """.format(deltaconfirmed=total["deltaconfirmed"], deltarecovered=total['recovered'], deltadeaths=total['deltadeaths'],updated_on=updated_on , date=updated_on[0:6], time=updated_on[-9:])
    return msg



def get_statewise_msg():
    return "Still in development, contribute at https://github.com/akigugale/covid19india-telegram-bot"


