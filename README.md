# 📈 PSX Beginner Calculator & Portfolio Tracker

A lightweight web app tailored for retail investors on the **Pakistan Stock Exchange (PSX)**. Built with **Flask** and modern **Vanilla JavaScript**, it offers precision financial calculators with built-in brokerage fees, Sindh Sales Tax (SST), and FBR tax logic.

🚀 **Live Demo:** [psx-beginner-calc.vercel.app](https://psx-beginner-calc.vercel.app/)

---

## Key Features

* **Live PSX Stock Ticker:** Real-time animated market bar displaying popular PSX symbols.
* **Average Down Calculator:** Computes weighted average price and total exposure across multiple buying tranches.
* **Break-Even Price Finder:** Factor in round-trip broker commissions (AKD, KTrade, Arif Habib, etc.) and 13% SST to find your exact zero-loss sell target.
* **Dividend & Yield Engine:** Calculates gross yield and net payout after Filer (15%) or Non-Filer (30%) Withholding Tax (WHT).
* **CGT & Realized Profit Calculator:** Computes net gains after applying tiered Capital Gains Tax (15% Filer / 25% Non-Filer) and brokerage costs.
* **Portfolio Tracker with CSV Export:** Log stock purchases with zero-latency `localStorage` persistence and export your holdings to CSV anytime.
* **Theme Switching:** Dark Mode / Light Mode with seamless theme persistence.

---

## 🛠️ Tech Stack

* **Backend:** Python / Flask
* **Frontend:** HTML5, CSS3 (CSS Variables), JavaScript (ES6+ AJAX)
* **Storage:** Browser `localStorage` (Serverless-compatible persistence)
* **Deployment:** Vercel (Serverless Functions)

---

## 💻 Local Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/MaazGul-2006/psx_beginner_calc.git](https://github.com/MaazGul-2006/psx_beginner_calc.git)
   cd psx_beginner_calc

```

2. **Create a Virtual Environment & Install Dependencies:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install flask

```


3. **Run the Application:**
```bash
python app.py

```


Open `http://127.0.0.1:5000` in your browser.

---

## 📊 Project Screenshots

| Light Mode | Dark Mode |
| --- | --- |
| `screenshots/light.png` | `screenshots/dark.png` |

---

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

```

---
