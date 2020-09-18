import os
import re
import yagmail

def format_subject(league):
    print('', flush=True)
    this_week = league.current_week
    last_week = this_week - 1 if this_week > 1 else 1
    subject = 'Power Rankings: Week ' \
              + str(last_week) \
              + ' - ' \
              + str(league.settings.name)
    print(subject, flush=True)
    return subject

def format_league_info(league):
    this_week = league.current_week
    last_week = this_week - 1 if this_week > 1 else 1
    lines = list()

    top_team = league.top_team_week(last_week)
    lines.append('<strong>Highest scoring team this week:</strong> ' \
                 + str(top_team.scores[last_week - 1]) \
                 + ' points - ' \
                 + top_team.team_name)

    bottom_team = league.bottom_team_week(last_week)
    lines.append('<strong>Lowest scoring team this week:</strong> ' \
                 + str(bottom_team.scores[last_week - 1]) \
                 + ' points - ' \
                 + bottom_team.team_name)

    top_player = league.top_player_week(last_week)
    lines.append('<strong>Highest scoring player this week:</strong> ' \
                 + str(top_player.points) + ' points - ' \
                 + top_player.name \
                 + ' (' \
                 + top_player.slot_position \
                 + ' - ' \
                 + top_player.team.team_name \
                 + ')')

    bottom_player = league.bottom_player_week(last_week)
    lines.append('<strong>Lowest scoring player this week:</strong> ' \
                 + str(bottom_player.points) \
                 + ' points - ' \
                 + bottom_player.name \
                 + ' (' \
                 + bottom_player.slot_position \
                 + ' - ' \
                 + bottom_player.team.team_name \
                 + ')')

    overachiever = league.overachiever(last_week)
    over_diff = '+' + str(overachiever.diff) if overachiever.diff > 0 else overachiever.diff
    lines.append('<strong>Biggest overachiever:</strong> ' \
                 + str(over_diff) \
                 + ' (' \
                 + str(overachiever.points) \
                 + ' points - ' \
                 + str(overachiever.projected_points) \
                 + ' projected) - ' \
                 + overachiever.name \
                 + ' (' \
                 + overachiever.slot_position \
                 + ' - ' \
                 + overachiever.team.team_name \
                 + ')')

    underachiever = league.underachiever(last_week)
    under_diff = '+' + str(underachiever.diff) if underachiever.diff > 0 else underachiever.diff
    lines.append('<strong>Worst underachiever:</strong> ' \
                 + str(under_diff) \
                 + ' (' \
                 + str(underachiever.points) \
                 + ' points - ' \
                 + str(underachiever.projected_points) \
                 + ' projected) - ' \
                 + underachiever.name \
                 + ' (' \
                 + underachiever.slot_position \
                 + ' - ' \
                 + underachiever.team.team_name \
                 + ')')

    formatted = format_html_list(lines)
    html = '<p>' + formatted + '</p>'
    print('', flush=True)
    print(html, flush=True)
    return html

def format_power_rankings(league):
    print('', flush=True)
    this_week = league.current_week
    last_week = this_week - 1 if this_week > 1 else 1
    print('Formatting power rankings for week ' + str(last_week), flush=True)
    power_rankings = league.all_power_rankings[last_week - 1]
    header = 'Power rankings:'
    print(header, flush=True)
    html = '<p><h3>' + header + '</h3>'
    for t in power_rankings:
        rank_info = format_rank_info(league,t)
        extra_info = format_extra_info(league,t)
        html = html + '<p>' + rank_info + extra_info + '</p><br>'
    html = html + '</p>'
    print('', flush=True)
    print(html, flush=True)
    return html

def format_rank_info(league,t):
    this_week = league.current_week
    last_week = this_week - 1 if this_week > 1 else 1
    lines = list()
    lines.append(str(t['rank']) + ') ' + t['team'].team_name)
    lines.append(t['team'].owner)
    s = league.get_standings_info(t['team'], last_week)
    team_WLT = str(s['wins']) + '-' + str(s['losses'])
    team_WLT += '-' + str(s['ties']) if s['ties'] > 0 else ''
    lines.append(team_WLT + ', ' + str(s['season_points']) + ' points')
    if last_week > 1:
        previous_rank = league.get_team_power_rank(t['team'], last_week - 1)
        lines.append('Last week rank: ' + str(previous_rank['rank']))
    html = format_html_list(lines)
    return html

def format_extra_info(league,t):
    this_week = league.current_week
    last_week = this_week - 1 if this_week > 1 else 1
    team = t['team']
    box = team.boxscores[last_week - 1]
    team_stats = league.get_standings_info(t['team'], last_week)
    html = ''

    row = list()
    row.append({'Dominance score': str(t['score'])})
    row.append({'Standings position': str(league.get_standings_position(team, last_week))})
    if last_week > 1:
        row.append({'Prev standings pos': str(league.get_standings_position(team, last_week - 1))})
    html+= format_html_table(row)

    row = list()
    row.append({'Points': str(box.points)})
    row.append({'Bench points': str(box.bench_points)})
    row.append({'The Ratio™': str(ratio(box.points,box.bench_points))})
    html += format_html_table(row)

    row = list()
    row.append({'Season points': str(team_stats['season_points'])})
    row.append({'Seas. pts against': str(team_stats['season_points_against'])})
    season_points_diff = team_stats['season_points'] - team_stats['season_points_against']
    if season_points_diff > 0:
        season_diff_text = '+' + str(season_points_diff)
    else:
        season_diff_text = str(season_points_diff)
    row.append({'Season pts diff': season_diff_text})
    html += format_html_table(row)

    row = list()
    total_pts_rank  = (league.get_total_points_rank(team,last_week))
    row.append({'Season points rank': str(total_pts_rank)})
    total_pts_against_rank = league.get_total_points_against_rank(team,last_week)
    row.append({'Season pts against rank': str(total_pts_against_rank)})
    html += format_html_table(row)

    row = list()
    row.append({'Game result': team.streak_type})
    row.append({'Current streak': str(team.streak_length) + 'x ' + team.streak_type})
    html += format_html_table(row)

    row = list()
    row.append({'Opponent': box.opponent.team_name})
    row.append({'Opponent points': str(box.opponent_points)})
    if last_week > 1:
        row.append({'Oppt prev rank': str(league.get_team_power_rank(box.opponent,last_week - 1))})
    html += format_html_table(row)

    row = list()
    row.append({'Top player': str(box.top_player.points) \
                              + ': ' \
                              + box.top_player.name \
                              + ' - ' \
                              + box.top_player.slot_position})
    row.append({'Worst player': str(box.bottom_player.points) \
                                + ': ' \
                                + box.bottom_player.name \
                                + ' - ' \
                                + box.bottom_player.slot_position})
    html += format_html_table(row)

    row = list()
    over_diff = '+' + str(box.overachiever.diff) if box.overachiever.diff > 0 else box.overachiever.diff
    row.append({'Overachiever': str(over_diff) \
                                + ' (' \
                                + str(box.overachiever.points) \
                                + 'pts - ' \
                                + str(box.overachiever.projected_points) \
                                + 'prj)<br>' \
                                + box.overachiever.name \
                                + ' - ' \
                                + box.overachiever.slot_position})
    under_diff = '+' + str(box.underachiever.diff) if box.underachiever.diff > 0 else box.underachiever.diff
    row.append({'Underachiever': str(under_diff) \
                                 + ' (' \
                                 + str(box.underachiever.points) \
                                 + 'pts - ' \
                                 + str(box.underachiever.projected_points) \
                                 + 'prj)<br>' \
                                 + box.underachiever.name \
                                 + ' - ' \
                                 + box.underachiever.slot_position})
    html += format_html_table(row)

    if len(box.goose_eggs) > 0:
        row = list()
        row.append({'Goose eggs': format_goose_eggs(box.goose_eggs)})
        html += format_html_table(row)

    if this_week <= len(team.schedule):
        row = list()
        next_oppt = team.schedule[this_week - 1]
        row.append({'Next opponent': next_oppt.team_name})
        row.append({'Next oppt rank': str(league.get_power_rank(next_oppt, last_week)['rank'])})
        o = league.get_standings_info(next_oppt, last_week)
        next_oppt_WLT = str(o['wins']) + '-' + str(o['losses'])
        next_oppt_WLT += '-' + str(o['ties']) if o['ties'] > 0 else ''
        row.append({'Next oppt W-L': next_oppt_WLT})
        html += format_html_table(row)

    return html

def ratio(p1,p2):
    if p2 <= 0:
        return "PERFECT"
    else:
        return round(p1 / p2,2)

def format_html_list(list):
    print('', flush=True)
    html = '<dl>'
    for line in list:
        print(line, flush=True)
        if re.match(r'^\d+\)', line):  # if line starts with a 1), 12), etc
            line = '<strong>' + line + '</strong>'  # bold it
        if line[0] == '-':  # if line starts with an hyphen
            line = line.replace('-','&nbsp;&nbsp;',1)  # remove hyphen + indent 2 spaces
        html = html + '<dt>' + line + '</dt>'
    html = html + '</dl>'
    return html

def format_html_table(row):
    table_width = 666
    cell_width = round(table_width / len(row) / 2, 2)
    cell_percent = round(cell_width / table_width * 100, 2)
    html = '<table width="' + str(table_width) \
           + '" cellpadding="1" cellspacing="0" border="1" ' \
           + 'style="border-collapse: collapse; white-space:pre-wrap"><tr>'
    for cell in row:
        html += format_html_cell(cell,cell_percent)
    html += '</tr></table>'
    return html

def format_html_cell(item,width):
    html = ''
    for key in item:
        html += '<td width="' \
             + str(width) \
             + '%" border-left="1" style="background-color:lightgray; text-align:center">' \
             + key \
             + '</td>'
        html += '<td width="' \
             + str(width) \
             + '%" style="text-align:center">' \
             + str(item[key]) \
             + '</td>'
    return html

def format_goose_eggs(goose_eggs):
    html = ''
    for player in goose_eggs:
        html += str(player.points) \
                + ' (' \
                + str(player.projected_points) \
                + ' proj) : ' \
                + player.name \
                + ' - ' + player.slot_position
        if goose_eggs.index(player) + 1 != len(goose_eggs):
            html += '<br>'
    return html

def send_email(subject,html_body):
    _EMAIL_TO = os.environ['_EMAIL_TO']
    _EMAIL_FROM = os.environ['_EMAIL_FROM']
    _EMAIL_PASS = os.environ['_EMAIL_PASS']
    print('', flush=True)
    try:
        #initializing the server connection
        yag = yagmail.SMTP(user=_EMAIL_FROM, password=_EMAIL_PASS)
        #sending the email
        yag.send(to=_EMAIL_TO, subject=subject, contents=html_body)
        print("Email sent successfully", flush=True)
    except:
        print("Error, email was not sent", flush=True)
        raise Exception("Email failed to send!")