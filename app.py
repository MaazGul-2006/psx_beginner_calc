import sqlite3
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)
DATABASE = 'portfolio.db'

# --- Database Setup ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                shares REAL NOT NULL,
                buy_price REAL NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        db.commit()

# Initialize the SQLite database on startup
init_db()

# --- Broker Fee Profiles ---
# Rates based on standard PSX guidelines and online broker tariff schedules
BROKER_PROFILES = {
    'standard': {'rate': 0.0015, 'min_fee': 0.03, 'name': 'Standard PSX (0.15%)'},
    'ktrade': {'rate': 0.0012, 'min_fee': 0.02, 'name': 'KTrade Online (0.12%)'},
    'akd': {'rate': 0.0015, 'min_fee': 0.03, 'name': 'AKD Securities (0.15%)'},
    'arifhabib': {'rate': 0.0010, 'min_fee': 0.02, 'name': 'Arif Habib Ltd (0.10%)'}
}

SST_RATE = 0.13             # 13% Sindh Sales Tax on commission
FILER_CGT = 0.15            # 15% CGT for Filers
NON_FILER_CGT = 0.25        # 25% CGT for Non-Filers
FILER_DIV_TAX = 0.15        # 15% Withholding Tax on Dividends
NON_FILER_DIV_TAX = 0.30    # 30% Withholding Tax on Dividends

def calculate_broker_commission(value, shares, broker_key):
    profile = BROKER_PROFILES.get(broker_key, BROKER_PROFILES['standard'])
    calculated_comm = value * profile['rate']
    min_floor_comm = shares * profile['min_fee']
    base_comm = max(calculated_comm, min_floor_comm)
    sst = base_comm * SST_RATE
    return base_comm + sst

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# 1. Average Down Calculator
@app.route('/average-down', methods=['POST'])
def average_down():
    try:
        b1_shares = float(request.form.get('b1_shares', 0))
        b1_price = float(request.form.get('b1_price', 0))
        b2_shares = float(request.form.get('b2_shares', 0))
        b2_price = float(request.form.get('b2_price', 0))

        total_shares = b1_shares + b2_shares
        total_cost = (b1_shares * b1_price) + (b2_shares * b2_price)
        avg_price = total_cost / total_shares if total_shares > 0 else 0

        return jsonify({
            'avg_result': {
                'total_shares': total_shares,
                'total_cost': round(total_cost, 2),
                'avg_price': round(avg_price, 2)
            }
        })
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400

# 2. Break-Even Price Finder (Supports Custom Brokers)
@app.route('/break-even', methods=['POST'])
def break_even():
    try:
        buy_price = float(request.form.get('buy_price', 0))
        shares = float(request.form.get('shares', 0))
        broker_key = request.form.get('broker', 'standard')
        
        buy_value = buy_price * shares
        buy_fees = calculate_broker_commission(buy_value, shares, broker_key)
        total_invested = buy_value + buy_fees

        # Estimate round-trip requirement including sell-side commissions
        profile = BROKER_PROFILES.get(broker_key, BROKER_PROFILES['standard'])
        effective_rate = profile['rate'] * (1 + SST_RATE)
        break_even_total = total_invested / (1 - effective_rate)
        break_even_price = break_even_total / shares if shares > 0 else 0

        return jsonify({
            'breakeven_result': {
                'total_invested': round(total_invested, 2),
                'break_even_price': round(break_even_price, 2),
                'total_fees': round(break_even_total - buy_value, 2)
            }
        })
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400

# 3. Dividend & Yield Calculator
@app.route('/dividend', methods=['POST'])
def dividend():
    try:
        shares = float(request.form.get('shares', 0))
        dps = float(request.form.get('dps', 0))
        market_price = float(request.form.get('market_price', 0))
        tax_status = request.form.get('tax_status', 'filer')

        gross_dividend = shares * dps
        tax_rate = FILER_DIV_TAX if tax_status == 'filer' else NON_FILER_DIV_TAX
        tax_deducted = gross_dividend * tax_rate
        net_dividend = gross_dividend - tax_deducted
        dividend_yield = (dps / market_price * 100) if market_price > 0 else 0

        return jsonify({
            'div_result': {
                'gross_dividend': round(gross_dividend, 2),
                'tax_deducted': round(tax_deducted, 2),
                'net_dividend': round(net_dividend, 2),
                'yield': round(dividend_yield, 2)
            }
        })
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400

# 4. Capital Gains & Net Profit Calculator (Supports Custom Brokers)
@app.route('/cgt', methods=['POST'])
def cgt():
    try:
        buy_price = float(request.form.get('buy_price', 0))
        sell_price = float(request.form.get('sell_price', 0))
        shares = float(request.form.get('shares', 0))
        tax_status = request.form.get('tax_status', 'filer')
        broker_key = request.form.get('broker', 'standard')

        buy_value = buy_price * shares
        sell_value = sell_price * shares

        buy_fees = calculate_broker_commission(buy_value, shares, broker_key)
        sell_fees = calculate_broker_commission(sell_value, shares, broker_key)
        total_brokerage_cost = buy_fees + sell_fees

        gross_profit = sell_value - buy_value
        net_capital_gain = max(0, gross_profit - total_brokerage_cost)

        cgt_rate = FILER_CGT if tax_status == 'filer' else NON_FILER_CGT
        cgt_tax = net_capital_gain * cgt_rate if gross_profit > 0 else 0

        net_profit = gross_profit - total_brokerage_cost - cgt_tax

        return jsonify({
            'cgt_result': {
                'gross_profit': round(gross_profit, 2),
                'brokerage_fees': round(total_brokerage_cost, 2),
                'cgt_tax': round(cgt_tax, 2),
                'net_profit': round(net_profit, 2)
            }
        })
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400

# --- 5. Portfolio Tracker Endpoints ---
@app.route('/portfolio/add', methods=['POST'])
def portfolio_add():
    try:
        symbol = request.form.get('symbol', '').upper()
        shares = float(request.form.get('shares', 0))
        buy_price = float(request.form.get('buy_price', 0))
        date = request.form.get('date', '')

        db = get_db()
        db.execute('INSERT INTO portfolio (symbol, shares, buy_price, date) VALUES (?, ?, ?, ?)',
                   (symbol, shares, buy_price, date))
        db.commit()
        return jsonify({'success': True})
    except Exception:
        return jsonify({'error': 'Failed to save transaction'}), 400

@app.route('/portfolio/list', methods=['GET'])
def portfolio_list():
    db = get_db()
    cursor = db.execute('SELECT * FROM portfolio ORDER BY id DESC')
    rows = cursor.fetchall()
    items = []
    total_invested = 0
    for r in rows:
        cost = r['shares'] * r['buy_price']
        total_invested += cost
        items.append({
            'id': r['id'],
            'symbol': r['symbol'],
            'shares': r['shares'],
            'buy_price': r['buy_price'],
            'total_cost': round(cost, 2),
            'date': r['date']
        })
    return jsonify({'items': items, 'total_portfolio_cost': round(total_invested, 2)})

@app.route('/portfolio/delete/<int:item_id>', methods=['POST'])
def portfolio_delete(item_id):
    db = get_db()
    db.execute('DELETE FROM portfolio WHERE id = ?', (item_id,))
    db.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)