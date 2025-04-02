from flask import Blueprint, request, jsonify
from app.model import generate_response, analyze_tone, summarize_email
from app.utils import prioritize_emails

bp = Blueprint("main", __name__)

@bp.route("/compose", methods=["POST"])
def compose_email():
    data = request.json
    prompt = data.get("prompt")
    user_id = data.get("user_id")
    response = generate_response(prompt, user_id)
    return jsonify({"response": response})

@bp.route("/analyze-tone", methods=["POST"])
def analyze():
    data = request.json
    email_content = data.get("content")
    tone = analyze_tone(email_content)
    return jsonify({"tone": tone})

@bp.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    email_content = data.get("content")
    summary = summarize_email(email_content)
    return jsonify({"summary": summary})

@bp.route("/prioritize", methods=["POST"])
def prioritize():
    data = request.json
    emails = data.get("emails")
    user_id = data.get("user_id")
    prioritized_emails = prioritize_emails(emails, user_id)
    return jsonify({"prioritized_emails": prioritized_emails})