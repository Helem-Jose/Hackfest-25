document.addEventListener("DOMContentLoaded", function () {
    let fetchButton = document.getElementById("fetchEmails");

    if (fetchButton) {
        fetchButton.addEventListener("click", () => {
            chrome.runtime.sendMessage({ action: "fetchEmails" }, response => {
                let emailsDiv = document.getElementById("emails");
                emailsDiv.innerHTML = "";

                if (response?.emails?.length > 0) {
                    response.emails.forEach(email => {
                        let emailEntry = `<div><strong>📨 ${email.subject}</strong><br>
                                          From: ${email.sender}<br>
                                          <p>${email.message.substring(0, 200)}...</p></div><hr>`;
                        emailsDiv.innerHTML += emailEntry;
                    });
                } else {
                    emailsDiv.innerHTML = "<p>No emails found.</p>";
                }
            });
        });
    } else {
        console.error("❌ Button with ID 'fetchEmails' not found!");
    }
});
