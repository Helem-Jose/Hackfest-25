from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import imaplib
import email
from email.header import decode_header

# Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Gmail IMAP Credentials
IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "24je0116@iitism.ac.in"
EMAIL_PASSWORD = "ylnm ydto pvts fcws"

def fetch_threads():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()

    email_threads = []

    for email_id in email_ids[-5:]:  # Fetch last 5 emails
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                sender, encoding = decode_header(msg.get("From"))[0]
                if isinstance(sender, bytes):
                    sender = sender.decode(encoding or "utf-8")

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                email_threads.append({"sender": sender, "subject": subject, "message": body.strip()})

    mail.logout()
    return email_threads

@app.route('/get_emails', methods=['GET'])
def get_emails():
    emails = fetch_threads()
    return jsonify(emails)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
