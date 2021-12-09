let color = '#3c3aa7';

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({ color });
});
