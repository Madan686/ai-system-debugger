import json
import requests


OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral:latest"


def build_debug_prompt(error_text):
    """
    Builds a strict JSON prompt for the AI model.

    Why this function is required:
    We do not want one long paragraph.
    We want the model to return separated fields:
    summary, root_cause, possible_location, fix_steps, corrected_code_or_command.
    """

    prompt = f"""
You are an expert software debugging assistant.

Your task:
Analyze the given error log or stack trace and produce a clear debugging explanation.

Return ONLY valid JSON.
Do not return markdown.
Do not return explanation outside JSON.
Do not add extra keys.
Do not skip any key.

Return exactly this JSON structure:

{{
  "category": "Choose one: Dependency Error, Import Error, Database Error, Authentication Error, Runtime Error, API Error, Configuration Error, Syntax Error, Network Error, File System Error, Environment Error, Unknown Error",
  "summary": "Explain what the error means in maximum 2 short sentences.",
  "root_cause": "Explain the most likely technical cause in maximum 2 short sentences.",
  "possible_location": "Mention the most likely file, function, dependency, configuration, API, database, or runtime area where the issue exists.",
  "fix_steps": [
    "First practical debugging step",
    "Second practical debugging step",
    "Third practical debugging step"
  ],
  "corrected_code_or_command": "Return ONLY raw command or code.
Do not explain it.
Do not add sentences before or after it.
Examples:
pip install flask
python app.py
requests.post(url, json=data)"
}}

Guidelines:
- Focus mainly on debugging, not only classification.
- Category should be selected based on the primary cause.
- Keep summary short and beginner-friendly.
- Root cause must be specific, not generic.
- Fix steps must be practical and directly related to the error.
- corrected_code_or_command should contain only the command or code when useful.
- Avoid unsafe advice such as permanently disabling SSL verification.
- Return only JSON.

Small classification guide:
- Missing module during import → Import Error
- Package install/version/setup issue → Dependency Error
- SQL/MongoDB/table/query/connection issue → Database Error
- Token/API key/login/permission issue → Authentication Error
- HTTP endpoint/method/status/request issue → API Error
- Missing env/config/secret/settings issue → Configuration Error
- Invalid code syntax → Syntax Error
- Server/DNS/socket/timeout connection issue → Network Error
- Missing file/path/read/write issue → File System Error
- OS/driver/runtime/version issue → Environment Error
- Code fails during execution but does not fit above → Runtime Error

Error Log:
{error_text}
"""
    return prompt


def extract_json_from_response(ai_text):
    """
    Converts the AI response text into a Python dictionary.

    Why this function is needed:
    Sometimes AI models add extra words before or after JSON.
    This function extracts only the JSON part safely.
    """

    try:
        start_index = ai_text.find("{")
        end_index = ai_text.rfind("}") + 1

        if start_index == -1 or end_index == 0:
            raise ValueError("No JSON object found in AI response.")

        json_text = ai_text[start_index:end_index]
        return json.loads(json_text)

    except Exception:
        return {
            "category": "Unknown Error",
            "summary": "AI returned an invalid response format.",
            "root_cause": "The model did not return valid JSON.",
            "possible_location": "AI response parser",
            "fix_steps": [
                "Retry the request.",
                "Check the prompt format.",
                "Use a model that follows JSON instructions better."
            ],
            "corrected_code_or_command": "Not applicable"
        }


def analyze_with_ollama(error_text):
    """
    Sends the error text to Ollama and returns structured debugging analysis.

    Flow:
    1. Build strict JSON prompt
    2. Send prompt to Ollama API
    3. Receive model response
    4. Convert response into Python dictionary
    5. Return dictionary to Flask
    """

    prompt = build_debug_prompt(error_text)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        ai_text = result.get("response", "{}")

        return extract_json_from_response(ai_text)

    except requests.exceptions.ConnectionError:
        return {
            "category": "AI Runtime Error",
            "summary": "Ollama is not running.",
            "root_cause": "The Flask app cannot connect to the local Ollama server.",
            "possible_location": "Ollama service",
            "fix_steps": [
                "Open a new terminal.",
                "Run ollama serve.",
                "Restart the Flask server."
            ],
            "corrected_code_or_command": "ollama serve"
        }

    except requests.exceptions.Timeout:
        return {
            "category": "AI Runtime Error",
            "summary": "The AI model took too long to respond.",
            "root_cause": "The local model may be slow or overloaded.",
            "possible_location": "Ollama runtime",
            "fix_steps": [
                "Try again with a shorter error log.",
                "Close unnecessary applications.",
                "Restart Ollama and Flask."
            ],
            "corrected_code_or_command": "Not applicable"
        }

    except requests.exceptions.RequestException as error:
        return {
            "category": "API Error",
            "summary": "AI request failed.",
            "root_cause": str(error),
            "possible_location": "Ollama API request",
            "fix_steps": [
                "Check the Ollama API URL.",
                "Use http://localhost:11434/api/generate.",
                "Restart Ollama and Flask."
            ],
            "corrected_code_or_command": "OLLAMA_API_URL = \"http://localhost:11434/api/generate\""
        }