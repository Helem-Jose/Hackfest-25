chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "fetchEmails") {
        fetch("http://127.0.0.1:5000/get_emails")
            .then(response => response.json())
            .then(data => {
                console.log("📩 Email Threads:", data);
                sendResponse({ emails: data });
            })
            .catch(error => console.error("❌ Error fetching emails:", error));
        return true;
    }
});
