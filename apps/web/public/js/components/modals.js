// Expenso Modal & Shortcut Controller Component
const Modals = (() => {
  function open(modalId) {
    const el = document.getElementById(modalId);
    if (el) {
      el.classList.add("active");
      const input = el.querySelector("input:not([type=hidden]), select");
      if (input) setTimeout(() => input.focus(), 100);
    }
  }

  function close(modalId) {
    if (modalId === "authModal" && !API.getToken()) return;
    const el = document.getElementById(modalId);
    if (el) el.classList.remove("active");
  }

  function closeAll() {
    document.querySelectorAll(".modal-overlay.active").forEach(m => {
      if (m.id === "authModal" && !API.getToken()) return;
      m.classList.remove("active");
    });
  }

  function setupShortcuts() {
    window.addEventListener("keydown", (e) => {
      const activeEl = document.activeElement;
      const isInput = activeEl && ["INPUT", "SELECT", "TEXTAREA"].includes(activeEl.tagName);

      if (e.key === "Escape") { closeAll(); return; }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault(); open("commandModal"); return;
      }
      if (isInput) return;

      if (e.key === "e" || e.key === "E") {
        e.preventDefault(); openAddTxModal("expense");
      } else if (e.key === "i" || e.key === "I") {
        e.preventDefault(); openAddTxModal("income");
      } else if (e.key === "/") {
        e.preventDefault();
        window.navigateToView("transactions");
        const s = document.getElementById("txSearchInput");
        if (s) s.focus();
      }
    });
  }

  function openAddTxModal(type = "expense") {
    const form = document.getElementById("transactionForm");
    if (form) { form.reset(); delete form.dataset.editId; }
    document.getElementById("txModalTitle").innerText = type === "expense" ? "Add Expense" : "Add Income";
    document.getElementById("txType").value = type;
    document.getElementById("txDate").value = new Date().toISOString().slice(0, 10);

    const catSelect = document.getElementById("txCategory");
    catSelect.innerHTML = '<option value="">Select Category</option>';
    State.state.categories.filter(c => c.type === type).forEach(c => {
      const opt = document.createElement("option"); opt.value = c.id; opt.innerText = c.name; catSelect.appendChild(opt);
    });

    const pmSelect = document.getElementById("txPaymentMethod");
    pmSelect.innerHTML = '<option value="">Select Payment Method</option>';
    State.state.paymentMethods.forEach(p => {
      const opt = document.createElement("option"); opt.value = p.id; opt.innerText = p.name; pmSelect.appendChild(opt);
    });
    open("transactionModal");
  }

  function openBudgetModal() {
    const catSelect = document.getElementById("budgetCategory");
    catSelect.innerHTML = '<option value="">Select Category</option>';
    State.state.categories.filter(c => c.type === "expense").forEach(c => {
      const opt = document.createElement("option"); opt.value = c.id; opt.innerText = c.name; catSelect.appendChild(opt);
    });
    open("budgetModal");
  }

  function openRecurringModal() {
    const catSelect = document.getElementById("recCategory");
    catSelect.innerHTML = '<option value="">Select Category</option>';
    State.state.categories.filter(c => c.type === "expense").forEach(c => {
      const opt = document.createElement("option"); opt.value = c.id; opt.innerText = c.name; catSelect.appendChild(opt);
    });
    document.getElementById("recStartDate").value = new Date().toISOString().slice(0, 10);
    open("recurringModal");
  }

  return { open, close, closeAll, setupShortcuts, openAddTxModal, openBudgetModal, openRecurringModal };
})();
