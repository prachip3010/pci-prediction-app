from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import numpy as np

# Load model
with open("MMGSY_best_model.pkl", "rb") as f:
    model = pickle.load(f)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        # Extract only the 12 features your model needs (order matters!)
        features = [
            data["Part_length"],
            data["Carriageway width in m."],
            data["Year of construction /upgradation"],
            data["Study Stretch Chainage"],
            data["Avg Rain fall"],
            data["Age of Pavement during Evalution Years"],
            data["MDD"],
            data["OMC"],
            data["LL"],
            data["PL"],
            data["PI"],
            data["CBR"]
        ]
        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]
        return jsonify({"Actual_PCI": float(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# For local development only
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
