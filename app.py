import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
CORS(app) # Enable CORS for communication with React frontend

# --- 1. Load the Model ---
# Use the trained model placed under plant-disease-detection.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'plant-disease-detection', 'train_plant_disease_model.keras')

if not os.path.exists(MODEL_PATH):
    print(f"Error: Model file not found at {MODEL_PATH}")
    print("Please ensure 'train_plant_disease_model.keras' exists in 'plant-disease-detection'.")
    exit()

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("ML Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# --- 2. Define Disease Classes ---
# This class order must match validation_set.class_names from training/testing notebooks.
CLASS_NAMES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

# --- 3. Prediction Function ---
def preprocess_image(image_data):
    """
    Preprocesses the image for the ML model.
    Matches notebook inference: RGB image resized to 64x64 and batched.
    """
    image = image_data.convert('RGB').resize((64, 64))
    img_array = np.asarray(image, dtype=np.float32)

    # Expand dimensions to match model input shape: (batch, height, width, channels)
    img_reshape = np.expand_dims(img_array, axis=0)

    return img_reshape

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            # Read the image file
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))
            
            # Preprocess and predict
            processed_image = preprocess_image(image)
            predictions = model.predict(processed_image, verbose=0)[0]
            result_index = int(np.argmax(predictions))
            result_class = CLASS_NAMES[result_index]
            confidence = float(predictions[result_index]) * 100
            
            return jsonify({'prediction': result_class, 'confidence': f"{confidence:.2f}%"})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Plant disease detection API is running.',
        'endpoints': {
            'health': '/health',
            'predict': '/predict (POST multipart/form-data with key "file")'
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_loaded': True, 'classes': len(CLASS_NAMES)})

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Run on port 5000