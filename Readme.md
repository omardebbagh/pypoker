# pypoker - Poker Texas Holdem Analytical Tools and Poker bot using CFR and MCCFR minimization algorithm for multiple poker versions 

## Project Overview
This project aims to develop multiple analytical tools useful for Texas Holdem poker analysis. For now, it contains a Range Equity Calculator to analyze poker hands and compute their equity in head-to-head or multi-hand scenarios.
By simulating thousands of possible outcomes using Monte Carlo simulations, the tool evaluates hand strengths and calculates winning probabilities against specific ranges.
It supports preflop, post-flop and turn equity calculations providing insights into how hands perform against various board states. 
The calculator has been tested against professional online tools, yielding consistent results with only minor variations, ensuring its accuracy and reliability. 
This project aims also to explore a bot development using CFR and MCCFR algorithms.

## Features
- Hands Parsing: Hand ranges are parsed using standard poker notation (e.g., "TT+, AQs, KTs"), and the tool expands these ranges into all possible card combinations for equity calculation.
- A Notebook was created showing the basic usage of the tools 

## To Do
- Analyze historical hand data and past plays to identify patterns and trends that could improve strategic decision-making.
- Finish building a poker bot using Counterfactual Regret Minimization (CFR) and Monte Carlo CFR (MCCFR) for Kuhn Poker and Limit Hold'em.

## Dependencies 
- Python 3.x
- matplotlib


