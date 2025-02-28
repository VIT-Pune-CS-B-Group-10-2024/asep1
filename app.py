from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import numpy as np

app = Flask(__name__)

# Function to fetch data from NIST ESTAR
def fetch_nist_data(metal):
    try:
        url = f"https://physics.nist.gov/PhysRefData/Star/Text/ESTAR{metal}.html"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data from the <pre> tag
        pre_tag = soup.find('pre')
        if not pre_tag:
            raise ValueError("Data not found in <pre> tag.")

        # Parse the data from the <pre> tag
        lines = pre_tag.text.splitlines()
        data = []
        for line in lines[5:]:  # Skip the header lines
            if line.strip():  # Skip empty lines
                columns = line.split()
                if len(columns) >= 6:
                    kinetic_energy = float(columns[0])  # Kinetic Energy (MeV)
                    stopping_power = float(columns[1])  # Stopping Power (MeV cm²/g)
                    csda_range = float(columns[2])  # CSDA Range (g/cm²)
                    data.append({
                        'kinetic_energy': kinetic_energy,
                        'stopping_power': stopping_power,
                        'csda_range': csda_range,
                    })
        return data
    except Exception as e:
        print(f"Error fetching data for {metal}: {e}")
        return None

# Simulation function
def simulate_radiation(metal, property1, property2):
    data = fetch_nist_data(metal)
    if not data:
        return "Failed to fetch data for the selected metal.", []

    # Extract selected properties
    try:
        x = [d[property1] for d in data]
        y = [d[property2] for d in data]
    except KeyError:
        return f"Invalid properties selected: {property1}, {property2}", []

    # Generate plot data
    plot_data = [{
        'x': x,
        'y': y,
        'type': 'scatter',
        'mode': 'lines+markers',
        'name': f'{property1} vs {property2}',
    }]

    result = f"Simulation results for {metal}: {property1} vs {property2}."
    return result, plot_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        result, plot_data = simulate_radiation(data['metal'], data['property1'], data['property2'])
        return jsonify({'result': result, 'plot_data': plot_data})
    except Exception as e:
        print(f"Error in simulation: {e}")
        return jsonify({'result': 'An error occurred during simulation.', 'plot_data': []})

if __name__ == '__main__':
    app.run(debug=True)