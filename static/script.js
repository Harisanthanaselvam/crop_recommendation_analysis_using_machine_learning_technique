document.getElementById('cropForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const data = {
        N: parseFloat(document.getElementById('nitrogen').value),
        P: parseFloat(document.getElementById('phosphorus').value),
        K: parseFloat(document.getElementById('potassium').value),
        temperature: parseFloat(document.getElementById('temperature').value),
        humidity: parseFloat(document.getElementById('humidity').value),
        ph: parseFloat(document.getElementById('ph').value),
        rainfall: parseFloat(document.getElementById('rainfall').value)
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.crop) {
            document.getElementById('result').innerText = `🌱 Recommended Crop: ${result.crop}`;
        } else {
            document.getElementById('result').innerText = `❌ Error: ${result.error || 'Unexpected error'}`;
        }
    } catch (error) {
        document.getElementById('result').innerText = '❌ Error: Network or server issue';
        console.error('Fetch Error:', error);
    }
});
