from espn_api.football import League as ESPNLeague
from myteam import MyTeam

class MyLeague(ESPNLeague):
    def convert_teams(self):  # convert Team objects to MyTeam subclass
        for team in self.teams:
            team.__class__ = MyTeam

    def build_boxscores(self):
        print('', flush=True)
        print('BUILDING AND ANALYZING BOXSCORES...', flush=True)
        for w in range(1,self.current_week + 1):  # aggregate all box scores for each week of the season
            box_scores = self.box_scores(w)
            for team in self.teams:  # add the box scores to a list of boxscore objects for each team
                team.build_boxscore(box_scores)

    def build_power_rankings(self):
        print('', flush=True)
        print('BUILDING POWER RANKINGS...', flush=True)
        self.all_power_rankings = list()
        for week in range(1,self.current_week + 1):  # calculate power rankings for each week of the season
            week_rankings = list()
            power_rankings = self.power_rankings(week)
            for t in self.power_rankings(week):
                week_rankings.append({'team': t[1],
                                      'score': t[0],
                                      'rank': power_rankings.index(t) + 1})
            self.all_power_rankings.append(week_rankings)

    def build_standings(self):
        print('', flush=True)
        print('BUILDING STANDINGS...', flush=True)
        self.all_standings = list()
        for week in range(1,self.current_week + 1):  # calculate standings list for each week of the season
            week_standings = list()
            for team in self.teams:  # get information about each team's weekly stats
                week_standings.append({'team': team,
                                       'season_points': team.get_season_points(week),
                                       'season_points_against': team.get_season_points_against(week),
                                       'wins': team.get_wins(week),
                                       'losses': team.get_losses(week),
                                       'ties': team.get_ties(week)})
            # ESPN sorting priority for standings:
            # 1. Most wins
            # 2. If wins are tied, total points scored is the tiebreaker
            week_standings = sorted(week_standings, key=lambda t: (t['wins'], t['season_points']), reverse=True)
            self.all_standings.append(week_standings)

    def get_standings(self,week):
        return self.all_standings[week - 1]

    def get_standings_info(self,team,week):
        standings = self.get_standings(week)
        for t in standings:
            if t['team'].team_id == team.team_id:
                return t

    def get_standings_position(self,team,week):
        standings = self.get_standings(week)
        for t in standings:
            if t['team'].team_id == team.team_id:
                return standings.index(t) + 1

    def get_power_rank(self,team,week):
        for t in self.all_power_rankings[week - 1]:
            if t['team'].team_id == team.team_id:
                return t

    def get_total_points_rank(self,team,week):  # more points = higher rank
        standings = sorted(self.get_standings(week), key=lambda t: t['season_points'], reverse=True)
        for t in standings:
            if t['team'].team_id == team.team_id:
                return standings.index(t) + 1

    def get_total_points_against_rank(self,team,week):  # more points against = higher rank
        standings = sorted(self.get_standings(week), key=lambda t: t['season_points_against'], reverse=True)
        for t in standings:
            if t['team'].team_id == team.team_id:
                return standings.index(t) + 1

    def top_team_week(self,week):  # team with the most points in a given week
        self.teams = sorted(self.teams, key=lambda t: int(t.scores[week - 1]), reverse=True)
        return self.teams[0]

    def bottom_team_week(self,week):  # team with the least points in a given week
        self.teams = sorted(self.teams, key=lambda t: int(t.scores[week - 1]), reverse=False)
        return self.teams[0]

    def top_player_week(self,week):  # player with the most points in a given week
        players = list()
        for team in self.teams:
            players.append(team.top_player(week))
        players = sorted(players, key=lambda p: int(p.points), reverse=True)
        return players[0]

    def bottom_player_week(self,week):  # player with the least points in a given week
        players = list()
        for team in self.teams:
            players.append(team.bottom_player(week))
        players = sorted(players, key=lambda p: int(p.points), reverse=False)
        return players[0]

    def overachiever(self,week):  # player with the highest score compared to projected points in a given week
        players = list()
        for team in self.teams:
            players.append(team.overachiever(week))
        players = sorted(players, key=lambda p: int(p.diff), reverse=True)
        return players[0]

    def underachiever(self,week):  # player with the lowest score compared to projected points in a given week
        players = list()
        for team in self.teams:
            players.append(team.underachiever(week))
        players = sorted(players, key=lambda p: int(p.diff), reverse=False)
        return players[0]

    def largest_mov(self,week):  # team and opponent with the highest margin of victory in a given week
        mov = 0
        for team in self.teams:
            if team.mov[week - 1] > mov:
                mov = team.mov[week - 1]
                winner = team
                loser = team.schedule[week - 1]
        return {'mov': mov,
                'winner': winner,
                'loser': loser}

    def smallest_mov(self,week):  # team and opponent with the lowest margin of victory in a given week
        mov = 1000
        for team in self.teams:
            if team.mov[week - 1] < mov and team.mov[week - 1] >= 0:
                mov = team.mov[week - 1]
                winner = team
                loser = team.schedule[week - 1]
        return {'mov': mov,
                'winner': winner,
                'loser': loser}