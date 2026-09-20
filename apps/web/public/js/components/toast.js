// Expenso Toast Notification & Undo Service
const Toast = (() => {
  function show(message, type = "success", undoCallback = null, duration = 4000) {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast ${type}`;

    const textSpan = document.createElement("span");
    textSpan.innerText = message;
    toast.appendChild(textSpan);

    if (undoCallback) {
      const undoBtn = document.createElement("button");
      undoBtn.className = "toast-undo-btn";
      undoBtn.innerText = "Undo";
      undoBtn.onclick = () => { undoCallback(); toast.remove(); };
      toast.appendChild(undoBtn);
    }

    container.appendChild(toast);
    setTimeout(() => {
      if (toast.parentElement) {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(50px)";
        toast.style.transition = "all 0.25s ease";
        setTimeout(() => toast.remove(), 250);
      }
    }, duration);
  }

  return { show };
})();
