from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# Dummy simulation function
def simulate_radiation(metal, radiation, temperature, intensity):
    # Replace this with actual simulation logic
    damage_factor = np.random.uniform(0.1, 0.9)
    result = f"{metal.capitalize()} exposed to {radiation} radiation at {temperature}K and {intensity} W/m² has a damage factor of {damage_factor:.2f}."

    # Dummy plot data
    plot_data = [{
        'z': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        'type': 'surface'
    }]

    return result, plot_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    result, plot_data = simulate_radiation(data['metal'], data['radiation'], data['temperature'], data['intensity'])
    return jsonify({'result': result, 'plot_data': plot_data})

if __name__ == '_main_':
    app.run(debug=True)
