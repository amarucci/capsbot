class Game(object):
    def __init__(self, names):
        self.players = names
        self.team1 = names[0] + ' & ' + names[1]
        self.team2 = names[2] + ' & ' + names[3]
        self.scores = [0,0,0,0]

    def get_score(self):
        return self.scores[0] + self.scores[1], self.scores[2] + self.scores[3]

    def get_names(self):
        return self.players

    def get_teams(self):
        return self.team1, self.team2

    def update_score(self, name):
        self.scores[self.players.index(name)] += 1
