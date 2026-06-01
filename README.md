# Plant Disease Classifier

Flask + React application for plant leaf disease prediction using a TensorFlow model.

## Prerequisites

- Python 3.11
- Node.js (LTS)

## Backend Setup

From project root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs at `http://127.0.0.1:5000`.

Health endpoint:

`http://127.0.0.1:5000/health`

## Frontend Setup

In a second terminal:

```powershell
cd frontend
npm install
npm start
```

Frontend runs at `http://localhost:3000`.

## Model Path

The backend loads the model from:

`plant-disease-detection/train_plant_disease_model.keras`
