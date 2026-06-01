import React, { useState } from 'react';
import './App.css';
import logo from './logo.svg';

const API_BASE_URL = 'http://127.0.0.1:5000';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Revoke the old object URL to avoid memory leaks
      if (previewImage) {
        URL.revokeObjectURL(previewImage);
      }
      setSelectedFile(file);
      setPreviewImage(URL.createObjectURL(file));
      setPrediction(null);
      setConfidence(null);
      setError(null);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    if (previewImage) URL.revokeObjectURL(previewImage);
    setPreviewImage(null);
    setPrediction(null);
    setConfidence(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select an image first.");
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);
    setConfidence(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        let errorData = {};
        try {
          errorData = await response.json();
        } catch (_jsonParseError) {
          // Keep a generic fallback if backend doesn't return JSON.
        }
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setPrediction(data.prediction);
      setConfidence(data.confidence);
    } catch (err) {
      setError(`Failed to get prediction: ${err.message}`);
      console.error("Prediction error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="app-header">
        <img src={logo} className="app-logo" alt="Leaf logo" />
        <h1>LeafCare - Plant Disease Detection</h1>
      </div>
      <p>Upload an image of a plant leaf to identify potential diseases.</p>
      
      <div className="upload-section">
        <input type="file" accept="image/*" onChange={handleFileChange} id="file-input" />
        <div className="button-group">
          <button onClick={handleUpload} disabled={!selectedFile || loading}>
            {loading ? 'Analyzing...' : 'Classify Image'}
          </button>
          <button onClick={handleClear} disabled={loading} style={{ marginLeft: '10px' }}>
            Clear
          </button>
        </div>
      </div>

      {error && <p className="error-text">Error: {error}</p>}

      {previewImage && (
        <div>
          <h2>Uploaded Image:</h2>
          <img src={previewImage} alt="Preview" style={{ maxWidth: '100%', maxHeight: '300px', borderRadius: '8px', marginTop: '20px' }} />
        </div>
      )}

      {prediction && (
        <div className="result-card">
          <h2 className="result-title">Prediction Result:</h2>
          <p className="result-disease">
            Disease: {prediction}
          </p>
          <p className="result-confidence">
            Confidence: {confidence}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;