// Get the focused textbox value (textarea/input/contenteditable)
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "getTextboxValue") {
      const activeElement = document.activeElement;
  
      if (
        activeElement.tagName === "TEXTAREA" ||
        (activeElement.tagName === "INPUT" && activeElement.type === "text")
      ) {
        sendResponse({ text: activeElement.value });
      } else if (
        activeElement.tagName === "DIV" &&
        activeElement.isContentEditable
      ) {
        sendResponse({ text: activeElement.innerText });
      } else {
        sendResponse({ text: "" });
      }
    }
  
    if (msg.action === "sendToChatGPT") {
      const editable = document.querySelector('div[contenteditable="true"]');
  
      if (editable) {
        // Clear existing content first
        editable.innerText = "";
        editable.dispatchEvent(new InputEvent('input', { bubbles: true }));
  
        // Paste masked content after slight delay
        setTimeout(() => {
          editable.innerText = msg.text;
          editable.dispatchEvent(new InputEvent('input', { bubbles: true }));
          console.log("✅ Masked prompt inserted — waiting for manual send.");
        }, 200);
      } else {
        console.warn("⚠️ ChatGPT input box not found.");
      }
    }
  });
  