from flask import Flask, render_template, request

app = Flask(__name__)

# PSX Standard Defaults
BROKERAGE_RATE = 0.0015     # 0.15% standard broker commission
SST_RATE = 0.13             # 13% Sindh/Provincial Sales Tax on commission
FILER_CGT = 0.15            # 15% CGT for Filers
NON_FILER_CGT = 0.25        # 25% CGT for Non-Filers
FILER_DIV_TAX = 0.15        # 15% Withholding Tax on Dividends
NON_FILER_DIV_TAX = 0.30    # 30% Withholding Tax on Dividends

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

        return render_template('index.html', avg_result={
            'total_shares': total_shares,
            'total_cost': round(total_cost, 2),
            'avg_price': round(avg_price, 2)
        })
    except Exception:
        return render_template('index.html', error="Invalid input in Average Down Calculator")

# 2. Break-Even Price Finder
@app.route('/break-even', methods=['POST'])
def break_even():
    try:
        buy_price = float(request.form.get('buy_price', 0))
        shares = float(request.form.get('shares', 0))
        
        # Total cost including buying commission
        buy_value = buy_price * shares
        buy_comm = buy_value * BROKERAGE_RATE
        buy_tax = buy_comm * SST_RATE
        total_invested = buy_value + buy_comm + buy_tax

        # Selling break-even price per share considering selling commission
        effective_commission_multiplier = 1 - (BROKERAGE_RATE * (1 + SST_RATE))
        break_even_total = total_invested / effective_commission_multiplier
        break_even_price = break_even_total / shares if shares > 0 else 0

        return render_template('index.html', breakeven_result={
            'total_invested': round(total_invested, 2),
            'break_even_price': round(break_even_price, 2),
            'total_fees': round(break_even_total - buy_value, 2)
        })
    except Exception:
        return render_template('index.html', error="Invalid input in Break-Even Calculator")

# 3. Dividend & Yield Calculator
@app.route('/dividend', methods=['POST'])
def dividend():
    try:
        shares = float(request.form.get('shares', 0))
        dps = float(request.form.get('dps', 0)) # Dividend Per Share (Rs)
        market_price = float(request.form.get('market_price', 0))
        tax_status = request.form.get('tax_status', 'filer')

        gross_dividend = shares * dps
        tax_rate = FILER_DIV_TAX if tax_status == 'filer' else NON_FILER_DIV_TAX
        tax_deducted = gross_dividend * tax_rate
        net_dividend = gross_dividend - tax_deducted
        
        dividend_yield = (dps / market_price * 100) if market_price > 0 else 0

        return render_template('index.html', div_result={
            'gross_dividend': round(gross_dividend, 2),
            'tax_deducted': round(tax_deducted, 2),
            'net_dividend': round(net_dividend, 2),
            'yield': round(dividend_yield, 2)
        })
    except Exception:
        return render_template('index.html', error="Invalid input in Dividend Calculator")

# 4. Capital Gains & Fees Calculator
@app.route('/cgt', methods=['POST'])
def cgt():
    try:
        buy_price = float(request.form.get('buy_price', 0))
        sell_price = float(request.form.get('sell_price', 0))
        shares = float(request.form.get('shares', 0))
        tax_status = request.form.get('tax_status', 'filer')

        buy_value = buy_price * shares
        sell_value = sell_price * shares

        # Brokerage fees (buy + sell side)
        total_comm = (buy_value + sell_value) * BROKERAGE_RATE
        total_sst = total_comm * SST_RATE
        total_brokerage_cost = total_comm + total_sst

        gross_profit = sell_value - buy_value
        net_capital_gain = max(0, gross_profit - total_brokerage_cost)

        cgt_rate = FILER_CGT if tax_status == 'filer' else NON_FILER_CGT
        cgt_tax = net_capital_gain * cgt_rate if gross_profit > 0 else 0

        net_profit = gross_profit - total_brokerage_cost - cgt_tax

        return render_template('index.html', cgt_result={
            'gross_profit': round(gross_profit, 2),
            'brokerage_fees': round(total_brokerage_cost, 2),
            'cgt_tax': round(cgt_tax, 2),
            'net_profit': round(net_profit, 2)
        })
    except Exception:
        return render_template('index.html', error="Invalid input in CGT Calculator")

if __name__ == '__main__':
    app.run(debug=True)