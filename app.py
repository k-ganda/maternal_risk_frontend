from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
FASTAPI_URL = 'http://127.0.0.1:8000'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/preprocess')
def preprocess():
    return render_template('preprocess.html')

@app.route('/visualizations')
def visualizations():
    return render_template('visualizations.html')  

@app.route('/retrain')
def retrain():
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
            response = requests.post(f"{FASTAPI_URL}/predict", json=form_data)
            response.raise_for_status()  
            result = response.json()
            prediction_message = result.get('Your Predicted Risk Level is: ', 'No result')

        except requests.exceptions.RequestException as e:
            prediction_message = f"An error occurred: {e}"

    return render_template('predict.html', prediction_message=prediction_message, form_data=form_data)


        

if __name__ == '__main__':
    app.run(debug=True)