
# coding: utf-8

class Hand():
    comparison = dict(zip(
        ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2', '-', '+'], range(0, 15)))

    def __init__(self, cards=[]):
        if not cards:
            self.length = 0
            self.jj = False
        else:
            self.cards = [card[0] for card in cards]
            self.minimum = min(self.cards, key=lambda x: Hand.comparison[x])
            self.base = Hand.comparison[self.minimum]

            if '+' in self.cards:
                self.joker = 2
            elif '-' in self.cards:
                self.joker = 1
            else:
                self.joker = 0

            if len(set(self.cards) - {self.minimum, '2', '-', '+'}):
                self.length = -1
            else:
                self.length = len(self.cards)

            if self.base == 11 and self.length == 1: 
                self.jj = False
            elif self.base + self.length >= 12:
                self.jj = True
            else:
                self.jj = False

    def __gt__(self, other):
        if other.length == 0:
            return True
        elif other.joker == 0:
            return self.length == other.length and self.base > other.base
        else:
            return self.length == other.length and self.base > other.base and self.joker > other.joker


class Game():
    card_list = [k + l for k in [i + j for i in ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
                                 for j in ['s', 'c', 'h', 'd']]
                 + ['-j', '+j']
                 for l in ['1', '2', '3', '4']]

    def __init__(self):
        self.table = []
        self.cards_dist = dict(
            zip(Game.card_list, [-1 for _ in range(0, len(Game.card_list))]))
        self.players = 6
        self.rank = [0 for _ in range(self.players)]
        self.cards_count = [0 for _ in range(self.players)]
        self.distrubute()
        self.active = self.first_player()
        self.last_active = self.active

    def distrubute(self):
        import random
        all_cards = set(Game.card_list)
        for i in range(self.players):
            cards_for_player = random.sample(
                all_cards, len(Game.card_list) // self.players)
            self.draw(i, cards_for_player)
            all_cards -= set(cards_for_player)

    def first_player(self):  # Can be improved
        import random
        return random.sample(range(6), 1)[0]

    def draw(self, player, cards=[]):
        for card in cards:
            if self.cards_dist[card] == -1:
                self.cards_dist[card] = player
                self.cards_count[player] += 1
            else:
                print("Get {} from {}".format(card, self.card_dist[card]))
                self.cards_dist[card] = player
                self.cards_count[player] += 1
        return self.cards_count[player]

    def subtract(self, player, cards=[]):
        for card in cards:
            if self.cards_dist[card] == player:
                self.cards_dist[card] = -1
                self.cards_count[player] -= 1
            else:
                raise ValueError(
                    "{} does not belong to player {}".format(card, player))
        return self.cards_count[player]

    def play(self, player, cards=[]):
        if not player == self.active:
            print("Wrong player, it is player {}'s turn".format(self.active))
            return False
        h = Hand(cards)
        t = Hand(self.table)
        if h.length < 0:
            print("Ilegal hands as {}".format(cards))
            return False
        if t.length == 0 and h.length == 0 and self.cards_count[player] != 0:
            print("You have to play something")
            return False
        if h.length == 0:
            print("Pass")
            self.get_next_player(True, t.jj)
            return True
        if h > t:
            self.table = cards
            if self.subtract(player, cards) == 0:
                self.player_win(player)
            self.get_next_player(False, h.jj or t.jj)
            return True
        else:
            print("Wrong hand")
            return False

    def get_next_player(self, _pass, jj):
        if not _pass:
            self.last_active = self.active
            for i in range(1, 6):
                if self.cards_count[(self.active + i) % 6] != 0:
                    self.active = (self.active + i) % 6
                    print(self.active)
                    break
        if _pass:
            for i in range(1, 6):
                if self.last_active == (self.active + i) % 6:
                    self.table = []
                if self.cards_count[(self.active + i) % 6] != 0:
                    self.active = (self.active + i) % 6
                    break
            raise ValueError("Get_net_player")
        print("Next player is player {}".format(self.active))
        print(self.table)
        print(self.get_cards(self.active))

    def player_win(self, player):
        print("Player {} wins".format(player))
        self.players -= 1
        self.rank[player] = 6 - self.players
        if self.players == 1:
            for i in range(6):
                if self.rank[i] == 0:
                    self.rank[i] = 6
            self.end_game()

    def end_game(self):
        raise ValueError("End of game: {}".format(self.rank))

    def get_cards(self, player):
        cards = list()
        for key in self.cards_dist:
            if self.cards_dist[key] == player:
                cards.append(key)
        cards.sort(key=lambda x: Hand.comparison[x[0]])
        return cards

    def get_table(self):
        self.table.sort(key=lambda x: Hand.comparison[x[0]])
        return self.last_active, self.table

    def get_ncards(self, i):
        return self.cards_count[i]

    def get_round_player_id(self, i):
        return self.active

