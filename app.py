from flask import Flask, request, jsonify
import dialogflow_v2 as dialogflow
import os, uuid

# ملف JSON للـ credentials ترفعيه في إعدادات Render كـ Environment Variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "final-leay-4404b490528d.json"

project_id = "final-leay"

app = Flask(__name__)

def detect_intent_texts(project_id, session_id, text, language_code="ar"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_text

@app.route("/message", methods=["POST"])
def message():
    data = request.get_json()
    user_message = data.get("message", "")
    session_id = str(uuid.uuid4())
    reply_text = detect_intent_texts(project_id, session_id, user_message)
    return jsonify({"reply": reply_text})

# Render يقرأ المتغير PORT تلقائياً
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
