import datetime
import os
from myleague import MyLeague
from myteam import MyTeam
import functions

_ESPN_LEAGUE_ID = os.environ['_ESPN_LEAGUE_ID']
_ESPN_S2 = os.environ['_ESPN_S2']
_ESPN_SWID = os.environ['_ESPN_SWID']
_YEAR = datetime.datetime.now().year

def main():
    league = MyLeague(league_id=_ESPN_LEAGUE_ID, year=_YEAR, espn_s2=_ESPN_S2, swid=_ESPN_SWID)
    this_week = league.current_week
    last_week = this_week - 1 if this_week > 1 else 1
    print('THIS WEEK = ' + str(this_week), flush=True)
    print('GENERATING POWER RANKINGS FOR WEEK = ' + str(last_week), flush=True)
    league.convert_teams()
    league.build_boxscores()
    league.build_standings()
    league.build_power_rankings()
    subject = functions.format_subject(league)
    league_info_html = functions.format_league_info(league)
    power_rankings_html = functions.format_power_rankings(league)
    html_body = '<HTML><BODY>' + league_info_html + power_rankings_html + '</BODY></HTML>'

    functions.send_email(subject,html_body)

if __name__ == '__main__':
    main()