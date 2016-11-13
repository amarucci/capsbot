class Game(object):
    def __init__(self, name1, name2):
        self.team1 = name1
        self.team2 = name2
        self.score1 = 0
        self.score2 = 0

    def get_score(self):
        return self.score1, self.score2

    def get_names(self):
        return self.team1, self.team2

    def update_score(self, x, y):
        self.score1 += x
        self.score2 += y
