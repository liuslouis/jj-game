def format_cards(str_cards):
    """
    Format from 'As1' into CSS class labels for html render
    Input:
    - str_cards: list of string card labels
    Return:
    - cards: list of card dict
    """
    suits = {'s':'spades', 'c':'clubs', 'h':'hearts', 'd':'diams'}
    cssclass_ranks = {'1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7',
             '8':'8', '9':'9', 'T':'10', 'J':'j', 'Q':'q', 'K':'k', 'A':'a'}
    cards = []
    for c in str_cards:
        if c[1] != 'j': # not joker
            card = {}
            card['label'] = c
            card['rank'] = c[0]
            card['suit'] = r'&'+suits[c[1]]+';'
            card['cssclass'] = 'card rank-'+cssclass_ranks[c[0]]+' '+suits[c[1]]
            cards.append(card)
        else: # joker
            card = {}
            card['label'] = c
            card['rank'] = c[0]
            card['suit'] = 'Joker'
            card['cssclass'] = "card big joker" if c[0] == 'U' else "card little joker"
            cards.append(card)
    #print(cards)
    return cards
