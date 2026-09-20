// Expenso Home Landing View Controller
const HomeView = (() => {
  async function load() {
    try {
      const [summary, cats, breakdown] = await Promise.all([
        API.getSummary(),
        API.getCategories("expense"),
        API.getCategoryBreakdown("expense", "this_month")
      ]);

      // Update balance pill
      const balEl = document.getElementById("homeCurrentBalance");
      if (balEl) balEl.innerText = State.formatCurrency(summary.total_balance);

      const todayEl = document.getElementById("homeTodayExpense");
      if (todayEl) todayEl.innerText = State.formatCurrency(summary.today_expense);

      const spendMap = {};
      if (breakdown && Array.isArray(breakdown)) {
        breakdown.forEach(b => {
          spendMap[b.category_id] = b.amount;
        });
      }

      renderQuickCategoryChips(cats, spendMap);
    } catch (err) {
      console.error("Failed to load Home view:", err);
    }
  }

  function renderQuickCategoryChips(categories, spendMap = {}) {
    const container = document.getElementById("homeQuickChips");
    if (!container) return;

    const categoryIcons = {
      "Food": "🍔",
      "Shopping": "🛒",
      "Transport": "🚕",
      "Bills": "💡",
      "Entertainment": "🎬",
      "Health": "💊",
      "Rent": "🏠",
      "Education": "📚",
      "Travel": "✈️",
      "Work": "💻",
      "Others": "📦"
    };

    // Sort by spending this month or pick top 4 prominent categories
    const sorted = [...categories].sort((a, b) => (spendMap[b.id] || 0) - (spendMap[a.id] || 0));
    const top4 = sorted.slice(0, 4);

    container.innerHTML = top4.map(c => {
      const amt = spendMap[c.id] || 0;
      const icon = categoryIcons[c.name] || "🏷️";
      return `
        <button class="quick-chip" onclick="HomeView.selectQuickCategory(${c.id}, '${escapeHtml(c.name)}')">
          <span class="quick-chip-icon">${icon}</span>
          <span class="quick-chip-name">${escapeHtml(c.name)}</span>
          <span class="quick-chip-amount">${State.formatCurrency(amt)}</span>
        </button>
      `;
    }).join("");
  }

  // Encircled Big Plus Button Action
  function onHeroPlusClick() {
    Modals.open("homeChoiceModal");
  }

  // Choosing between Expense and Income from hero
  function chooseType(type) {
    Modals.close("homeChoiceModal");
    Modals.openAddTxModal(type);
  }

  // Quick Category Chip selected directly from Home screen
  function selectQuickCategory(categoryId, categoryName) {
    Modals.openAddTxModal("expense");
    const catSelect = document.getElementById("txCategory");
    if (catSelect) catSelect.value = categoryId;
    const descInput = document.getElementById("txDescription");
    if (descInput) descInput.value = categoryName;

    // Focus on amount for immediate input
    const amtInput = document.getElementById("txAmount");
    if (amtInput) {
      amtInput.focus();
      amtInput.select();
    }
  }

  return {
    load,
    onHeroPlusClick,
    chooseType,
    selectQuickCategory
  };
})();
