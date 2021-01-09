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


def html_base(body):
    return f"""
    <head>
        <title>ITC's Heart Disease Predictor</title>
    </head>
    <body>  
        <h1><img src="https://i.ibb.co/mD4jTGQ/itclogo.jpg" alt="ITC logo">ITC's Heart Disease Predictor</h1>
        {body}
    </body>        
    """


@app.route('/')
def home():
    html_body = f"""     
    <form action="/predict_single">
        <label for="age">Age: </label><input type="text" id="age" name="age" value=70><br><br>
        <label for="sex">Sex (1 = male; 0 = female): </label><input type="text" id="sex" name="sex" value=1><br><br>
        <label for="cp">Chest pain type (4 values): </label><input type="text" id="cp" name="cp" value=4><br><br>
        <label for="trestbps">Resting blood pressure (in mm Hg on admission to the hospital): </label><input type="text" id="trestbps" name="trestbps" value="150"><br><br>
        <label for="chol">Serum Cholestoral in mg/dl: </label><input type="text" id="chol" name="chol" value=276><br><br>
        <label for="fbs">Fasting blood sugar > 120 mg/dl (1 = yes; 0 = no): </label><input type="text" id="fbs" name="fbs" value=0><br><br>
        <label for="restecg">Resting electrocardiographic results (values 0,1,2): </label><input type="text" id="restecg" name="restecg" value=0><br><br>
        <label for="thalach">Maximum heart rate achieved: </label><input type="text" id="thalach" name="thalach" value=112><br><br>
        <label for="exang">Exercise induced angina (1 = yes; 0 = no): </label><input type="text" id="exang" name="exang" value=1><br><br>
        <label for="oldpeak">Old Peak (ST depression induced by exercise relative to rest): </label><input type="text" id="oldpeak" name="oldpeak" value=0.6><br><br>
        <label for="slope">Slope (of the peak exercise ST segment): </label><input type="text" id="slope" name="slope" value=1><br><br>
        <label for="ca">Number of major vessels (0-3) colored by flourosopy: </label><input type="text" id="ca" name="ca" value=1><br><br>
        <label for="thal">Thal (3 = normal; 6 = fixed defect; 7 = reversable defect): </label><input type="text" id="thal" name="thal" value=1><br><br>
        <input type="submit" value="Predict">
    </form> 
    """
    return html_base(html_body)


@app.route('/predict_single')
def predict_single():
    query = request.args
    ordered_params = ['trestbps', 'slope', 'chol', 'exang', 'thal', 'age', 'fbs', 'restecg', 'oldpeak', 'sex', 'thalach', 'ca', 'cp']
    ordered_query = np.array([query[key] for key in ordered_params])
    sample = ordered_query.astype(np.float)[np.newaxis, :]
    prediction = CLF.predict(sample)

    prediction_string = "Yes" if prediction[0] else "No"
    html_body = f"<p>Heart Disease: {prediction_string}</p><a href='/'>Go back</a>"
    return html_base(html_body)


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
