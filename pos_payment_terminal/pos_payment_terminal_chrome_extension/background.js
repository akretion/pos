// background.js

// Default bridge URL (can be changed in popup)
const DEFAULT_BRIDGE_URL = "http://127.0.0.1:8080/pay";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "process_payment") {

    // We must return true to indicate we will respond asynchronously
    handlePaymentRequest(request.payload, sendResponse);
    return true;
  }
});

async function handlePaymentRequest(payload, sendResponse) {
  try {
    // 1. Get Bridge URL from storage
    const config = await chrome.storage.local.get(['bridgeUrl']);
    const bridgeUrl = config.bridgeUrl || DEFAULT_BRIDGE_URL;

    // 2. Map Odoo payload to Bridge Contract
    const bridgePayload = {
      order_id: payload.order_id,
      amount: payload.amount,
      currency: payload.currency || 'EUR',
      check: payload.is_check || false
    };

    console.log("[Ext Bg] Sending to Bridge:", bridgeUrl, bridgePayload);

    // 3. Call the Local Bridge
    const response = await fetch(bridgeUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(bridgePayload)
    });

    if (!response.ok) {
      throw new Error(`Bridge Service Error: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("[Ext Bg] Received from Bridge:", data);

    // 4. Map Caisse-AP Protocol logic to Odoo Response
    // Protocol Rules:
    // AE = '10' -> Success
    // AE = '01' -> Failure (Look at AF)
    // AE = '11' -> Request Accepted (Immediate response, transaction pending)

    let status = "failure";

    if (data.ae === '10') {
      status = "success";
    } else if (data.ae === '11') {
      status = "pending"; // Handle immediate ACK logic if necessary
    } else if (data.ae === '01') {
      // Check AF code for specific mapping if needed (08=Timeout, 04=Refused)
      status = data.af === '08' ? "timeout" : "failure";
    }

    sendResponse({
      status: status,
      ae: data.ae,
      af: data.af || null,
      raw_response: data // Pass full data for debugging
    });

  } catch (error) {
    console.error("[Ext Bg] Error processing payment:", error);
    sendResponse({
      status: "failure",
      ae: "99", // Custom code for connection error
      af: "00",
      error: "Could not connect to Local Bridge Service. Ensure it is running."
    });
  }
}
