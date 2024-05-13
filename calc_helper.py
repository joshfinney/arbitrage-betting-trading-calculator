from decimal import Decimal, getcontext, ROUND_HALF_UP
from tabulate import tabulate

# Set the precision for Decimal operations
getcontext().prec = 20

def calculate_matched_betting(back_stake, back_odds, lay_odds, lay_commission):
    lay_stake = (back_stake * back_odds) / (lay_odds - lay_commission / 100)
    liability = (lay_odds - Decimal('1')) * lay_stake
    profit_if_back_wins = (back_stake * (back_odds - Decimal('1'))) - liability
    profit_if_lay_wins = lay_stake * (Decimal('1') - lay_commission / 100) - back_stake
    match_rating = (back_odds / lay_odds) * 100
    return {
        "Lay Stake": lay_stake,
        "Liability": liability,
        "Profit if Bookmaker Bet Wins": profit_if_back_wins,
        "Profit if Exchange Lay Wins": profit_if_lay_wins,
        "Match Rating": match_rating
    }

def display_results_for_range(back_stake, back_odds, min_lay_odds, max_lay_odds, lay_commission, step):
    headers = ['Lay Odds', 'Lay Stake (£)', 'Liability (£)', 'Profit if Back Wins (£)', 'Profit if Lay Wins (£)', 'Match Rating (%)']
    results_list = []
    lay_odds = Decimal(min_lay_odds)
    while lay_odds <= Decimal(max_lay_odds):
        results = calculate_matched_betting(back_stake, back_odds, lay_odds, lay_commission)
        row = [float(lay_odds)] + [float(x) for x in results.values()]
        results_list.append(row)
        lay_odds += Decimal(step)
    return results_list  # Changed from print to return for use in Flask app