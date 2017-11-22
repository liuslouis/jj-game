class Hand:
    def __init__(self, jj=False):
        self.jj = jj

class Game:
    def __init__(self):
        self.active = 0
        self.hasoppo = {} # 有头没头
        self.readyburn = {} # 谁能烧

    def set_burn_status(self, player, status):
        """
        Interact with front and server to set if a player wanna burn
        """
        self.readyburn[player] = status

    def get_burn_status(self, player):
        """
        Get those ready to burn in correct order after the hand of @player
        """
        return [(player+i)%6 for i in range(5) if self.readyburn.get((player+i)%6, False)]

    def play(self, player, hand):
        # TODO:
        #   1. 如果一个人走了， self.hasoppo[(player+3)%6] = False
        print('Who Ready to Burn:', self.get_burn_status(player))
        self.set_next_player(player, hand.jj and self.hasoppo.get(player, True))

    def set_next_player(self, player, jj):
        if not jj:
            # TODO: 没有够级下个人是谁
            self.active = 1
        else:
            # TODO: 有够级下个人是谁
            self.active = 2

        print('Next:', self.active, '\n')


if __name__ == '__main__':
    g = Game()
    # test1
    g.play(player=0, hand=Hand(jj=False))

    # test2
    g.set_burn_status(1, True)
    g.set_burn_status(4, True)
    g.play(player=3, hand=Hand(jj=True))
