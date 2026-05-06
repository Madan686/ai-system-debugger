from flask import Flask, render_template, request, jsonify

app=Flask(__name__)

@app.route("/")
def home():
    """
    Loads the main frontend page.
    this function runs when user opens:
    http://127.0.0.1:5000
    """
    return render_template("index.html")

@app.route("/analyze", method=["POST"])
def analyze_error():
    """
    Receives error text from the frontend.
    for noe, it only returns sample response.
    Later, we will connect AI logic here.
    """

    data=request.get_json()
    
    error_text= data.get("error_text","")
    if not error_text.strip():
        return jsonify({
            "success":False,
            "message": "Error text cannot be empty."
        }), 400
    
    return jsonify({
        "success":True,
        "analysis":{
            "summary": "sample error summary",
            "root_cause": "Sample root cause",
            "fix_steps": [
                "Check the error line",
                "Verify the variable or dependency",
                "Apply the correct"
                "ed code"
            ]
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
