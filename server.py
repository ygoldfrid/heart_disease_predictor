import os
import numpy as np
import pickle
import json
import html_templates
from flask import Flask
from flask import request
app = Flask(__name__)

MODEL_FILENAME = 'heart_model.pkl'

with open(MODEL_FILENAME, 'rb') as file:
    CLF = pickle.load(file)


@app.route('/')
def home():
    return html_templates.form()


@app.route('/predict_single')
def predict_single():
    query = request.args
    ordered_params = ['trestbps', 'slope', 'chol', 'exang', 'thal', 'age', 'fbs', 'restecg', 'oldpeak', 'sex', 'thalach', 'ca', 'cp']
    ordered_query = np.array([query[key] for key in ordered_params])
    sample = ordered_query.astype(np.float)[np.newaxis, :]
    prediction = CLF.predict(sample)

    prediction_string = "Yes" if prediction[0] else "No"
    return html_templates.results(prediction_string)


@app.route("/predict_multiple", methods=["POST"])
def predict_multiple():
    body = request.get_json()
    if type(body) == str:
        body = json.loads(body)
    samples = np.array([list(sample.values()) for sample in body])
    predictions = CLF.predict(samples)
    return json.dumps({"predictions": predictions.tolist()})


if __name__ == '__main__':
    port = os.environ.get('PORT')

    if port:
        app.run(host='0.0.0.0', port=int(port))
    else:
        app.run()
