# from flask import Flask, render_template, request, redirect, url_for
# import requests

# app = Flask(__name__)
# app.config.update(EXPLAIN_TEMPLATE_LOADING = True)
# BACKEND_URL = "http://localhost:8000"  # FastAPI endpoint

# @app.route("/", methods=["GET", "POST"])
# def signup():
#     if request.method == "POST":
#         email = request.form["email"]
#         topics = request.form.getlist("topics")
        
#         # Send data to FastAPI backend
#         response = requests.post(
#             f"{BACKEND_URL}/api/users",
#             json={
#                 "email": email,
#                 "preferences": {"topics": topics}
#             }
#         )
        
#         if response.status_code == 200:
#             return redirect(url_for("success"))
#         else:
#             error = response.json().get("detail", "Signup failed")
#             return render_template("signup.html", error=error)
    
#     return render_template("signup.html")

# @app.route("/success")
# def success():
#     return "Thank you! You'll receive your first newsletter soon."

# if __name__ == "__main__":
#     app.run(port=5000, debug=True)

from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Backend API URL
BACKEND_URL = "http://localhost:8000/api/users"

@app.route("/", methods=["GET"])
def index():
    return render_template("signup.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    try:
        data = request.get_json()
        # Get data from frontend
        email = data.get("email")
        topics = data.get("topics")  # Collect selected topics as a list

        # Construct the JSON payload in the required format
        payload = {
            "email": email,
            "topics": topics
        }
        print(payload)

        # Send data to backend
        response = requests.post(
            BACKEND_URL,
            json={
                "email": email,
                "preferences": {"topics": topics}
            }
        )

        # Return backend response to frontend
        return jsonify(response.json())
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)