import requests

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
            print(f"Die Währung {target_currency} ist nicht verfügbar.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None
base_currency = input("Gib die Basiswährung ein (z.B. CHF): ").upper()
target_currency = input("Gib die Zielwährung ein (z.B. EUR): ").upper()
amount = float(input(f"Gib den Betrag in {base_currency} ein: "))
exchange_rate = get_exchange_rate(base_currency, target_currency)
if exchange_rate is not None:
    converted_amount = amount * exchange_rate
    print(f"{amount} {base_currency} sind {converted_amount:.2f} {target_currency}")
