from flask import Flask, render_template, request
from decimal import Decimal, InvalidOperation
import calc_helper as calc

app = Flask(__name__)

def validate_and_convert(value, default):
    """Validate the input and convert it to Decimal, or return a default value."""
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        return Decimal(default)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    error = None
    if request.method == 'POST':
        try:
            # Fetch and validate inputs
            back_stake = validate_and_convert(request.form.get('back_stake', '5'), '5')
            back_odds = validate_and_convert(request.form.get('back_odds', '6'), '6')
            min_lay_odds = validate_and_convert(request.form.get('min_lay_odds', '4'), '4')
            max_lay_odds = validate_and_convert(request.form.get('max_lay_odds', '4.5'), '4.5')
            lay_commission = validate_and_convert(request.form.get('lay_commission', '5'), '5')
            step = validate_and_convert(request.form.get('step', '0.1'), '0.1')

            # Calculate results if form submission is successful
            results = calc.display_results_for_range(back_stake, back_odds, min_lay_odds, max_lay_odds, lay_commission, step)
        except InvalidOperation:
            # Handle potential conversion errors when input is not a valid Decimal
            error = 'Invalid input format. Please ensure all inputs are valid numbers.'

    # Render the index.html whether it's a GET request or a POST request that has processed results
    return render_template('index.html', results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True)