// Expenso Recurring Bills View Controller
const RecurringView = (() => {
  async function load() {
    try {
      const list = await API.getRecurring();
      const grid = document.getElementById("recurringListGrid");
      if (!grid) return;

      if (!list || !list.length) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-muted); background: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-subtle);"><h3>No recurring expenses or subscriptions set</h3><p style="margin: 8px 0 16px;">Track Netflix, Rent, Gym, and scheduled payments.</p><button class="btn btn-primary" onclick="Modals.openRecurringModal()">+ Add Recurring Bill</button></div>';
        return;
      }

      grid.innerHTML = list.map(item => `
        <div class="card">
          <div class="card-header">
            <span style="font-weight: 700; font-size: 1.1rem;">${escapeHtml(item.name)}</span>
            <button class="btn btn-icon-only btn-sm" onclick="RecurringView.remove(${item.id})">🗑️</button>
          </div>
          <div style="font-size: 1.6rem; font-weight: 800; color: var(--danger); margin: 8px 0;">
            ${State.formatCurrency(item.amount)}
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: var(--text-secondary); margin-top: 12px;">
            <span>Frequency: <strong style="text-transform: capitalize;">${item.frequency}</strong></span>
            <span>Next due: <strong>${State.formatDate(item.next_date)}</strong></span>
          </div>
        </div>
      `).join("");
    } catch (err) {
      console.error("Recurring load failed:", err);
    }
  }

  async function processDue() {
    try {
      const res = await API.processDueRecurring();
      if (res.processed_count > 0) Toast.show(`Processed ${res.processed_count} due bills!`);
      else Toast.show("No recurring bills due today.", "info");
      load();
    } catch (err) { Toast.show(err.message, "error"); }
  }

  async function remove(id) {
    if (!confirm("Delete this recurring subscription?")) return;
    try {
      await API.deleteRecurring(id);
      Toast.show("Subscription removed.");
      load();
    } catch (err) { Toast.show(err.message, "error"); }
  }

  return { load, processDue, remove };
})();
