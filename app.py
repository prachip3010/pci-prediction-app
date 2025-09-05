import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the trained model
with open("MMGSY_best_model.pkl", "rb") as f:
    model = pickle.load(f)

# Feature order expected by the model
features = [
    "Unnamed: 0",
    "Carriageway width in m.",
    "Year of construction /upgradation",
    "Study Stretch Chainage",
    "Avg Rain fall",
    "Age of Pavement during Evalution Years ",
    "MDD",
    "PI",
    "SCI",
    "MSN",
    "CVPD",
    "evalution_quarter"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Build input vector (add dummy 0 for "Unnamed: 0")
        input_data = [0]  # dummy index
        for feature in features[1:]:  # skip Unnamed: 0, already added
            if feature not in data:
                return jsonify({"error": f"Missing feature: {feature}"}), 400
            input_data.append(float(data[feature]))

        # Reshape for model
        input_array = np.array(input_data).reshape(1, -1)

        # Prediction
        prediction = model.predict(input_array)
        predicted_value = float(prediction[0])

        return jsonify({"prediction": predicted_value})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
