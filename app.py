from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import os  # Sabse upar standard tareeke se import kiya

app = Flask(__name__)

# 1. Hamare trained Random Forest model ko load kar rahe hain
with open('rf_house_model.pkl', 'rb') as file:
    model = pickle.load(file)

# 2. Home Page Route
@app.route('/')
def home():
    return render_template('index.html')

# 3. Predict Form Rendering Route
@app.route('/predict_form')
def predict_form():
    return render_template('predict.html')

# 4. Route to render the analytics launch panel template (Duplicate Hataya)
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

# 5. Advanced Route to trigger local Power BI Application launch offline
@app.route('/launch_powerbi')
def launch_powerbi():
    # Automatically finds the path of dashboard.pbix inside your project folder
    pbix_path = os.path.abspath("dashboard.pbix")
    
    try:
        if os.path.exists(pbix_path):
            os.startfile(pbix_path) # Python native trigger to open local file with Power BI Desktop
            return render_template('analytics.html')
        else:
            return "Error: File 'dashboard.pbix' not found in project directory. Please add it."
    except Exception as e:
        return f"An error occurred while launching Power BI: {str(e)}"

# 6. Predict Route - Jahan form ka data aayega aur prediction hogi
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Form se saare inputs le rahe hain
            bedrooms = int(request.form['bedrooms'])
            bathrooms = float(request.form['bathrooms'])
            sqft_living = int(request.form['sqft_living'])
            sqft_lot = int(request.form['sqft_lot'])
            floors = float(request.form['floors'])
            waterfront = int(request.form['waterfront'])
            view = int(request.form['view'])
            condition = int(request.form['condition'])
            grade = int(request.form['grade'])
            sqft_above = int(request.form['sqft_above'])
            sqft_basement = int(request.form['sqft_basement'])
            yr_built = int(request.form['yr_built'])
            yr_renovated = int(request.form['yr_renovated'])
            zipcode = int(request.form['zipcode'])
            lat = float(request.form['lat'])
            long = float(request.form['long'])
            sqft_living15 = int(request.form['sqft_living15'])
            sqft_lot15 = int(request.form['sqft_lot15'])

            # Saare features ko ek array me arrange kar rahe hain
            features = [
                bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, 
                view, condition, grade, sqft_above, sqft_basement, yr_built, 
                yr_renovated, zipcode, lat, long, sqft_living15, sqft_lot15
            ]
            
            final_features = [np.array(features)]
            
            # Model se price predict karwaya
            prediction = model.predict(final_features)
            output = round(prediction[0], 2)

            # Result ko wapas predict.html page par bhej rahe hain
            return render_template('predict.html', prediction_text=f'Estimated House Price: ₹{output:,}')
        
        except Exception as e:
            return render_template('predict.html', prediction_text=f'Error in prediction: {str(e)}')

if __name__ == "__main__":
    app.run(debug=True)