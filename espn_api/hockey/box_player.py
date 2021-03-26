from .player import Player

class BoxPlayer(Player):
    '''player with extra data from a matchup'''
    def __init__(self, data, pro_schedule):
        super(BoxPlayer, self).__init__(data)
        pass