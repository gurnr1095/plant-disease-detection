# Plant Disease Classifier

A full-stack Flask + React web application that uses a deep learning Convolutional Neural Network (CNN) to detect and classify 38 different types of plant leaf diseases across 14 crop types (such as Apple, Corn, Grape, Potato, Tomato, etc.).

## About this Project

This project aims to assist farmers and agricultural researchers in identifying crop diseases early by analyzing plant leaf images. 
- **Deep Learning Model**: A TensorFlow/Keras Convolutional Neural Network (CNN) trained on the **New Plant Diseases Dataset**.
- **Backend API**: Built with Flask, it exposes prediction and health endpoints and performs image preprocessing (converting to RGB and resizing to 64x64).
- **Frontend UI**: Built with React, providing a user-friendly drag-and-drop interface for uploading leaf photos and instantly displaying predictions with confidence percentages.

---

## Prerequisites

- Python 3.11
- Node.js (LTS)

---

## Backend Setup

From the project root directory:

```powershell
# Create and activate virtual environment
py -3.11 -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
```

* The backend runs at `http://127.0.0.1:5000`.
* Check API status at: `http://127.0.0.1:5000/health`.

---

## Frontend Setup

In a second terminal window:

```powershell
cd frontend
npm install
npm start
```

* The frontend application runs at `http://localhost:3000`.

---

## Model Path & Training

The backend expects the trained TensorFlow model to be located at:
`plant-disease-detection/train_plant_disease_model.keras`

> [!IMPORTANT]
> Since the `.keras` model file is excluded from the Git repository due to its large size (33MB), you must do one of the following before running the backend:
> 1. Run the training notebook [Train_plant_disease.ipynb](file:///c:/Users/Gurnoor%20Kaur/Desktop/sem4proj/plant-disease-detection/Train_plant_disease.ipynb) to train the CNN model and output the file locally.
> 2. Manually copy your pre-trained `train_plant_disease_model.keras` model file into the `plant-disease-detection/` folder.
