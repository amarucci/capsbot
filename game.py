class Game(object):
    score1 = 0
    score2 = 0
    name1 = "Team 1"
    name2 = "Team 2"

    def getscore():
        return "%s: %s \n %s: %s"(name1, score1, name2, score2)
