from flask import Flask, render_template, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

# Determine executable path depending on OS
ENGINE_EXEC = os.path.join(".", "engine", "psx_math.exe" if os.name == "nt" else "psx_math")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/calculate", methods=["POST"])
def calculate():
    try:
        data = request.json
        shares = str(data.get("shares", 0))
        buy = str(data.get("buy", 0))
        sell = str(data.get("sell", 0))
        filer = str(data.get("filer", 1))

        # Execute compiled C++ engine
        result = subprocess.run(
            [ENGINE_EXEC, shares, buy, sell, filer],
            capture_output=True,
            text=True,
            check=True
        )

        output_data = json.loads(result.stdout.strip())
        return jsonify(output_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)