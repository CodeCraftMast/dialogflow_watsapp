from flask import Flask, request, jsonify
import os
import uuid
import json
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

# قراءة بيانات اعتماد Google من متغير البيئة
creds_json = os.environ.get("GOOGLE_CREDENTIALS")
if not creds_json:
    raise ValueError("GOOGLE_CREDENTIALS environment variable is missing")

creds_dict = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(creds_dict)

# إنشاء عميل Dialogflow
session_client = dialogflow.SessionsClient(credentials=credentials)
project_id = "final-leay"

app = Flask(__name__)

def detect_intent_texts(project_id, session_id, text, language_code="ar"):
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text

@app.route("/message", methods=["POST"])
def message():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    session_id = str(uuid.uuid4())
    try:
        reply_text = detect_intent_texts(project_id, session_id, user_message)
        return jsonify({"reply": reply_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render يحدد PORT تلقائيًا
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
