from pypoker.analysis_tools.range_vs_range_equity import EquityCalculator


def main():
    calculator = EquityCalculator()

    # Example 1: Preflop Equity
    range1 = "AA, KK, QQ"
    range2 = "AKs, AKo, AQs, AQo"
    print(f"Calculating preflop equity between Range1: {range1} and Range2: {range2}")
    preflop_equity = calculator.calculate_preflop_equity(range1, range2, num_simulations=10000)
    print(f"Preflop Equity Results: {preflop_equity}")
    calculator.visualize_equity(preflop_equity, title="Preflop Equity Comparison")

    # Example 2: Flop Equity
    range1 = "AKs, AQs, KQs, QJs"
    range2 = "AQo, KQo, JTs, T9s"
    community_cards_flop = "AhKhQd"  # Example community cards on the flop
    print(f"\nCalculating flop equity between Range1: {range1} and Range2: {range2} with Community Cards: {community_cards_flop}")
    flop_equity = calculator.calculate_flop_equity(range1, range2, community_cards_flop, num_simulations=10000)
    print(f"Flop Equity Results: {flop_equity}")
    calculator.visualize_equity(flop_equity, title="Flop Equity Comparison")

    # Example 3: Turn Equity
    range1 = "JJ+, ATs+, KQs"
    range2 = "TT, 99, 88, AQo"
    community_cards_turn = "AsKd7c5h"  # Example community cards on the turn
    print(f"\nCalculating turn equity between Range1: {range1} and Range2: {range2} with Community Cards: {community_cards_turn}")
    turn_equity = calculator.calculate_turn_equity(range1, range2, community_cards_turn, num_simulations=10000)
    print(f"Turn Equity Results: {turn_equity}")
    calculator.visualize_equity(turn_equity, title="Turn Equity Comparison")


if __name__ == "__main__":
    main()

