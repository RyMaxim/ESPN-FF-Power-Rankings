import datetime
import os
from myleague import MyLeague
from myteam import MyTeam
import format_utils
import utils

_ESPN_LEAGUE_ID = os.environ['_ESPN_LEAGUE_ID']
_ESPN_S2 = os.environ['_ESPN_S2']
_ESPN_SWID = os.environ['_ESPN_SWID']
_YEAR = datetime.datetime.now().year

def main():
    league = MyLeague(league_id=_ESPN_LEAGUE_ID, year=_YEAR, espn_s2=_ESPN_S2, swid=_ESPN_SWID)
    week = utils.set_week(league)
    print('GENERATING POWER RANKINGS FOR WEEK ' + str(week), flush=True)
    league.convert_teams()
    league.build_boxscores()
    league.build_standings()
    league.build_power_rankings()
    subject = format_utils.format_subject(league,week)
    league_info_html = format_utils.format_league_info(league,week)
    power_rankings_html = format_utils.format_power_rankings(league,week)
    html_body = '<HTML><BODY>' + league_info_html + power_rankings_html + '</BODY></HTML>'

    utils.send_email(subject,html_body)

if __name__ == '__main__':
    main()