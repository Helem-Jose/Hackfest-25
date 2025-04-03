from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
import imaplib
import email
from email.header import decode_header
import logging
import re
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
CORS(app)

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "adityamathur2958@gmail.com"
EMAIL_PASSWORD = "ycps tmns jngb iiox"  # Use an App Password if 2FA is enabled

@app.route('/signin.html')
def serve_signin():
    return render_template('signin.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('.', filename)

def fetch_thread_by_thrid(thread_id):
    try:
        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        # Can change to "[Gmail]/All Mail" for broader scope

        # Enable Gmail extensions
        mail.select('"[Gmail]/All Mail"')

        # Search for emails with the specific X-GM-THRID
        result, data = mail.search(None, f'X-GM-THRID {thread_id}')
        if result != "OK":
            mail.logout()
            return {"error": "Failed to search emails by thread ID"}

        email_ids = data[0].split()
        if not email_ids:
            mail.logout()
            return {"error": "No emails found for this thread ID"}

        email_threads = []
        for email_id in email_ids:
            # Fetch email data including headers and body
            result, msg_data = mail.fetch(email_id, "(RFC822 X-GM-THRID)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Decode subject
                    subj, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subj, bytes):
                        subj = subj.decode(encoding or "utf-8")

                    # Decode sender
                    sender, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding or "utf-8")

                    # Get date
                    date = msg.get("Date", "Unknown Date")

                    # Get thread ID (for verification)
                    thrid = msg.get("X-GM-THRID", "Unknown")

                    # Extract body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    email_threads.append({
                        "sender": sender,
                        "subject": subj,
                        "message": body.strip(),
                        "date": date,
                        "thread_id": thrid
                    })

            


        mail.logout()
        return email_threads
    except Exception as e:
        return {"error": str(e)}


def fetch_thread_id_by_subject(subject):
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")
        search_query = subject.replace('"', '')
        
        result, data = mail.search(None, f'(SUBJECT "{search_query}")')
        

        if result != "OK" or not data[0]:
            mail.logout()
            return {"error": "No emails found for this subject"}
        if result != "OK" or not data[0]:
            mail.logout()
            return {"error": "No emails found for this subject"}

        email_ids = data[0].split()
        latest_email_id = email_ids[-1]  # Most recent email

        result, msg_data = mail.fetch(latest_email_id, "(X-GM-THRID)")
        
        for response_part in msg_data:
                 # Check if response_part is a tuple
                decoded_response = str(response_part)  # Decode the IMAP response
                

                 # Extract X-GM-THRID using regex
                match = re.search(r'X-GM-THRID (\d+)', decoded_response)
                if match:
                    thread_id = match.group(1)
                    mail.logout()
                    return {"thread_id": thread_id}

        
        mail.logout()
        return {"error": "Thread ID not found"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/get_thread_id', methods=['GET'])
def get_thread_id():
    subject = request.args.get('subject', '')
    if not subject:
        return jsonify({"error": "Subject parameter is required"}), 400
    
    result = fetch_thread_id_by_subject(subject)
    
    if "error" in result:
        return jsonify({"error": result["error"]}), 500
    
    return jsonify(result)




@app.route('/get_thread', methods=['GET'])
def get_thread():
    thread_id = request.args.get('thread_id', '')
    if not thread_id:
        return jsonify({"error": "Thread ID parameter is required"}), 400
    result = fetch_thread_by_thrid(thread_id)
    
    if isinstance(result, dict) and "error" in result:
        return jsonify({"error": result["error"]}), 500
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)