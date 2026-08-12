#include <iostream>
#include <iomanip>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    // Expecting 4 arguments: shares, buy_price, sell_price, is_filer (1 or 0)
    if (argc < 5) {
        cout << "{\"error\":\"Invalid arguments\"}" << endl;
        return 1;
    }

    double shares = stod(argv[1]);
    double buy_price = stod(argv[2]);
    double sell_price = stod(argv[3]);
    bool is_filer = (string(argv[4]) == "1");

    double total_investment = shares * buy_price;
    double gross_sale = shares * sell_price;
    
    // Standard PSX brokerage commission (approx. 0.15% per side + SECP/LUMS fees)
    double buy_commission = total_investment * 0.0015;
    double sell_commission = gross_sale * 0.0015;
    double total_fees = buy_commission + sell_commission;

    // Gross gain before taxes
    double gross_profit = (gross_sale - total_investment) - total_fees;

    // Pakistan CGT rules: 15% for Active Tax Filers, 30% for Non-Filers
    double cgt_rate = is_filer ? 0.15 : 0.30;
    double cgt_tax = (gross_profit > 0) ? (gross_profit * cgt_rate) : 0.0;
    double net_profit = gross_profit - cgt_tax;

    // Output formatted JSON for Flask API consumption
    cout << "{"
         << "\"invested\":" << fixed << setprecision(2) << total_investment << ","
         << "\"total_fees\":" << total_fees << ","
         << "\"gross_profit\":" << gross_profit << ","
         << "\"cgt_tax\":" << cgt_tax << ","
         << "\"net_profit\":" << net_profit
         << "}" << endl;

    return 0;
}