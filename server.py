import os
import numpy as np
import pickle
import json
from flask import Flask
from flask import request
app = Flask(__name__)

MODEL_FILENAME = 'heart_model.pkl'

with open(MODEL_FILENAME, 'rb') as file:
    CLF = pickle.load(file)


@app.route('/predict_single')
def predict_single():
    query = request.args
    sample = np.array(list(query.values())).astype(np.float)[np.newaxis, :]
    prediction = CLF.predict(sample)
    return f"Predicted value: {prediction[0]}"


@app.route("/predict_multiple", methods=["POST"])
def predict_multiple():
    body = request.get_json()
    samples = np.array([list(sample.values()) for sample in json.loads(body)])
    predictions = CLF.predict(samples)
    return json.dumps({"predictions": predictions.tolist()})


if __name__ == '__main__':
    port = os.environ.get('PORT')

    if port:
        app.run(host='0.0.0.0', port=int(port))
    else:
        app.run()
