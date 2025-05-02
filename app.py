import pickle
from flask import Flask, render_template, request, jsonify

# Load model
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Manual label-to-crop-name mapping (example, adjust as per your data)
label_to_crop = {
    0: 'apple', 1: 'banana', 2: 'blackgram', 3: 'chickpea',
    4: 'coconut', 5: 'coffee', 6: 'cotton', 7: 'grapes',
    8: 'jute', 9: 'kidneybeans', 10: 'lentil', 11: 'maize',
    12: 'mango', 13: 'mothbeans', 14: 'mungbean', 15: 'muskmelon',
    16: 'orange', 17: 'papaya', 18: 'pigeonpeas', 19: 'pomegranate',
    20: 'rice', 21: 'watermelon'
}

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Extract and convert input values
        N = float(data['N'])
        P = float(data['P'])
        K = float(data['K'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])

        # Prepare input
        input_features = [[N, P, K, temperature, humidity, ph, rainfall]]
        prediction = model.predict(input_features)[0]

        # Map prediction to crop name
        crop_name = label_to_crop.get(int(prediction), "Unknown Crop")

        return jsonify({'crop': crop_name})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
