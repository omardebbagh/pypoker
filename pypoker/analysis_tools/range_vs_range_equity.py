from collections import defaultdict
import random
import matplotlib.pyplot as plt
from typing import Dict
from pypoker.utils import *
from pypoker.analysis_tools.hand_evaluator import HandEvaluator
from pypoker.analysis_tools.range_parser import RangeParser


class EquityCalculator:
    def __init__(self):
        self.deck = [Card(rank, suit) for rank in Card.RANKS for suit in Card.SUITS]

    def calculate_preflop_equity(self, range1_str, range2_str, num_simulations=10000) -> Dict[str, float]:
        """
        Calculate equity preflop between two ranges.
        Uses Monte Carlo simulation for performance.
        """

        range1_combinations = RangeParser.generate_combinations(range1_str)
        range2_combinations = RangeParser.generate_combinations(range2_str)

        total_simulations = num_simulations
        valid_simulations = 0  # Track valid simulations
        wins = defaultdict(int)
        ties = 0

        for _ in range(total_simulations):
            # Shuffle the deck
            deck = self.deck.copy()
            random.shuffle(deck)

            # Draw hands
            hand1 = range1_combinations[random.randint(0, len(range1_combinations) - 1)]
            hand2 = range2_combinations[random.randint(0, len(range2_combinations) - 1)]

            # Ensure no overlapping cards
            if set(hand1.cards) & set(hand2.cards):
                continue  # Skip this simulation

            # Draw community cards
            community = Hand(deck[:5])
            all_cards1 = hand1.cards + community.cards
            all_cards2 = hand2.cards + community.cards

            # Ensure no overlapping with community
            if set(hand1.cards) & set(community.cards) or set(hand2.cards) & set(community.cards):
                continue  # Skip this simulation

            valid_simulations += 1  # Increment valid simulation count

            # Evaluate hands
            eval1 = HandEvaluator.evaluate_hand(all_cards1)
            eval2 = HandEvaluator.evaluate_hand(all_cards2)

            result = HandEvaluator.compare_hands(eval1, eval2)
            if result == 1:
                wins['range1'] += 1
            elif result == -1:
                wins['range2'] += 1
            else:
                ties += 1

        # Avoid division by zero
        if valid_simulations == 0:
            return {'range1': 0, 'range2': 0, 'ties': 0}

        equity_range1 = (wins['range1'] + ties / 2) / valid_simulations * 100
        equity_range2 = (wins['range2'] + ties / 2) / valid_simulations * 100

        return {'range1': equity_range1, 'range2': equity_range2, 'ties': (ties / valid_simulations * 100)}

    def calculate_flop_equity(self, range1_str, range2_str,
                              community_cards_str, num_simulations=10000) -> Dict[str, float]:
        """
        Calculate equity on the flop between two ranges given the community cards.
        community_cards_str: string like "AsKd7c" (exactly 3 community cards)
        """
        # Parse community cards
        community = Hand()
        for i in range(0, len(community_cards_str), 2):
            card_str = community_cards_str[i:i + 2]
            community.add_card(Card.from_string(card_str))

        if len(community) != 3:
            raise ValueError("Exactly 3 community cards (the flop) must be provided.")

        range1_combinations = RangeParser.generate_combinations(range1_str)
        range2_combinations = RangeParser.generate_combinations(range2_str)

        total_simulations = num_simulations
        valid_simulations = 0  # Track valid simulations
        wins = defaultdict(int)
        ties = 0

        for _ in range(total_simulations):
            # Shuffle the deck
            deck = self.deck.copy()
            random.shuffle(deck)

            # Remove community cards from deck
            remaining_deck = [card for card in deck if card not in community.cards]

            # Draw hands
            hand1 = range1_combinations[random.randint(0, len(range1_combinations) - 1)]
            hand2 = range2_combinations[random.randint(0, len(range2_combinations) - 1)]

            # Ensure no overlapping cards
            if (set(hand1.cards) & set(hand2.cards)) or \
                    (set(hand1.cards) & set(community.cards)) or \
                    (set(hand2.cards) & set(community.cards)):
                continue  # Skip this simulation

            # Draw the turn and river cards
            if len(remaining_deck) < 2:
                continue  # Not enough cards to draw the turn and river
            turn = remaining_deck[0]
            river = remaining_deck[1]
            all_community = community.cards + [turn, river]

            valid_simulations += 1  # Increment valid simulation count

            all_cards1 = hand1.cards + all_community
            all_cards2 = hand2.cards + all_community

            # Evaluate hands
            eval1 = HandEvaluator.evaluate_hand(all_cards1)
            eval2 = HandEvaluator.evaluate_hand(all_cards2)

            result = HandEvaluator.compare_hands(eval1, eval2)
            if result == 1:
                wins['range1'] += 1
            elif result == -1:
                wins['range2'] += 1
            else:
                ties += 1

        # Avoid division by zero
        if valid_simulations == 0:
            return {'range1': 0, 'range2': 0, 'ties': 0}

        equity_range1 = (wins['range1'] + ties / 2) / valid_simulations * 100
        equity_range2 = (wins['range2'] + ties / 2) / valid_simulations * 100

        return {'range1': equity_range1, 'range2': equity_range2, 'ties': ties / valid_simulations * 100}

    def calculate_turn_equity(self, range1_str, range2_str, community_cards_str,
                              num_simulations=10000) -> Dict[str, float]:
        """
        Calculate equity on the turn between two ranges given the community cards.
        community_cards_str: string like "AsKd7c5h"
        """
        # Parse community cards
        community = Hand()
        for i in range(0, len(community_cards_str), 2):
            card_str = community_cards_str[i:i + 2]
            community.add_card(Card.from_string(card_str))

        if len(community) != 4:
            raise ValueError("Exactly 4 community cards (flop and turn) must be provided.")

        range1_combinations = RangeParser.generate_combinations(range1_str)
        range2_combinations = RangeParser.generate_combinations(range2_str)

        total_simulations = num_simulations
        valid_simulations = 0  # Track valid simulations
        wins = defaultdict(int)
        ties = 0

        for _ in range(total_simulations):
            # Shuffle the deck
            deck = self.deck.copy()
            random.shuffle(deck)

            # Remove community cards from deck
            remaining_deck = [card for card in deck if card not in community.cards]

            # Draw hands
            hand1 = range1_combinations[random.randint(0, len(range1_combinations) - 1)]
            hand2 = range2_combinations[random.randint(0, len(range2_combinations) - 1)]

            # Ensure no overlapping cards
            if set(hand1.cards) & set(hand2.cards) or set(hand1.cards) & set(community.cards) or set(hand2.cards) & set(
                    community.cards):
                continue  # Skip this simulation

            # Draw the river card
            if len(remaining_deck) < 1:
                continue  # Not enough cards to draw the river
            river = remaining_deck[0]
            all_community = community.cards + [river]

            valid_simulations += 1  # Increment valid simulation count

            all_cards1 = hand1.cards + all_community
            all_cards2 = hand2.cards + all_community

            # Evaluate hands
            eval1 = HandEvaluator.evaluate_hand(all_cards1)
            eval2 = HandEvaluator.evaluate_hand(all_cards2)

            result = HandEvaluator.compare_hands(eval1, eval2)
            if result == 1:
                wins['range1'] += 1
            elif result == -1:
                wins['range2'] += 1
            else:
                ties += 1

        # Avoid division by zero
        if valid_simulations == 0:
            return {'range1': 0, 'range2': 0, 'ties': 0}

        equity_range1 = (wins['range1'] + ties / 2) / valid_simulations * 100
        equity_range2 = (wins['range2'] + ties / 2) / valid_simulations * 100

        return {'range1': equity_range1, 'range2': equity_range2, 'ties': (ties / valid_simulations * 100)}

    def visualize_equity(self, equity_results, title="Equity Comparison"):
        """
        Visualize the equity results using a pie chart.
        equity_results: dict with keys 'range1', 'range2', 'ties'
        """
        labels = ['Range 1', 'Range 2', 'Ties']
        sizes = [equity_results['range1'], equity_results['range2'], equity_results['ties']]
        colors = ['lightgreen', 'red', 'skyblue']
        explode = (0.1, 0.1, 0)  # Explode Range1 and Range2 slices

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=140, explode=explode, shadow=True)
        plt.title(title)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()
