from flask import Flask, render_template, request, jsonify
from ai_engine import analyze_with_ollama
from database import create_history_table, save_analysis, get_analysis_history

app=Flask(__name__)
create_history_table()

def validate_error_input(error_text):
    """
    Validates the error text submitted by the user.
    
    Rules: 
    1. Input should not be Empty.
    2. Input should be minimum of 10 characters.
    """

    if not error_text:
        return False, "Error text is required."
    
    if len(error_text.strip())< 10:
        return False, "Enter the valid error log with atleast of 10 characters."
    
    return True, "Valid Input."


@app.route("/")
def home():
    """
    Loads the main frontend page.
    this function runs when user opens:
    http://127.0.0.1:5000
    """
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_error():
    """
    Receives error text from the frontend.
    Validates it, sends it to Ollama,
    and returns AI-generated analysis.
    """

    data = request.get_json() or {}

    error_text = data.get("error_text", "")

    is_valid, message = validate_error_input(error_text)

    if not is_valid:
        return jsonify({
            "success": False,
            "message": message
        }), 400

    ai_result = analyze_with_ollama(error_text)
    save_analysis(error_text, ai_result)

    return jsonify({
        "success": True,
        "analysis": ai_result
    })


@app.route("/history", methods=["GET"])
def history():
    search_query=request.args.get("search","").strip()
    records=get_analysis_history(search_query)
    
    return jsonify({
        "success":True,
        "history":records
    })


if __name__ == "__main__":
    app.run(debug=True)
