class MyBoxScore():
    def __init__(self,boxscore,pos,bye=None):
        if pos == 'home':
            opp = 'away'
        if pos == 'away':
            opp = 'home'
        self.team = getattr(boxscore,pos + '_team')
        self.points = getattr(boxscore,pos + '_score')
        self.lineup = getattr(boxscore,pos + '_lineup')
        self.opponent = getattr(boxscore,opp + '_team') if not bye else 'BYE'
        self.opponent_points = getattr(boxscore,opp + '_score') if not bye else 0
        self.opponent_lineup = getattr(boxscore,opp + '_lineup') if not bye else []
        self.fix_flex_players()
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
        self.get_bench_heroes()

    def fix_flex_players(self):  # convert position text for 'RB/WR/TE' to 'FLX'
        for player in self.lineup:
            player.slot_position = 'FLX' if player.slot_position == 'RB/WR/TE' else player.slot_position
            for i, position in enumerate(player.eligibleSlots):
                player.eligibleSlots[i] = 'FLX' if position == 'RB/WR/TE' else position
        for player in self.opponent_lineup:
            player.slot_position = 'FLX' if player.slot_position == 'RB/WR/TE' else player.slot_position
            for i, position in enumerate(player.eligibleSlots):
                player.eligibleSlots[i] = 'FLX' if position == 'RB/WR/TE' else position

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

    def get_bench_heroes(self):  # bench players that scored 25+ points and outscored starters at their position
        self.bench_heroes = list()
        bench_over_25 = list()
        starters = list()
        for player in self.lineup:
            if player.slot_position != 'BE' and player.slot_position != 'IR':  # starting players
                starters.append(player)
                starters.sort(key = lambda p: p.slot_position, reverse=True)  # HACK: put "FLX" at the end of the list
            elif player.slot_position == 'BE' and player.points >= 25:  # bench players that scored 25+
                player.eligibleSlots.sort()
                bench_over_25.append(player)
        for player in bench_over_25:  # loop through the bench players over 25 points
            for starter in starters:  # loop through starters
                if (
                    player.points > starter.points  # bench player scored more than starter
                    and starter.slot_position in player.eligibleSlots  # bench player could have played starter's position
                ):
                    if player not in [p['player'] for p in self.bench_heroes]:  # avoid duplicates
                        self.bench_heroes.append({'player': player,'position': starter.slot_position})
        self.bench_heroes.sort(key = lambda p: p['player'].points, reverse=True)