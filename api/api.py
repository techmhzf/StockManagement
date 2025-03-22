from flask import Flask, jsonify
import requests

app = Flask(__name__)

def get_stock_price(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    response = requests.get(url)
    data = response.json()
    
    try:
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        return price
    except (KeyError, TypeError, IndexError):
        return None  # Handle errors gracefully

@app.route('/api/stocks')
def fetch_stocks():
    stock_symbols = ["AAPL", "GOOGL", "MSFT", "TSLA"]  # Add your preferred stocks
    stock_data = []

    for symbol in stock_symbols:
        price = get_stock_price(symbol)
        stock_data.append({
            "symbol": symbol,
            "company": symbol,  # You can map symbols to full names
            "price": price if price else "N/A",
            "change": "Updating..."
        })

    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(debug=True)