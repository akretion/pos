// content_script.js

const INPUT_TYPE = "POS_PAYMENT_TERMINAL_REQUEST";
const OUTPUT_TYPE = "POS_PAYMENT_TERMINAL_RESPONSE";

// Listen for messages from Odoo POS (Web Page)
window.addEventListener("message", (event) => {
  // Security check: ensure message is from the same window
  if (event.source !== window) return;

  if (event.data && event.data.type === INPUT_TYPE) {
    console.log("[Ext Content] Received request from POS:", event.data.payload);

    // Forward to Background Script
    chrome.runtime.sendMessage(
      { action: "process_payment", payload: event.data.payload },
      (response) => {
        // Handle response from Background Script (Bridge result)
        if (chrome.runtime.lastError) {
          console.error("[Ext Content] Runtime Error:", chrome.runtime.lastError);
          sendResponseToPOS({
            status: "failure",
            ae: "99", // Internal Error
            af: "00",
            error: chrome.runtime.lastError.message
          });
        } else {
          sendResponseToPOS(response);
        }
      }
    );
  }
});

function sendResponseToPOS(payload) {
  // Send the result back to Odoo POS window
  window.postMessage({
    type: OUTPUT_TYPE,
    payload: payload
  }, "*");
}
