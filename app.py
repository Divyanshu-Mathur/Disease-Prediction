import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify

# Load trained model and symptom list
model = joblib.load("model.pkl") 
label = joblib.load('label.pkl')
descriptions = pd.read_csv("symptom_Description.csv")
precautions = pd.read_csv("symptom_precaution.csv")
    

# Load symptom names from dataset
df=pd.read_csv('Training.csv')
df.drop(columns='Unnamed: 133',axis=1,inplace=True)
symptom_list = list(df.columns)[:-1]  # Add all 133 symptoms here

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", symptoms=symptom_list)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        selected_symptoms = data.get("symptoms", [])
        print(selected_symptoms)

        if not selected_symptoms:
            return jsonify({"error": "No symptoms selected"}), 400

        # Convert selected symptoms into input format for model
        input_features = [1 if symptom in selected_symptoms else 0 for symptom in symptom_list]
        input_array = np.array(input_features)

        # Make prediction
        prediction = model.predict([input_array])[0]
        disease = list(label.inverse_transform([prediction]))[0]
        probabilities = model.predict_proba([input_array])[0]
        predicted_index = model.classes_.tolist().index(prediction)
        confidence_score = float(probabilities[predicted_index] * 100)
        
        description = descriptions.loc[descriptions["Disease"] == disease, "Description"].values[0]
        precaution_row = precautions.loc[precautions["Disease"] == disease]
        precaution_list = precaution_row.iloc[0, 1:].dropna().tolist()

        return jsonify({
            "prediction": disease,
            "confidence": confidence_score,
            "description": description,
            "precautions": precaution_list
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
