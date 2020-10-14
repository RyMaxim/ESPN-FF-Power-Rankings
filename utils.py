import os
import sys
import yagmail

def set_week(league):
    print('THIS WEEK = ' + str(league.current_week), flush=True)
    print('NFL WEEK = ' + str(league.nfl_week), flush=True)
    if league.current_week <= 1:
        print('>> Week 1 is not complete. Wait until Tuesday of week 2. Terminating...',flush=True)
        sys.exit(0)
    if league.current_week > league.settings.reg_season_count:
        print('>> Regular season has ended.',flush=True)
        if league.current_week < league.nfl_week:
            print('>> Championship is over.',flush=True)
            return len(league.teams[0].schedule)
    return league.current_week - 1

def ratio(p1,p2):
    if p2 <= 0:
        return "PERFECT"
    else:
        return round(p1 / p2,2)

def send_email(subject,html_body):
    _EMAIL_TO = os.environ['_EMAIL_TO']
    _EMAIL_FROM = os.environ['_EMAIL_FROM']
    _EMAIL_PASS = os.environ['_EMAIL_PASS']
    print('', flush=True)
    yag = yagmail.SMTP(user=_EMAIL_FROM, password=_EMAIL_PASS)
    for email in _EMAIL_TO.split(','):
        try:
            yag.send(to=email, subject=subject, contents=html_body)
            print('EMAIL SENT TO: ' + email, flush=True)
        except:
            print('EMAIL FAILED TO: ' + email, flush=True)
            raise Exception("Email failed to send!")
    print('', flush=True)