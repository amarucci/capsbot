class Game(object):
    def __init__(self, names, owner,  chat_id):
        self.players = names
        self.team1 = names[0] + ' & ' + names[1]
        self.team2 = names[2] + ' & ' + names[3]
        self.scores = [0,0,0,0]
        self.d_scores = [0,0,0,0]
        self.owner = owner
        self.deuces = False
        self.chat_id = int(chat_id)

    #used for displaying total scores, takes into account deuces
    def get_score(self):
        if(self.deuces):
            return sum(self.d_scores[0:2]) + 2,sum(self.d_scores[2:4]) + 2
        else:
            return sum(self.scores[0:2]),sum(self.scores[2:4])

    #returns array with players real scores
    def get_individual_scores(self):
        return self.scores

    def get_names(self):
        return self.players

    def get_teams(self):
        return self.team1, self.team2

    def update_score(self, name):
        self.scores[self.players.index(name)] += 1
        self.d_scores[self.players.index(name)] += 1

    def get_owner(self):
        return self.owner

    def set_game_id(self, game_id):
        self.game_id = int(game_id)

    def get_game_id(self):
        return self.game_id

    def get_chat_id(self):
        return self.chat_id

    #returns false when the score doesn't change
    def deuced(self):
        if sum(self.d_scores[0:2]) == sum(self.d_scores[2:4]):
            self.d_scores[0:4] = [0] * len(self.d_scores)
            return True
        else:
            return False

    def set_deuces(self):
        if self.get_score() >= (2,2):
            self.deuces = True
            return True
        else:
            return False

    def get_deuces(self):
        return self.deuces
