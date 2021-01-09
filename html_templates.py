def base(body):
    return f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

        <title>ITC's Heart Disease Predictor</title>
      </head>
      <body>
        <div class="container p-1">
        <main>
            <div class="row">
            <h1><img src="https://i.ibb.co/mD4jTGQ/itclogo.jpg" alt="ITC logo"> ITC's Heart Disease Predictor</h1>
            </div>
            {body}        
        </main>
        </div>
      </body>
    </html>
    """


def form_input(input_id, label, value, under=''):
    return f"""
        <div class="row mb-2 px-2">
                <label for="{input_id}" class="form-label">{label}</label>
                <input type="text" class="form-control" id="{input_id}" name="{input_id}" value="{value}" aria-describedby="{input_id}_help">
                <div id="{input_id}_help" class="form-text">{under} </div>
        </div>
    """


def form():
    return base(f"""
        <div class="px-5 mt-4">
        <form action="/predict_single">
        <div class="row">
            <div class="col">
                {form_input('age', 'Age', 70, 'in years')}
                {form_input('sex', 'Sex', 1, '1 = male; 0 = female')}
                {form_input('cp', 'Chest pain type', 4, 'Values from 1-4')}
                {form_input('trestbps', 'Resting blood pressure', 276, 'in mm Hg on admission to the hospital')}
                {form_input('chol', 'Serum Cholestoral in mg/dl', 150)}
                              
            </div>
            <div class="col">
                {form_input('fbs', 'Fasting blood sugar > 120 mg/dl', 0, '1 = yes; 0 = no')}
                {form_input('restecg', 'Resting electrocardiographic results', 0,  'Values from 0-2')}  
                {form_input('thalach', 'Maximum heart rate achieved', 112, 'bpm')}
                {form_input('exang', 'Exercise induced angina', 1, '1 = yes; 0 = no')}                
            </div>
            <div class="col">
                {form_input('oldpeak', 'Old Peak', 0.6, 'ST depression induced by exercise relative to rest')}
                {form_input('slope', 'Slope', 1, 'slope of the peak exercise ST segment')}
                {form_input('ca', 'Number of vessels colored by flourosopy', 1, 'Values from 0-3')}
                {form_input('thal', 'Thal', 1, '3 = normal; 6 = fixed defect; 7 = reversable defect')}
            </div>
        </div>
        <div class="row mt-2">
            <button type="submit" class="btn btn-success">PREDICT</button>
        </div>
        </form>
        </div>
    """)


def results(prediction):
    return base(f"""
        <h4 class="text-center mb-5">Results</h4>
        <p class="text-center">Heart Disease: {prediction}</p>
        <p class="text-center"><a class="btn btn-success mt-5" href='/'>Go back</a></p>
    """)
