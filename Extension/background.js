// Listen for messages from the content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'openPopup') {
        // Open the extension popup programmatically
        chrome.action.openPopup();
    }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "fetchEmails") {
        fetch(`http://127.0.0.1:5000/get_thread?subject=${encodeURIComponent(message.subject)}`)
            .then(response => response.json())
            .then(data => sendResponse({ emails: data }))
            .catch(error => sendResponse({ error: error.message }));
        return true; // Keep the message channel open for async response
    }
});