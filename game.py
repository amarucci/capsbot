class Game(object):
    def __init__(self, names, owner, game_id):
        self.players = names
        self.team1 = names[0] + ' & ' + names[1]
        self.team2 = names[2] + ' & ' + names[3]
        self.scores = [0,0,0,0]
        self.owner = owner
        self.game_id = game_id
        self.deuces = false

    def get_score(self):
        return self.scores[0] + self.scores[1], self.scores[2] + self.scores[3]

    def get_individual_scores(self):
        return self.scores

    def get_names(self):
        return self.players

    def get_teams(self):
        return self.team1, self.team2

    def update_score(self, name):
        self.scores[self.players.index(name)] += 1

    def get_owner(self):
        return self.owner
    
    def get_id(self):
        return game_id

    def set_deuces(self):
        self.deuces = true

    def deuces(self):
        return self.deuces
