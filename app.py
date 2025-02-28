import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
import io

app = Flask(__name__)

@app.route('/')  
def home():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    metal = data.get("metal")
    property1 = data.get("property1")
    property2 = data.get("property2")

    # Sample logic for damage factor calculation
    damage_factor = (len(metal) + len(property1) + len(property2)) * 10

    # Recommendation based on damage factor
    recommendation = "Suitable for spacecraft" if damage_factor < 100 else "Not suitable for spacecraft"

    response = {
        "damage_factor": damage_factor,
        "recommendation": recommendation
    }
    return jsonify(response)

@app.route('/generate_graph')
def generate_graph():
    # Generate sample data for visualization
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.random.uniform(0.8, 1.2, size=len(x))  # Simulated data variation

    plt.figure(figsize=(6, 4))
    plt.plot(x, y, label="Radiation Interaction")
    plt.xlabel("Radiation Intensity")
    plt.ylabel("Damage Response")
    plt.title("Radiation Interaction with Metal")
    plt.legend()
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
