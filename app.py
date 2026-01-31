from flask import Flask, render_template, request
import pickle
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Load the model
# Ensure 'model.pkl' is in the same directory as app.py or provide a full path
try:
    model = pickle.load(open('model.pkl', 'rb'))
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: model.pkl not found. Please ensure the model file is in the correct directory.")
    exit()

# Create the 'templates' directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')
    print("Created 'templates' directory.")

# Define the content for index.html
index_html_content = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Titanic Survival Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }
        .container { background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
        h1 { text-align: center; color: #333; }
        form div { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; color: #555; }
        input[type="number"], select { width: calc(100% - 22px); padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        input[type="submit"] { width: 100%; padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        input[type="submit"]:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Predict Titanic Survival</h1>
        <form action="/predict" method="post">
            <div>
                <label for="pclass">Passenger Class (1, 2, or 3):</label>
                <input type="number" id="pclass" name="pclass" min="1" max="3" required>
            </div>
            <div>
                <label for="sex">Sex:</label>
                <select id="sex" name="sex" required>
                    <option value="0">Male</option>
                    <option value="1">Female</option>
                </select>
            </div>
            <div>
                <label for="age">Age:</label>
                <input type="number" id="age" name="age" min="0" max="100" step="any" required>
            </div>
            <div>
                <label for="fare">Fare:</label>
                <input type="number" id="fare" name="fare" min="0" step="any" required>
            </div>
            <div>
                <label for="sibsp">Number of Siblings/Spouses Aboard:</label>
                <input type="number" id="sibsp" name="sibsp" min="0" required>
            </div>
            <div>
                <label for="parch">Number of Parents/Children Aboard:</label>
                <input type="number" id="parch" name="parch" min="0" required>
            </div>
            <div>
                <input type="submit" value="Predict Survival">
            </div>
        </form>
    </div>
</body>
</html>
"""

# Write the content to index.html
with open('templates/index.html', 'w') as f:
    f.write(index_html_content)
print("Created 'templates/index.html'.")

# Define the content for result.html
result_html_content = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction Result</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f4; }
        .container { background-color: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px; margin: auto; text-align: center; }
        h1 { color: #333; }
        p { font-size: 1.2em; color: #555; }
        a { display: inline-block; margin-top: 20px; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px; }
        a:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Prediction Result</h1>
        <p>The passenger is predicted to: <strong>{{ prediction_text }}</strong></p>
        <a href="/">Make another prediction</a>
    </div>
</body>
</html>
"""

# Write the content to result.html
with open('templates/result.html', 'w') as f:
    f.write(result_html_content)
print("Created 'templates/result.html'.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        pclass = float(request.form['pclass'])
        sex = float(request.form['sex'])
        age = float(request.form['age'])
        fare = float(request.form['fare'])
        sibsp = float(request.form['sibsp'])
        parch = float(request.form['parch'])

        input_data = np.array([[pclass, sex, age, fare, sibsp, parch]])

        prediction = model.predict(input_data)
        prediction_text = "survive" if prediction[0] == 1 else "not survive"

        return render_template('result.html', prediction_text=prediction_text)
    except Exception as e:
        return render_template('result.html', prediction_text=f"Error: {e}")
