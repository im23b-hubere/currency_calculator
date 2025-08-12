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
        
        if not base_currency or not target_currency or amount <= 0:
            return jsonify({
                'success': False,
                'message': 'Bitte geben Sie gültige Werte ein.'
            })
        
        exchange_rate = get_exchange_rate(base_currency, target_currency)
        
        if exchange_rate is None:
            return jsonify({
                'success': False,
                'message': f'Die Währung {target_currency} ist nicht verfügbar oder ein Fehler ist aufgetreten.'
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
