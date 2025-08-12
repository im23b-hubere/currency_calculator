from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if target_currency in data['rates']:
            rate = data['rates'][target_currency]
            return rate
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

def validate_currency(currency):
    """Überprüft ob eine Währung gültig ist"""
    valid_currencies = [
        'EUR', 'USD', 'CHF', 'GBP', 'JPY', 'CAD', 'AUD', 'CNY', 'NZD', 'SEK',
        'NOK', 'DKK', 'PLN', 'CZK', 'HUF', 'RUB', 'TRY', 'BRL', 'MXN', 'INR',
        'KRW', 'SGD', 'HKD', 'THB', 'MYR', 'IDR', 'PHP', 'VND', 'BDT', 'PKR'
    ]
    return currency.upper() in valid_currencies

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        base_currency = data.get('base_currency', '').upper()
        target_currency = data.get('target_currency', '').upper()
        amount = float(data.get('amount', 0))
        
        # Validiere Währungen
        if not validate_currency(base_currency):
            return jsonify({
                'success': False,
                'message': f'"{base_currency}" ist keine gültige Währung.'
            })
        
        if not validate_currency(target_currency):
            return jsonify({
                'success': False,
                'message': f'"{target_currency}" ist keine gültige Währung.'
            })
        
        if amount <= 0:
            return jsonify({
                'success': False,
                'message': 'Der Betrag muss größer als 0 sein.'
            })
        
        exchange_rate = get_exchange_rate(base_currency, target_currency)
        
        if exchange_rate is None:
            return jsonify({
                'success': False,
                'message': f'Fehler beim Abrufen des Wechselkurses für {base_currency} → {target_currency}.'
            })
        
        converted_amount = amount * exchange_rate
        
        return jsonify({
            'success': True,
            'result': f'{amount} {base_currency} sind {converted_amount:.2f} {target_currency}',
            'rate': f'Wechselkurs: 1 {base_currency} = {exchange_rate:.4f} {target_currency}'
        })
        
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'Bitte geben Sie einen gültigen Betrag ein.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ein Fehler ist aufgetreten: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True)
