import pickle
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId


with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


label_to_crop = {
    0: 'apple', 1: 'banana', 2: 'blackgram', 3: 'chickpea',
    4: 'coconut', 5: 'coffee', 6: 'cotton', 7: 'grapes',
    8: 'jute', 9: 'kidneybeans', 10: 'lentil', 11: 'maize',
    12: 'mango', 13: 'mothbeans', 14: 'mungbean', 15: 'muskmelon',
    16: 'orange', 17: 'papaya', 18: 'pigeonpeas', 19: 'pomegranate',
    20: 'rice', 21: 'watermelon'
}


app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/')  
db = client['crop_Recommendation_analysis'] 
collection = db['crop_predictions']  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        N = float(data['N'])
        P = float(data['P'])
        K = float(data['K'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])

        input_features = [[N, P, K, temperature, humidity, ph, rainfall]]
        prediction = model.predict(input_features)[0]

        crop_name = label_to_crop.get(int(prediction), "Unknown Crop")

        
        data_to_store = {
            'N': N,
            'P': P,
            'K': K,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall,
            'recommended_crop': crop_name
        }

    
        collection.insert_one(data_to_store)

     
        return jsonify({'crop': crop_name})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
