// Expenso Categories & Payment Methods Management View Controller
const CategoriesView = (() => {
  let currentFilter = "all";
  let cachedUsedCategories = [];
  let cachedCatStats = {};

  async function load() {
    try {
      await window.loadCategoriesAndMethods();
      const txRes = await API.getTransactions({ limit: 500 });
      const txs = txRes?.transactions || [];

      // Calculate usage stats per category & payment method
      cachedCatStats = {};
      const pmStats = {};

      txs.forEach(t => {
        if (t.category_id) {
          if (!cachedCatStats[t.category_id]) {
            cachedCatStats[t.category_id] = { count: 0, total: 0, type: t.type };
          }
          cachedCatStats[t.category_id].count += 1;
          cachedCatStats[t.category_id].total += t.amount;
        }

        if (t.payment_method_id) {
          if (!pmStats[t.payment_method_id]) {
            pmStats[t.payment_method_id] = { count: 0, total: 0 };
          }
          pmStats[t.payment_method_id].count += 1;
          pmStats[t.payment_method_id].total += t.amount;
        }
      });

      // Filter ONLY categories with transactions
      cachedUsedCategories = State.state.categories.filter(c => cachedCatStats[c.id] && cachedCatStats[c.id].count > 0);
      cachedUsedCategories.sort((a, b) => (cachedCatStats[b.id]?.total || 0) - (cachedCatStats[a.id]?.total || 0));

      renderCategories();
      renderPaymentMethods(pmStats);
    } catch (err) {
      console.error("Failed to load active categories:", err);
    }
  }

  function setFilter(type) {
    currentFilter = type;
    document.querySelectorAll(".cat-filter-btn").forEach(btn => {
      btn.classList.toggle("active", btn.innerText.toLowerCase().includes(type) || (type === "all" && btn.innerText === "All"));
    });
    renderCategories();
  }

  function renderCategories() {
    const catList = document.getElementById("manageCategoriesList");
    if (!catList) return;

    const filtered = cachedUsedCategories.filter(c => currentFilter === "all" || c.type === currentFilter);

    if (filtered.length === 0) {
      const typeLabel = currentFilter === "all" ? "active" : currentFilter;
      catList.innerHTML = `
        <div class="empty-categories-card">
          <div class="empty-categories-icon">🏷️</div>
          <div class="empty-categories-title">No ${typeLabel} categories used yet</div>
          <p class="empty-categories-desc">Only categories with recorded transactions appear here. Record an expense or income to see it here.</p>
          <button class="btn btn-primary btn-sm" onclick="Modals.openAddTxModal('${currentFilter === 'income' ? 'income' : 'expense'}')">+ Record Transaction</button>
        </div>
      `;
      return;
    }

    catList.innerHTML = filtered.map(c => {
      const stats = cachedCatStats[c.id] || { count: 0, total: 0 };
      const icon = State.getCategoryIcon(c.name);
      const isIncome = c.type === "income";

      return `
        <div class="active-cat-card">
          <div class="active-cat-left">
            <div class="active-cat-icon-wrap">${icon}</div>
            <div class="active-cat-info">
              <span class="active-cat-name">${escapeHtml(c.name)}</span>
              <span class="active-cat-count">${stats.count} ${stats.count === 1 ? 'transaction' : 'transactions'}</span>
            </div>
          </div>
          <div class="active-cat-right">
            <span class="active-cat-amount ${c.type}">${isIncome ? '+' : '-'}${State.formatCurrency(stats.total)}</span>
            <span class="active-cat-badge ${c.type}">${c.type}</span>
          </div>
        </div>
      `;
    }).join("");
  }

  function renderPaymentMethods(pmStats = {}) {
    const pmList = document.getElementById("managePmList");
    const countEl = document.getElementById("activePmCount");
    if (!pmList) return;

    const usedPms = State.state.paymentMethods.filter(p => pmStats[p.id] && pmStats[p.id].count > 0);
    usedPms.sort((a, b) => (pmStats[b.id]?.count || 0) - (pmStats[a.id]?.count || 0));

    if (countEl) {
      countEl.innerText = `${usedPms.length} active`;
    }

    if (usedPms.length === 0) {
      pmList.innerHTML = '<div style="color: var(--text-muted); font-size: 0.85rem; padding: 12px 0;">No payment methods used yet.</div>';
      return;
    }

    pmList.innerHTML = usedPms.map(p => {
      const stats = pmStats[p.id] || { count: 0, total: 0 };
      const icon = State.getPaymentMethodIcon(p.name);
      return `
        <div class="active-pm-card">
          <div class="active-pm-left">
            <span class="active-pm-icon">${icon}</span>
            <div>
              <div class="active-pm-name">${escapeHtml(p.name)}</div>
              <div class="active-pm-count">${stats.count} ${stats.count === 1 ? 'txn' : 'txns'}</div>
            </div>
          </div>
          <div class="active-pm-total">${State.formatCurrency(stats.total)}</div>
        </div>
      `;
    }).join("");
  }

  return { load, setFilter };
})();

