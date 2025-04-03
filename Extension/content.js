// Function to handle button clicks
function handleButtonClick(event) {
    console.log('Button clicked!');
    console.log('Button text:', event.target.textContent);
    console.log('Button ID:', event.target.id);
    console.log('Timestamp:', new Date().toISOString());
    
    // Check if the button text is "Compose"
    if (event.target.textContent === "Compose" || event.target.textContent === "Reply") {
        // Send a message to the background script to open the popup
        chrome.runtime.sendMessage({ type: 'openPopup' });
    }

    // Optional: Send additional information to the background script
    chrome.runtime.sendMessage({
        type: 'buttonClicked',
        buttonText: event.target.textContent,
        buttonId: event.target.id,
        url: window.location.href,
        timestamp: new Date().toISOString()
    });
}

// Add click event listener to the document
document.addEventListener('click', handleButtonClick);

// Optional: Log when the content script is loaded
console.log('AI Email Reply loaded on:', window.location.href);

console.log("📌 Gmail IMAP Extractor Content Script Loaded!");

document.addEventListener("click", event => {
    if (window !== window.top) return;
    let emailThread = event.target.closest("tr.zA");
    if (emailThread) {
        console.log("📩 Email Thread Clicked!");
        let subjectElement = emailThread.querySelector(".y6 span");
        let subject = subjectElement ? subjectElement.textContent.trim() : "Unknown Subject";
        console.log("Subject:", subject);

        // Step 1: Fetch the thread ID for the clicked email (using subject as a fallback)
        fetch(`http://127.0.0.1:5000/get_thread_id?subject=${encodeURIComponent(subject)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error || !data.thread_id) {
                    throw new Error(data.error || "No thread ID found");
                }
                const threadId = data.thread_id;
                console.log("Thread ID:", threadId);

                // Step 2: Fetch the full thread using the thread ID
                return fetch(`http://127.0.0.1:5000/get_thread?thread_id=${threadId}`);
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("📩 Email Thread Data:", data);

                let emailBody = document.querySelector(".ii.gt");
                if (emailBody) {
                    emailBody.innerHTML = "<h3>Email Thread:</h3>";
                    if (data.error) {
                        emailBody.innerHTML += `<p>Error: ${data.error}</p>`;
                    } else if (data.length === 0) {
                        emailBody.innerHTML += "<p>No emails found in this thread.</p>";
                    } else {
                        data.forEach(email => {
                            emailBody.innerHTML += `
                                <p>
                                    <strong>${email.sender}</strong> (${email.date}): 
                                    ${email.message.substring(0, 100)}...
                                    (Thread ID: ${email.thread_id})
                                </p><hr>`;
                        });
                    }
                }
            })
            .catch(error => {
                console.error("❌ Error fetching thread:", error);
                let emailBody = document.querySelector(".ii.gt");
                if (emailBody) {
                    emailBody.innerHTML = `<h3>Error:</h3><p>${error.message}</p>`;
                }
            });
    }
});