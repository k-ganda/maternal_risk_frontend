from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import pickle
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
RENDER_URL = 'https://nurture-prediction.onrender.com'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/preprocess')
def preprocess():
    return render_template('preprocess.html')

@app.route('/visualizations')
def visualizations():
    return render_template('visualizations.html')  

@app.route('/upload-data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"detail": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"detail": "No selected file"}), 400

    # Log file content type to debug
    print(f"File content type: {file.content_type}")

    # Send the file to FastAPI backend
    response = requests.post(f'{RENDER_URL}/upload-data',  files={'file': (file.filename, file.stream, file.content_type)})

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify(response.json()), response.status_code


@app.route('/retrain', methods=['GET', 'POST'])
def retrain():
    if request.method == 'POST':
        file_path = request.json.get('file_path')
        if not file_path:
            return jsonify({"detail": "File path not provided"}), 400
        
        normalized_path = os.path.normpath(file_path).replace("\\", "/")
        
        # Debug statement to verify the normalized path
        print("Payload sent to FastAPI:", {"file_path": normalized_path})
        
        
        
        # Send the file path to FastAPI backend to retrain
        try:
            response = requests.post(f'{RENDER_URL}/retrain', json={"file_path": normalized_path})
            response.raise_for_status()  # Raise an error if response is not successful
            print("Response from FastAPI:", response.json())
            
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            # Handle errors from the FastAPI backend 
            print(f"Error communicating with FastAPI: {e}")
            return jsonify({"detail": f"Error retraining model: {str(e)}"}), 500
    return render_template('retrain.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction_message = None  
    form_data = {
        "Age": "",
        "SystolicBP": "",
        "DiastolicBP": "",
        "BS": "",
        "BodyTemp": "",
        "HeartRate": "",
    }  # Initialize form_data with empty strings

    if request.method == 'POST':
        print("Form Data Received:", request.form)
        try:
            # Get the form data from the request and populate form_data
            form_data = {
                "Age": int(request.form['Age']),
                "SystolicBP": int(request.form['SystolicBP']),
                "DiastolicBP": int(request.form['DiastolicBP']),
                "BS": float(request.form['BS']),
                "BodyTemp": float(request.form['BodyTemp']),
                "HeartRate": int(request.form['HeartRate']),
            }

            # Send the data to the FastAPI endpoint for prediction
            response = requests.post(f"{RENDER_URL}/predict", json=form_data)
            response.raise_for_status()  
            result = response.json()
            prediction_message = result.get('Your Predicted Risk Level is: ', 'No result')

        except requests.exceptions.RequestException as e:
            prediction_message = f"An error occurred: {e}"

    return render_template('predict.html', prediction_message=prediction_message, form_data=form_data)


        

if __name__ == '__main__':
    app.run(debug=True)