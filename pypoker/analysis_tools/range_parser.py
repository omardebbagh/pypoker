from pypoker.utils import *
from typing import List


class RangeParser:
    SUITED_CONNECTORS = ['s']  # Denotes suited hands like "A5s"
    OFFSUIT_CONNECTORS = ['o']  # Denotes offsuit hands like "A5o"

    @staticmethod
    def parse_hand_range(hand_range: str) -> List[str]:
        """
        Parse a string of a poker hand range into individual hands.
        Example: "22+, AKs, A2s-A5s" -> ["22", "33", "44", ..., "AKs", "A2s", ..., "A5s"]
        """
        hands = []
        segments = hand_range.split(',')
        for segment in segments:
            segment = segment.strip()
            if '-' in segment:
                hands.extend(RangeParser.expand_range(segment))
            elif '+' in segment:
                hands.extend(RangeParser.expand_plus(segment))
            else:
                hands.append(segment)
        return hands

    @staticmethod
    def expand_plus(segment: str) -> List[str]:
        """
        Expand a hand with a "+" sign.
        Example: "88+" -> ["88", "99", "TT", "JJ", "QQ", "KK", "AA"]
        """
        rank_order = Card.RANKS
        start_rank = segment[:2]  # First two characters, e.g., "88"
        start_index = rank_order.index(start_rank[0])
        pairs = [f"{rank_order[i]}{rank_order[i]}" for i in range(start_index, len(rank_order))]
        return pairs

    @staticmethod
    def expand_range(segment: str) -> List[str]:
        """
        Expand a range notation like "A2s-A5s" into ["A2s", "A3s", "A4s", "A5s"].
        """
        start_hand, end_hand = segment.split('-')
        assert len(start_hand) == len(end_hand), "Invalid range notation"

        if len(start_hand) == 3:  # For suited or offsuit notations like "A2s"
            suit = start_hand[-1]  # Get the last character 's' or 'o'
            rank_order = Card.RANKS
            start_index = rank_order.index(start_hand[1])
            end_index = rank_order.index(end_hand[1]) + 1
            expanded_hands = [f"{start_hand[0]}{rank_order[i]}{suit}" for i in range(start_index, end_index)]
            return expanded_hands

        return []

    @staticmethod
    def generate_combinations(hand_range_str: str) -> List[Hand]:
        """
        Generate all possible hand combinations for a range string like "AA, KK, AKs, AKo",
        """
        hands_notation = RangeParser.parse_hand_range(hand_range_str)
        all_combinations = []
        for hand_notation in hands_notation:
            combinations = RangeParser.generate_combinations_from_notation(hand_notation)
            all_combinations.extend(combinations)
        return all_combinations

    @staticmethod
    def generate_combinations_from_notation(hand_notation: str) -> List[Hand]:
        """
        Return all possible card combinations for a hand notation like "AKs" or "55",
        """
        if len(hand_notation) == 2:  # Pocket pairs like "AA"
            rank1, rank2 = hand_notation[0], hand_notation[1]
            assert rank1 == rank2, "Invalid pocket pair notation"
            return [
                Hand([Card(rank1, suit1), Card(rank2, suit2)])
                for suit1 in Card.SUITS
                for suit2 in Card.SUITS
                if suit1 < suit2  # Avoid duplicates by ensuring suit1 < suit2
            ]
        elif len(hand_notation) == 3:
            rank1, rank2, connector = hand_notation[0], hand_notation[1], hand_notation[2]
            if connector == 's':  # Suited
                return [
                    Hand([Card(rank1, suit), Card(rank2, suit)])
                    for suit in Card.SUITS
                ]
            elif connector == 'o':  # Offsuit
                return [
                    Hand([Card(rank1, suit1), Card(rank2, suit2)])
                    for suit1 in Card.SUITS
                    for suit2 in Card.SUITS
                    if suit1 != suit2
                ]
        return []
