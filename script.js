document.getElementById('simulation-form').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const formData = {
      metal: document.getElementById('metal').value,
      property1: document.getElementById('property1').value,
      property2: document.getElementById('property2').value,
    };
  
    fetch('/simulate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })
      .then(response => response.json())
      .then(data => {
        document.getElementById('result-text').innerText = data.result;
        Plotly.newPlot('visualization', data.plot_data);
      })
      .catch(error => console.error('Error:', error));
  });