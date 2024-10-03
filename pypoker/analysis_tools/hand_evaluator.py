from collections import defaultdict
from typing import Tuple, List


class HandEvaluator:
    HAND_RANKS = [
        "High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight",
        "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"
    ]

    @staticmethod
    def evaluate_hand(cards) -> Tuple:
        """
        Evaluate the strength of a 7-card hand.
        Returns a tuple where the first element is the rank index (higher is better),
        and the second element is a list of high card values for tiebreakers.
        """
        ranks = sorted([card.value for card in cards], reverse=True)
        suits = [card.suit for card in cards]
        rank_counts = defaultdict(int)
        for rank in ranks:
            rank_counts[rank] += 1

        is_flush = any(suits.count(suit) >= 5 for suit in set(suits))
        is_straight, high_straight = HandEvaluator.is_straight(ranks)
        if is_flush:
            flush_suit = HandEvaluator.get_flush_suit(suits)
            flush_cards = sorted([card.value for card in cards if card.suit == flush_suit], reverse=True)
            is_straight_flush, high_straight_flush = HandEvaluator.is_straight(flush_cards)
            if is_straight_flush:
                if high_straight_flush == 14:
                    return (9, [14])  # Royal Flush
                return (8, [high_straight_flush])  # Straight Flush

        four = HandEvaluator.get_n_of_a_kind_highest(rank_counts, 4)
        if four:
            kicker = HandEvaluator.get_kickers(ranks, exclude=[four])
            return (7, [four] + kicker)

        three = HandEvaluator.get_n_of_a_kind_highest(rank_counts, 3)
        pairs = HandEvaluator.get_all_n_of_a_kind(rank_counts, 2)
        if three and len(pairs) >= 1:
            return (6, [three] + [max(pairs)])  # Full House

        if is_flush:
            return (5, flush_cards[:5])

        if is_straight:
            return (4, [high_straight])

        if three:
            kicker = HandEvaluator.get_kickers(ranks, exclude=[three])
            return (3, [three] + kicker[:2])

        if len(pairs) >= 2:
            top_two = sorted(pairs, reverse=True)[:2]
            return (2, top_two + HandEvaluator.get_kickers(ranks, exclude=top_two)[:1])

        if len(pairs) == 1:
            return (1, [pairs[0]] + HandEvaluator.get_kickers(ranks, exclude=[pairs[0]])[:3])

        return (0, ranks[:5])  # High Card

    @staticmethod
    def is_straight(ranks):
        """Check if the ranks form a straight. Returns (True/False, high_card)."""
        unique_ranks = sorted(set(ranks), reverse=True)
        # Check for Ace-low straight (A-2-3-4-5)
        if unique_ranks[:5] == [14, 5, 4, 3, 2]:
            return True, 5
        for i in range(len(unique_ranks) - 4):
            window = unique_ranks[i:i + 5]
            if window[0] - window[4] == 4:
                return True, window[0]
        return False, None

    @staticmethod
    def get_flush_suit(suits):
        """Return the suit that makes a flush."""
        for suit in set(suits):
            if suits.count(suit) >= 5:
                return suit
        return None

    @staticmethod
    def get_n_of_a_kind_highest(rank_counts, n):
        """Return the highest rank that has exactly n of a kind."""
        pairs = [rank for rank, count in rank_counts.items() if count == n]
        if pairs:
            return max(pairs)
        return None

    @staticmethod
    def get_all_n_of_a_kind(rank_counts, n) -> List:
        """Return a list of all ranks that have exactly n of a kind."""
        return [rank for rank, count in rank_counts.items() if count == n]

    @staticmethod
    def get_kickers(ranks, exclude=[]) -> List:
        """Return the kicker cards, excluding specified ranks."""
        return [rank for rank in ranks if rank not in exclude]

    @staticmethod
    def compare_hands(hand1, hand2):

        if hand1[0] > hand2[0]:
            return 1
        elif hand1[0] < hand2[0]:
            return -1
        else:
            # Compare high cards
            for a, b in zip(hand1[1], hand2[1]):
                if a > b:
                    return 1
                elif a < b:
                    return -1
            return 0  # Tie
