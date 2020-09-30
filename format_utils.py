import html_utils
import utils

def format_subject(league,week):
    subject = 'Power Rankings: Week ' \
              + str(week) \
              + ' - ' \
              + str(league.settings.name)
    return subject

def format_league_info(league,week):
    lines = list()

    top_team = league.top_team_week(week)
    lines.append('<strong>Highest scoring team this week:</strong> ' \
                 + str(top_team.scores[week - 1]) \
                 + ' points - ' \
                 + top_team.team_name)

    bottom_team = league.bottom_team_week(week)
    lines.append('<strong>Lowest scoring team this week:</strong> ' \
                 + str(bottom_team.scores[week - 1]) \
                 + ' points - ' \
                 + bottom_team.team_name)

    top_player = league.top_player_week(week)
    lines.append('<strong>Highest scoring player this week:</strong> ' \
                 + str(top_player.points) + ' points - ' \
                 + top_player.name \
                 + ' (' \
                 + top_player.slot_position \
                 + ' - ' \
                 + top_player.team.team_name \
                 + ')')

    bottom_player = league.bottom_player_week(week)
    lines.append('<strong>Lowest scoring player this week:</strong> ' \
                 + str(bottom_player.points) \
                 + ' points - ' \
                 + bottom_player.name \
                 + ' (' \
                 + bottom_player.slot_position \
                 + ' - ' \
                 + bottom_player.team.team_name \
                 + ')')

    overachiever = league.overachiever(week)
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

    underachiever = league.underachiever(week)
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

    large_mov = league.largest_mov(week)
    lines.append('<strong>Biggest blowout:</strong> ' \
                 + str(large_mov['mov']) \
                 + ' points - ' \
                 + large_mov['winner'].team_name \
                 + ' vs ' \
                 + large_mov['loser'].team_name)
    small_mov = league.smallest_mov(week)
    lines.append('<strong>Closest finish:</strong> ' \
                 + str(small_mov['mov']) \
                 + ' points - ' \
                 + small_mov['winner'].team_name \
                 + ' vs ' \
                 + small_mov['loser'].team_name)
    formatted = html_utils.format_list(lines)
    html = '<p>' + formatted + '</p>'
    return html

def format_power_rankings(league,week):
    print('', flush=True)
    print('Formatting power rankings for week ' + str(week), flush=True)
    power_rankings = league.all_power_rankings[week - 1]
    header = 'Power rankings:'
    html = '<p><h3>' + header + '</h3>'
    for t in power_rankings:
        rank_info = format_rank_info(league,t,week)
        extra_info = format_extra_info(league,t,week)
        html = html + '<p>' + rank_info + extra_info + '</p><br>'
    html = html + '</p>'
    return html

def format_rank_info(league,t,week):
    lines = list()
    lines.append(str(t['rank']) + ') ' + t['team'].team_name)
    lines.append(t['team'].owner)
    s = league.get_standings_info(t['team'], week)
    team_WLT = str(s['wins']) + '-' + str(s['losses'])
    team_WLT += '-' + str(s['ties']) if s['ties'] > 0 else ''
    lines.append(team_WLT + ', ' + str(s['season_points']) + ' points')
    if week > 1:
        previous_rank = league.get_power_rank(t['team'], week - 1)
        lines.append('Last week rank: ' + str(previous_rank['rank']))
    html = html_utils.format_list(lines)
    return html

def format_extra_info(league,t,week):
    team = t['team']
    box = team.boxscores[week - 1]
    team_stats = league.get_standings_info(t['team'], week)
    html = ''

    row = list()
    row.append({'Dominance score': str(t['score'])})
    row.append({'Standings position': str(league.get_standings_position(team, week))})
    if week > 1:
        row.append({'Prev standing pos': str(league.get_standings_position(team, week - 1))})
    html+= html_utils.format_table(row)

    row = list()
    row.append({'Points': str(box.points)})
    row.append({'Bench points': str(box.bench_points)})
    row.append({'The Ratio™': str(utils.ratio(box.points,box.bench_points))})
    html += html_utils.format_table(row)

    row = list()
    row.append({'Season points': str(team_stats['season_points'])})
    row.append({'Seas. pts against': str(team_stats['season_points_against'])})
    season_points_diff = team_stats['season_points'] - team_stats['season_points_against']
    if season_points_diff > 0:
        season_diff_text = '+' + str(season_points_diff)
    else:
        season_diff_text = str(season_points_diff)
    row.append({'Season pts diff': season_diff_text})
    html += html_utils.format_table(row)

    row = list()
    total_pts_rank  = (league.get_total_points_rank(team,week))
    row.append({'Season points rank': str(total_pts_rank)})
    total_pts_against_rank = league.get_total_points_against_rank(team,week)
    row.append({'Season pts against rank': str(total_pts_against_rank)})
    html += html_utils.format_table(row)

    row = list()
    row.append({'Game result': team.streak_type})
    row.append({'Current streak': str(team.streak_length) + 'x ' + team.streak_type})
    html += html_utils.format_table(row)

    row = list()
    row.append({'Opponent': box.opponent.team_name if box.opponent != 'BYE' else 'BYE'})
    row.append({'Opponent points': str(box.opponent_points) if box.opponent != 'BYE' else 'N/A'})
    if week > 1:
        row.append({'Oppt prev rank': str(league.get_power_rank(box.opponent,week - 1)['rank']) if box.opponent != 'BYE' else 'N/A'})
    html += html_utils.format_table(row)

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
    html += html_utils.format_table(row)

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
    html += html_utils.format_table(row)

    if len(box.goose_eggs) > 0:
        row = list()
        row.append({'Goose eggs': format_goose_eggs(box.goose_eggs)})
        html += html_utils.format_table(row)

    next_week = week + 1
    if next_week <= len(team.schedule):
        row = list()
        next_oppt = team.schedule[next_week - 1]
        if next_oppt.team_id == team.team_id:
            next_oppt_name = 'BYE'
            next_oppt_rank = 'N/A'
            next_oppt_WLT = 'N/A'
        else:
            next_oppt_name = next_oppt.team_name
            next_oppt_rank = str(league.get_power_rank(next_oppt, week)['rank'])
            o = league.get_standings_info(next_oppt, week)
            next_oppt_WLT = str(o['wins']) + '-' + str(o['losses'])
            next_oppt_WLT += '-' + str(o['ties']) if o['ties'] > 0 else ''
        row.append({'Next opponent': next_oppt_name})
        row.append({'Next oppt rank': next_oppt_rank})
        row.append({'Next oppt W-L': next_oppt_WLT})
        html += html_utils.format_table(row)

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