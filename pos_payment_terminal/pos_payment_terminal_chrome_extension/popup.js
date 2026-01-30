document.addEventListener('DOMContentLoaded', () => {
  const urlInput = document.getElementById('url');
  const statusDiv = document.getElementById('status');

  // Load current setting
  chrome.storage.local.get(['bridgeUrl'], (result) => {
    urlInput.value = result.bridgeUrl || "http://127.0.0.1:8080/pay";
  });

  // Save setting
  document.getElementById('save').addEventListener('click', () => {
    const url = urlInput.value;
    chrome.storage.local.set({ bridgeUrl: url }, () => {
      statusDiv.style.display = 'block';
      setTimeout(() => { statusDiv.style.display = 'none'; }, 2000);
    });
  });
});
