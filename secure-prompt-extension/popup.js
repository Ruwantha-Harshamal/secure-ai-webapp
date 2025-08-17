document.addEventListener("DOMContentLoaded", () => {
    // Autofill with focused textbox content
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, { action: "getTextboxValue" }, (response) => {
        if (response && response.text) {
          document.getElementById("prompt").value = response.text;
        }
      });
    });
  
    // Detect & Mask
    document.getElementById("filterBtn").addEventListener("click", async () => {
      const prompt = document.getElementById("prompt").value;
  
      try {
        const response = await fetch("http://localhost:8000/api/filter", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt })
        });
  
        const data = await response.json();
        document.getElementById("output").textContent = data.masked_prompt || "No mask applied.";
      } catch (error) {
        console.error("❌ Error:", error);
        document.getElementById("output").textContent = "Error occurred.";
      }
    });
  
    // Send to ChatGPT (without auto-send)
    document.getElementById("sendBtn").addEventListener("click", () => {
      const masked = document.getElementById("output").textContent;
  
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, {
          action: "sendToChatGPT",
          text: masked
        });
      });
    });
  });
  