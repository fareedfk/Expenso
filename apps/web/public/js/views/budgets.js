// Expenso Budgets View Controller
const BudgetsView = (() => {
  async function load() {
    const today = new Date();
    try {
      const budgets = await API.getBudgets(today.getMonth() + 1, today.getFullYear());
      const grid = document.getElementById("budgetsGrid");
      if (!grid) return;
      if (!budgets || !budgets.length) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-muted); background: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-subtle);"><h3>No category budgets set for this month</h3><p style="margin: 8px 0 16px;">Set monthly limits to maintain spending discipline.</p><button class="btn btn-primary" onclick="Modals.openBudgetModal()">+ Set New Budget</button></div>';
        return;
      }
      grid.innerHTML = budgets.map(b => `
        <div class="card">
          <div class="card-header">
            <div style="display: flex; align-items: center; gap: 10px;">
              <span class="category-dot" style="width: 12px; height: 12px; background: ${b.category?.color || '#6366F1'};"></span>
              <span style="font-weight: 700; font-size: 1.1rem;">${escapeHtml(b.category?.name || 'General')}</span>
            </div>
            <button class="btn btn-icon-only btn-sm" onclick="BudgetsView.remove(${b.id})">🗑️</button>
          </div>
          <div style="margin: 16px 0;">
            <div style="font-size: 1.5rem; font-weight: 800;">
              ${State.formatCurrency(b.spent)} <span style="font-size: 0.9rem; font-weight: 500; color: var(--text-muted);">/ ${State.formatCurrency(b.amount)}</span>
            </div>
            <div style="font-size: 0.8rem; color: var(--text-secondary); margin-top: 4px;">
              ${b.remaining > 0 ? `${State.formatCurrency(b.remaining)} remaining` : 'Limit exceeded!'}
            </div>
          </div>
          <div class="progress-bar-bg" style="height: 10px;">
            <div class="progress-bar-fill ${b.status}" style="width: ${Math.min(b.percentage, 100)}%;"></div>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
            <span class="badge badge-${b.status === 'exceeded' ? 'danger' : (b.status === 'warning' ? 'warning' : 'success')}">${b.status.toUpperCase()}</span>
            <span style="font-size: 0.85rem; font-weight: 700;">${b.percentage}%</span>
          </div>
        </div>
      `).join("");
    } catch (err) {
      console.error("Budgets load failed:", err);
    }
  }

  async function remove(id) {
    if (!confirm("Remove this budget?")) return;
    try {
      await API.deleteBudget(id);
      Toast.show("Budget removed.");
      load();
    } catch (err) { Toast.show(err.message, "error"); }
  }

  return { load, remove };
})();
