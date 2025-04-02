console.log("📌 Gmail IMAP Extractor Content Script Loaded!");

document.addEventListener("click", event => {
    let emailThread = event.target.closest("tr.zA"); // Gmail email row

    if (emailThread) {
        console.log("📩 Email Thread Clicked!");

        // Request emails from backend
        fetch("http://127.0.0.1:5000/get_emails")
            .then(response => response.json())
            .then(data => {
                console.log("📩 Email Thread Data:", data);
                
                // Display data inside Gmail (optional)
                let emailBody = document.querySelector(".ii.gt");
                if (emailBody) {
                    emailBody.innerHTML = "<h3>Extracted Email Thread:</h3>";
                    data.forEach(email => {
                        emailBody.innerHTML += `<p><strong>${email.sender}</strong>: ${email.message.substring(0, 100)}...</p><hr>`;
                    });
                }
            })
            .catch(error => console.error("❌ Error fetching emails:", error));
    }
});
