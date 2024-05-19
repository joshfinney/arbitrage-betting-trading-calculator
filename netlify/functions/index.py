from flask import Flask, render_template, request
import json
from decimal import Decimal, InvalidOperation
import calc_helper as calc

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handler(event, context):
    results = []
    if event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        try:
            # Fetch and validate inputs
            back_stake = body.get('back_stake', '5')
            back_odds = body.get('back_odds', '6')
            min_lay_odds = body.get('min_lay_odds', '4')
            max_lay_odds = body.get('max_lay_odds', '4.5')
            lay_commission = body.get('lay_commission', '5')
            step = body.get('step', '0.1')

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
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid input format.'})
            }

    return {
        'statusCode': 200,
        'body': json.dumps({'results': results})
    }

if __name__ == '__main__':
    app.run(debug=True)