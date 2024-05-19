from decimal import Decimal, getcontext, ROUND_HALF_UP
from tabulate import tabulate

# Set the precision for Decimal operations
getcontext().prec = 20

def calculate_matched_betting(back_stake, back_odds, lay_odds, lay_commission):
    """
    Calculate various metrics for matched betting.
    
    Parameters:
    - back_stake (Decimal): The amount staked on the back bet.
    - back_odds (Decimal): The odds of the back bet.
    - lay_odds (Decimal): The odds of the lay bet.
    - lay_commission (Decimal): The commission rate of the lay bet.
    
    Returns:
    dict: A dictionary with keys 'Lay Stake', 'Liability', 'Profit if Bookmaker Bet Wins',
          'Profit if Exchange Lay Wins', and 'Match Rating'.
    
    Raises:
    ValueError: If lay_odds is less than or equal to lay_commission.
    """
    
    # Ensure all inputs are of type Decimal
    back_stake = Decimal(back_stake)
    back_odds = Decimal(back_odds)
    lay_odds = Decimal(lay_odds)
    lay_commission = Decimal(lay_commission) / 100  # Convert percentage to decimal for calculation

    # Validate inputs
    if lay_odds <= lay_commission:
        raise ValueError("Lay odds must be greater than lay commission to avoid division by zero.")

    # Calculate Lay Stake
    lay_stake = (back_odds / (lay_odds - lay_commission)) * back_stake
    
    # Calculate Liability
    liability = lay_stake * (lay_odds - 1)
    
    # Calculate Bookmaker Bet Win
    bookmaker_bet_win = (back_odds - 1) * back_stake - (lay_odds - 1) * lay_stake
    
    # Calculate Exchange Lay Win
    exchange_lay_win = lay_stake * (1 - lay_commission) - back_stake
    
    # Calculate Match Rating
    match_rating = (bookmaker_bet_win / back_stake) * 100 + 100

    return {
        "Lay Stake": lay_stake.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        "Liability": liability.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        "Profit if Bookmaker Bet Wins": bookmaker_bet_win.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        "Profit if Exchange Lay Wins": exchange_lay_win.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
        "Match Rating": match_rating.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    }

def display_results_for_range(back_stake, back_odds, min_lay_odds, max_lay_odds, lay_commission, step):
    """
    Generate results for a range of lay odds and display them in a tabulated format.
    
    Parameters:
    - back_stake (Decimal): The amount staked on the back bet.
    - back_odds (Decimal): The odds of the back bet.
    - min_lay_odds (Decimal): The minimum lay odds to start the range.
    - max_lay_odds (Decimal): The maximum lay odds to end the range.
    - lay_commission (Decimal): The commission rate of the lay bet.
    - step (Decimal): The increment step for the lay odds.
    
    Returns:
    list: A list of lists containing the results for each step in the range.
    """
    
    headers = ['Lay Odds', 'Lay Stake (£)', 'Liability (£)', 'Profit if Back Wins (£)', 'Profit if Lay Wins (£)', 'Match Rating (%)']
    results_list = []
    lay_odds = min_lay_odds
    step = Decimal(step)

    while lay_odds <= max_lay_odds:
        try:
            results = calculate_matched_betting(back_stake, back_odds, lay_odds, lay_commission)
            row = [float(lay_odds)] + [float(value) for value in results.values()]
            results_list.append(row)
        except ValueError as e:
            print(f"Skipping lay odds {lay_odds}: {e}")
        lay_odds += step

    return results_list

# Example usage:
# back_stake = Decimal('10')
# back_odds = Decimal('2.5')
# min_lay_odds = Decimal('2.4')
# max_lay_odds = Decimal('2.6')
# lay_commission = Decimal('0.05')
# step = Decimal('0.01')
# results = display_results_for_range(back_stake, back_odds, min_lay_odds, max_lay_odds, lay_commission, step)
# print(tabulate(results, headers=headers))