# maternal_risk_frontend

This contains the UI for the nurture_prediction project. It is a flask based app.

## Features

1. Prediction Page: Allows users to input patient data and receive risk predictions.

2. Dashboard: Visualizations showcasing insights from the dataset.

3. Data Upload: Users can upload new data to the system for model retraining.

4. Retrain Model: A trigger to retrain the machine learning model based on new data.

5. Flood Simulation: Tests system performance under a high load of prediction requests using Locust.

6. Dockerized Deployment: App is fully containerized for ease of deployment and scaling.

# Set Up

Clone the repository:

On your terminal run

`git clone https://github.com/k-ganda/maternal_risk_frontend.git`

Start the flask app

Run: `python app.py`

Then navigate to the url provided on your browser.

## Running the docker container

In your terminal,

1. Pull the docker image, run the following command:

```
docker pull kathrineg/maternal_risk_frontend:latest
```

2. Run the image by executing the command:

```
docker run -p 5000:5000 maternal_risk_frontend:latest
```

The app will now be accessible locally by opening a browser and navigating to:

http://localhost:5000
