## Installation Instructions

- Open Chrome and navigate to chrome://extensions.
- Enable Developer mode (top right).
- Click Load unpacked.
- Select the folder.
- Ensure your Local Bridge Service is running on the configured port.
- Open Odoo (or any webpage for testing) and use the simulation snippet to verify connectivity.

## Integration Test Plan (Simulating Odoo)

To verify the installation without a running Odoo instance, you can open the browser console (F12) on any page (after installing the extension) and run this simulation snippet.

```javascript
// 1. Setup Listener for the response
window.addEventListener("message", (event) => {
  if (event.data.type === "POS_PAYMENT_TERMINAL_RESPONSE") {
    console.log("%c TERMINAL RESPONSE RECEIVED:", "color: green; font-weight: bold;");
    console.log(event.data.payload);
  }
});

// 2. Send a Request
console.log("Sending Payment Request...");
window.postMessage({
  type: "POS_PAYMENT_TERMINAL_REQUEST",
  payload: {
    order_id: "TEST-ORDER-001",
    amount: 42.00,
    currency: "EUR",
    is_check: false
  }
}, "*");
```
