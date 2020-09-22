class MyBoxScore():
    def __init__(self,boxscore,pos):
        if pos == 'home':
            self.team = boxscore.home_team
            self.points = boxscore.home_score
            self.lineup = boxscore.home_lineup
            self.opponent = boxscore.away_team
            self.opponent_points = boxscore.away_score
            self.opponent_lineup = boxscore.away_lineup
        if pos == 'away':
            self.team = boxscore.away_team
            self.points = boxscore.away_score
            self.lineup = boxscore.away_lineup
            self.opponent = boxscore.home_team
            self.opponent_points = boxscore.home_score
            self.opponent_lineup = boxscore.home_lineup
        for player in self.lineup:
            player.team = self.team
        for player in self.opponent_lineup:
            player.team = self.opponent
        self.get_bench_points()
        self.get_top_player()
        self.get_bottom_player()
        self.get_overachiever()
        self.get_underachiever()
        self.get_goose_eggs()
        self.fix_flex_players()

    def get_bench_points(self):  # sum of bench player scores
        self.bench_points = 0
        for player in self.lineup:
            self.bench_points += player.points if player.slot_position == 'BE' else 0

    def get_top_player(self):  # top scoring non-bench, non-IR player
        self.lineup = sorted(self.lineup, key=lambda x: x.points, reverse=True)
        for player in self.lineup:
            if player.slot_position != 'BE' and player.slot_position != 'IR':
                self.top_player = player
                break

    def get_bottom_player(self):  # top scoring non-bench, non-IR player
        self.lineup = sorted(self.lineup, key=lambda x: x.points, reverse=False)
        for player in self.lineup:
            if player.slot_position != 'BE' and player.slot_position != 'IR':
                self.bottom_player = player
                break

    def get_overachiever(self):  # highest delta between points and projection for non-bench, non-IR players
        for player in self.lineup:
            player.diff = round(player.points - player.projected_points,2)
        self.lineup = sorted(self.lineup, key=lambda x: x.diff, reverse=True)
        for player in self.lineup:
            if player.slot_position != 'BE' and player.slot_position != 'IR':
                self.overachiever = player
                break

    def get_underachiever(self):  # lowest delta between points and projection for non-bench, non-IR players
        for player in self.lineup:
            player.diff = round(player.points - player.projected_points,2)
        self.lineup = sorted(self.lineup, key=lambda x: x.diff, reverse=False)
        for player in self.lineup:
            if player.slot_position != 'BE' and player.slot_position != 'IR':
                self.underachiever = player
                break

    def get_goose_eggs(self):  # non-bench, non-IR players who scored 0 or less points
        self.goose_eggs = list()
        for player in self.lineup:
            if player.slot_position != 'BE' and player.slot_position != 'IR' and player.points <= 0:
                self.goose_eggs.append(player)

    def fix_flex_players(self):  # convert position text for FLEX players to 'FLX'
        for player in self.lineup:
            player.slot_position = 'FLX' if player.slot_position == 'RB/WR/TE' else player.slot_position
        for player in self.opponent_lineup:
            player.slot_position = 'FLX' if player.slot_position == 'RB/WR/TE' else player.slot_position
