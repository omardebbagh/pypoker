

class Card:
    SUITS = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')

    RANK_VALUES = {rank: value for value, rank in enumerate(RANKS, start=2)}

    def __init__(self, rank: str, suit: str):
        assert rank in Card.RANKS, f"Invalid rank: {rank}"
        assert suit in Card.SUITS, f"Invalid suit: {suit}"
        self.rank = rank
        self.suit = suit
        self.value = Card.RANK_VALUES[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        return self.value < other.value

    def __hash__(self):
        return hash((self.rank, self.suit))

    @staticmethod
    def from_string(card_str: str):
        """Create a card from a string like 'Kh' for King of Hearts."""
        assert len(card_str) == 2 or len(card_str) == 3, f"Invalid card string: {card_str}"
        rank = card_str[:-1]
        suit_char = card_str[-1]

        suit_map = {'h': 'Hearts', 'd': 'Diamonds', 'c': 'Clubs', 's': 'Spades'}
        assert suit_char in suit_map, f"Invalid suit character: {suit_char}"
        return Card(rank, suit_map[suit_char])


class Hand:
    def __init__(self, cards=None):
        """Initialize a hand with a list of Card objects or an empty list."""
        self.cards = cards if cards else []

    def add_card(self, card: Card):
        """Add a card to the hand."""
        assert isinstance(card, Card), "Can only add objects of type Card"
        self.cards.append(card)

    def remove_card(self, card: Card):
        """Remove a card from the hand if it exists."""
        if card in self.cards:
            self.cards.remove(card)

    def get_ranks(self):
        """Return a list of ranks for the current cards in the hand."""
        return [card.rank for card in self.cards]

    def get_suits(self):
        """Return a list of suits for the current cards in the hand."""
        return [card.suit for card in self.cards]

    def __str__(self):
        """Return a string representation of the hand."""
        return ', '.join([str(card) for card in self.cards])

    def __len__(self):
        """Return the number of cards in the hand."""
        return len(self.cards)

    def sort(self):
        """Sort cards in the hand based on their rank value."""
        self.cards.sort(key=lambda card: card.value)
