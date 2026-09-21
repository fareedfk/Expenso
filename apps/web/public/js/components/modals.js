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

    document.getElementById("txDescription")?.addEventListener("input", (e) => {
      handleDescriptionInput(e.target.value);
    });
  }

  const EXPENSE_QUICK_TAGS = ["Lunch", "Dinner", "Groceries", "Uber / Cab", "Coffee / Tea", "Electricity Bill", "Medicine"];
  const INCOME_QUICK_TAGS = ["Salary", "Freelance Project", "Bonus", "Stock Dividend", "Refund", "Cash Gift"];

  function esc(s) {
    return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  const CATEGORY_KEYWORDS = {
    "food": ["food", "dinner", "lunch", "breakfast", "burger", "pizza", "coffee", "tea", "chai", "snack", "zomato", "swiggy", "restaurant", "cafe", "mcdonalds", "kfc", "dominos", "biryani", "roti", "samosa", "paneer", "meal", "dosa", "idli", "drink", "biscuit", "choc", "sweets", "cake", "icecream"],
    "transport": ["transport", "uber", "ola", "auto", "metro", "bus", "fuel", "petrol", "diesel", "cab", "train", "flight", "rapido", "parking", "toll", "ticket", "cng", "fare"],
    "shopping": ["shopping", "amazon", "flipkart", "clothes", "shoes", "grocery", "groceries", "mart", "myntra", "zara", "blinkit", "zepto", "instamart", "vegetables", "fruits", "dress", "shirt", "pant", "jeans", "tshirt"],
    "bills": ["bill", "electricity", "water", "wifi", "internet", "recharge", "phone", "mobile", "gas", "broadband", "jio", "airtel", "dth", "subscription", "power"],
    "rent": ["rent", "flat", "pg", "room", "maintenance", "landlord", "hostel", "apartment"],
    "entertainment": ["movie", "cinema", "game", "netflix", "party", "prime", "hotstar", "spotify", "theatre", "show", "concert", "outing", "club", "gaming"],
    "health": ["health", "medicine", "doctor", "pharmacy", "clinic", "hospital", "gym", "dentist", "tablet", "apollo", "test", "checkup", "vitamins", "pharma"],
    "education": ["education", "books", "course", "college", "school", "tuition", "exam", "fees", "stationery", "udemy", "coursera"],
    "travel": ["travel", "hotel", "resort", "trip", "holiday", "tour", "vacation", "airbnb", "stay"],
    "work": ["work", "office", "hardware", "software", "domain", "hosting", "laptop", "mouse"],
    "salary": ["salary", "stipend", "paycheck", "wages"],
    "freelancing": ["freelance", "client", "upwork", "fiverr", "gig"]
  };

  function detectCategoryFromText(text, type = "expense") {
    if (!text) return null;
    const lower = text.toLowerCase().trim();
    for (const [catKeyword, words] of Object.entries(CATEGORY_KEYWORDS)) {
      if (words.some(w => lower.includes(w))) {
        const match = State.state.categories.find(c => 
          c.type === type && c.name.toLowerCase().includes(catKeyword)
        );
        if (match) return match;
      }
    }
    return null;
  }

  function handleDescriptionInput(text) {
    const currentType = document.getElementById("txType")?.value || "expense";
    if (currentType !== "expense") return;
    const detected = detectCategoryFromText(text, currentType);
    if (detected) {
      const catSelect = document.getElementById("txCategory");
      if (catSelect) catSelect.value = detected.id;
      document.querySelectorAll(".tx-quick-chip").forEach(ch => {
        ch.classList.toggle("active", ch.dataset.catId == detected.id);
      });
    }
  }

  function switchTxType(type) {
    const isExpense = type === "expense";
    const typeInput = document.getElementById("txType");
    if (typeInput) typeInput.value = type;

    const form = document.getElementById("transactionForm");
    const editId = form?.dataset?.editId;
    const modalTitle = document.getElementById("txModalTitle");
    if (modalTitle) {
      modalTitle.innerText = editId
        ? `Edit ${isExpense ? "Expense" : "Income"}`
        : (isExpense ? "Add Expense" : "Add Income");
    }

    const submitBtn = document.getElementById("txSubmitBtn");
    if (submitBtn) {
      submitBtn.innerText = editId ? "Update Transaction" : (isExpense ? "Save Expense" : "Save Income");
    }

    const expBtn = document.getElementById("txTypeExpenseBtn");
    const incBtn = document.getElementById("txTypeIncomeBtn");
    if (expBtn) expBtn.classList.toggle("active", isExpense);
    if (incBtn) incBtn.classList.toggle("active", !isExpense);

    // Hide description group for Income, show for Expense
    const descGroup = document.getElementById("txDescriptionGroup");
    const descInput = document.getElementById("txDescription");
    if (descGroup) {
      descGroup.style.display = isExpense ? "block" : "none";
    }
    // Strict isolation: if income, completely wipe description input
    if (!isExpense && descInput) {
      descInput.value = "";
    }

    // Reset category selection on type switch so expense category never carries over into income
    const catSelect = document.getElementById("txCategory");
    if (catSelect && !editId) catSelect.value = "";
    document.querySelectorAll(".tx-quick-chip").forEach(ch => ch.classList.remove("active"));

    populateTxCategories(type);
    renderQuickDescriptions(type);
  }

  function populateTxCategories(type, selectedId = null) {
    const catSelect = document.getElementById("txCategory");
    if (!catSelect) return;
    catSelect.innerHTML = '<option value="">Select Category</option>';

    const filtered = State.state.categories.filter(c => c.type === type);
    filtered.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.id;
      const icon = State.getCategoryIcon(c.name);
      opt.innerText = `${icon}  ${c.name}`;
      if (selectedId && c.id == selectedId) opt.selected = true;
      catSelect.appendChild(opt);
    });

    const chipsRow = document.getElementById("txQuickCatChips");
    if (chipsRow) {
      chipsRow.innerHTML = filtered.slice(0, 8).map(c => {
        const icon = State.getCategoryIcon(c.name);
        const isActive = (selectedId && c.id == selectedId) || (catSelect.value == c.id);
        return `
          <button type="button" class="tx-quick-chip ${isActive ? 'active' : ''}" data-cat-id="${c.id}" onclick="Modals.selectCategoryChip(${c.id}, '${esc(c.name)}')">
            <span>${icon}</span>
            <span>${esc(c.name)}</span>
          </button>
        `;
      }).join("");
    }

    catSelect.onchange = () => {
      const val = catSelect.value;
      document.querySelectorAll(".tx-quick-chip").forEach(ch => {
        ch.classList.toggle("active", ch.dataset.catId === val);
      });
    };
  }

  function selectCategoryChip(catId, catName) {
    const catSelect = document.getElementById("txCategory");
    if (catSelect) {
      catSelect.value = catId;
    }
    document.querySelectorAll(".tx-quick-chip").forEach(ch => {
      ch.classList.toggle("active", ch.dataset.catId == catId);
    });
    const currentType = document.getElementById("txType")?.value || "expense";
    if (currentType === "expense") {
      const descInput = document.getElementById("txDescription");
      if (descInput && !descInput.value.trim()) {
        descInput.value = catName;
      }
    }
  }

  function renderQuickDescriptions(type) {
    const container = document.getElementById("txQuickDescChips");
    if (!container) return;
    const tags = type === "expense" ? EXPENSE_QUICK_TAGS : INCOME_QUICK_TAGS;
    container.innerHTML = tags.map(t => `
      <button type="button" class="quick-desc-chip" onclick="Modals.fillDescription('${t}')">+ ${t}</button>
    `).join("");
  }

  function fillDescription(text) {
    const descInput = document.getElementById("txDescription");
    if (descInput) {
      descInput.value = text;
      descInput.focus();
      handleDescriptionInput(text);
    }
  }

  function populateTxPaymentMethods(selectedId = null) {
    const pmSelect = document.getElementById("txPaymentMethod");
    if (!pmSelect) return;
    pmSelect.innerHTML = '<option value="">Select Payment Method</option>';
    let upiId = null;
    State.state.paymentMethods.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.id;
      const icon = State.getPaymentMethodIcon(p.name);
      opt.innerText = `${icon}  ${p.name}`;
      if (p.name.toLowerCase().includes("upi")) upiId = p.id;
      pmSelect.appendChild(opt);
    });

    const targetId = selectedId || upiId || (State.state.paymentMethods[0] ? State.state.paymentMethods[0].id : null);
    if (targetId) pmSelect.value = targetId;
  }

  function openAddTxModal(type = "expense") {
    const form = document.getElementById("transactionForm");
    if (form && !form.dataset.editId) {
      form.reset();
      delete form.dataset.editId;
      document.getElementById("txDate").value = State.getTodayDateString();
      const descInput = document.getElementById("txDescription");
      if (descInput) descInput.value = "";
      const catSelect = document.getElementById("txCategory");
      if (catSelect) catSelect.value = "";
      document.querySelectorAll(".tx-quick-chip").forEach(ch => ch.classList.remove("active"));
    }
    const curPrefix = document.getElementById("txCurrencyPrefix");
    if (curPrefix) curPrefix.innerText = State.getCurrencySymbol();

    switchTxType(type);
    populateTxPaymentMethods();

    open("transactionModal");
    setTimeout(() => {
      const amtInput = document.getElementById("txAmount");
      if (amtInput) amtInput.focus();
    }, 120);
  }

  function openBudgetModal() {
    const catSelect = document.getElementById("budgetCategory");
    catSelect.innerHTML = '<option value="">Select Category</option>';
    State.state.categories.filter(c => c.type === "expense").forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.id;
      const icon = State.getCategoryIcon(c.name);
      opt.innerText = `${icon}  ${c.name}`;
      catSelect.appendChild(opt);
    });
    open("budgetModal");
  }

  function openRecurringModal() {
    const catSelect = document.getElementById("recCategory");
    catSelect.innerHTML = '<option value="">Select Category</option>';
    State.state.categories.filter(c => c.type === "expense").forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.id;
      const icon = State.getCategoryIcon(c.name);
      opt.innerText = `${icon}  ${c.name}`;
      catSelect.appendChild(opt);
    });
    document.getElementById("recStartDate").value = State.getTodayDateString();
    open("recurringModal");
  }

  return {
    open,
    close,
    closeAll,
    setupShortcuts,
    openAddTxModal,
    openBudgetModal,
    openRecurringModal,
    switchTxType,
    selectCategoryChip,
    fillDescription,
    populateTxCategories,
    populateTxPaymentMethods
  };
})();
