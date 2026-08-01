# 📈 PSX Beginner Calculator

A modern, responsive multi-tool web application designed for retail investors in the Pakistan Stock Exchange (PSX). Built with **Python/Flask** on the backend and a sleek, mobile-friendly **HTML5/CSS3/JavaScript** frontend supporting persistent Dark Mode.

🔗 **Live Demo:** [https://psx-beginner-calc.vercel.app](https://psx-beginner-calc.vercel.app) *(Replace with your actual Vercel URL)*

---

## ✨ Features

1. **📊 Average Down Calculator:** Calculate your new average holding price and total investment when buying more shares at a different market price.
2. **🎯 Break-Even Price Finder:** Determine the exact target sell price needed to break even after accounting for standard PSX brokerage commissions and Sindh Sales Tax (SST).
3. **💰 Dividend & Yield Calculator:** Compute gross payouts, withholding tax breakdowns (Filer vs. Non-Filer), and net dividend yields based on current market prices.
4. **⚖️ CGT & Net Profit Calculator:** Calculate capital gains tax (CGT), round-trip brokerage fees, and net realized take-home profit.
5. **⚡ Modern UI & UX:** 
   - Clean tabbed navigation interface.
   - Asynchronous backend communication via Fetch API (no page reloads).
   - Responsive design optimized for desktop and mobile devices.
   - Persistent Light/Dark mode toggle.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask, Gunicorn
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, CSS Grid / Flexbox
* **Deployment:** Vercel (Serverless)

---

## 🚀 Local Installation & Setup

Follow these steps to run the project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MaazGul-2006/psx_beginner_calc.git](https://github.com/MaazGul-2006/psx_beginner_calc.git)
   cd psx_beginner_calc
   ```

2. **Create and activate a virtual environment:**
   ```Bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```Bash
    pip install -r requirements.txt  
    ```

4. **Run the Flask application:**
   ```Bash
   python app.py
   ```

5. Open your browser and navigate to http://127.0.0.1:5000. 

## 📂 Project Structure
   
```Plaintext:
psx_beginner_calc/
│
├── app.py                # Flask application backend routes and logic
├── requirements.txt      # Python package dependencies
├── Procfile              # Deployment configuration for production servers
├── templates/
│   └── index.html        # Frontend UI, CSS styles, and JavaScript client logic
└── README.md             # Project documentation 
```
## 👨‍💻 Author

Developed by Muhammad Maaz Gul

BS Data Science Student at FAST-NUCES