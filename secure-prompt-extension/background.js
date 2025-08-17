chrome.runtime.onMessage.addListener((msg, sender) => {
    console.log("📬 Received message in background:", msg); // <-- Add this for visibility
  
    if (msg.action === "filterText") {
      fetch("http://localhost:8000/api/filter", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt: msg.text })
      })
        .then(res => res.json())
        .then(data => {
          chrome.tabs.sendMessage(sender.tab.id, {
            action: "showMasked",
            masked: data.masked_prompt
          });
        })
        .catch(err => {
          console.error("Error fetching filtered text:", err);
        });
    }
  });
  