from espn_api.football import Team as ESPNTeam
from myboxscore import MyBoxScore
import functions

class MyTeam(ESPNTeam):
    def build_boxscore(self,boxscores):
        if not hasattr(self, 'boxscores'):
            self.boxscores = list()
        for game in boxscores:
            if game.home_team.team_id == self.team_id:
                self.boxscores.append(MyBoxScore(game,'home'))
                break
            if game.away_team.team_id == self.team_id:
                self.boxscores.append(MyBoxScore(game,'away'))
                break

    def get_season_points(self,week):
        season_points = 0
        #for boxscore in self.boxscores[:week]:
        #    season_points += boxscore.points
        season_points = sum(boxscore.points for boxscore in self.boxscores[:week])
        return season_points

    def get_season_points_against(self,week):
        season_points_against = 0
        #for boxscore in self.boxscores[:week]:
        #    season_points_against += boxscore.opponent_points
        season_points_against = sum(boxscore.opponent_points for boxscore in self.boxscores[:week])
        return season_points_against

    def get_wins(self,week):
        wins = 0
        for boxscore in self.boxscores[:week]:
            wins += 1 if boxscore.points > boxscore.opponent_points else 0
        return wins

    def get_losses(self,week):
        losses = 0
        for boxscore in self.boxscores[:week]:
            losses += 1 if boxscore.points < boxscore.opponent_points else 0
        return losses

    def get_ties(self,week):
        ties = 0
        for boxscore in self.boxscores[:week]:
            ties += 1 if boxscore.points == boxscore.opponent_points else 0
        return ties

    def top_player(self,week):
        return self.boxscores[week - 1].top_player

    def bottom_player(self,week):
        return self.boxscores[week - 1].bottom_player

    def overachiever(self,week):
        return self.boxscores[week - 1].overachiever

    def underachiever(self,week):
        return self.boxscores[week - 1].underachiever

    def goose_eggs(self,week):
        return self.boxscores[week - 1].goose_eggs
