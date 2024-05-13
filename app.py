from flask import Flask, render_template, request
from decimal import Decimal, InvalidOperation
import calc_helper as calc

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        try:
            # Fetch and validate inputs
            back_stake = request.form.get('back_stake', '5')
            back_odds = request.form.get('back_odds', '6')
            min_lay_odds = request.form.get('min_lay_odds', '4')
            max_lay_odds = request.form.get('max_lay_odds', '4.5')
            lay_commission = request.form.get('lay_commission', '5')
            step = request.form.get('step', '0.1')

            # Convert to Decimal if valid or use default values
            back_stake = Decimal(back_stake) if back_stake.replace('.', '', 1).isdigit() else Decimal('5')
            back_odds = Decimal(back_odds) if back_odds.replace('.', '', 1).isdigit() else Decimal('6')
            min_lay_odds = Decimal(min_lay_odds) if min_lay_odds.replace('.', '', 1).isdigit() else Decimal('4')
            max_lay_odds = Decimal(max_lay_odds) if max_lay_odds.replace('.', '', 1).isdigit() else Decimal('4.5')
            lay_commission = Decimal(lay_commission) if lay_commission.replace('.', '', 1).isdigit() else Decimal('5')
            step = Decimal(step) if step.replace('.', '', 1).isdigit() else Decimal('0.1')

            # Calculate results if form submission is successful
            results = calc.display_results_for_range(back_stake, back_odds, min_lay_odds, max_lay_odds, lay_commission, step)
        except InvalidOperation:
            # Handle potential conversion errors when input is not a valid Decimal
            return render_template('index.html', results=[], error='Invalid input format.')

    # Render the index.html whether it's a GET request or a POST request that has processed results
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)