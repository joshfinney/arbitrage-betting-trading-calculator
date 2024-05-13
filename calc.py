from decimal import Decimal, getcontext, ROUND_HALF_UP
from tabulate import tabulate

# Set the precision for Decimal operations
getcontext().prec = 20  # you can adjust this as needed

def calculate_matched_betting(back_stake, back_odds, lay_odds, lay_commission):
    # Ensure inputs are Decimal
    back_stake = Decimal(back_stake)
    back_odds = Decimal(back_odds)
    lay_odds = Decimal(lay_odds)
    lay_commission = Decimal(lay_commission)

    # Calculate Lay Stake using the formula derived earlier
    lay_stake = (back_stake * back_odds) / (lay_odds - lay_commission / 100)
    
    # Calculate Liability
    liability = (lay_odds - Decimal('1')) * lay_stake
    
    # Calculate Profit if the Bookmaker (Back) Bet Wins
    profit_if_back_wins = (back_stake * (back_odds - Decimal('1'))) - liability
    
    # Calculate Profit if the Exchange (Lay) Bet Wins
    profit_if_lay_wins = lay_stake * (Decimal('1') - lay_commission / 100) - back_stake
    
    # Calculate Match Rating
    match_rating = (back_odds / lay_odds) * 100
    
    return {
        "Lay Stake": lay_stake,
        "Liability": liability,
        "Profit if Bookmaker Bet Wins": profit_if_back_wins,
        "Profit if Exchange Lay Wins": profit_if_lay_wins,
        "Match Rating": match_rating
    }

def round_to_nearest_half(num):
    """Round numbers to the nearest half using Decimal."""
    num = Decimal(num)
    return (num * 2).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / 2

def display_results_for_range(back_stake, back_odds, min_lay_odds, max_lay_odds, lay_commission, step):
    headers = ['Lay Odds', 'Lay Stake (£)', 'Liability (£)', 'Profit if Back Wins (£)', 'Profit if Lay Wins (£)', 'Match Rating (%)']
    results_list = []
    
    lay_odds = Decimal(min_lay_odds)
    while lay_odds <= Decimal(max_lay_odds):
        results = calculate_matched_betting(back_stake, back_odds, lay_odds, lay_commission)
        row = [float(lay_odds)] + [float(x) for x in results.values()]
        results_list.append(row)
        lay_odds += Decimal(step)
    
    print(f"Matched Betting Results for Back Stake: {back_stake}, Back Odds: {back_odds}, Commission: {lay_commission}%\n")
    print(tabulate(results_list, headers=headers, floatfmt=".2f", tablefmt="grid"))

back_stake = Decimal('25')
back_odds = Decimal('13')
min_lay_odds = Decimal('14')
max_lay_odds = Decimal('15.5')
lay_commission = Decimal('5')
step = Decimal('0.25')

display_results_for_range(back_stake, back_odds, min_lay_odds, max_lay_odds, lay_commission, step)