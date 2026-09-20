// Expenso Categories & Payment Methods Management View Controller
const CategoriesView = (() => {
  async function load() {
    await window.loadCategoriesAndMethods();
    const catList = document.getElementById("manageCategoriesList");
    const pmList = document.getElementById("managePmList");

    if (catList) {
      catList.innerHTML = State.state.categories.map(c => `
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); margin-bottom: 8px;">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span class="category-dot" style="background: ${c.color || '#6366F1'};"></span>
            <span style="font-weight: 600;">${escapeHtml(c.name)}</span>
            <span class="badge ${c.type === 'income' ? 'badge-success' : 'badge-neutral'}">${c.type}</span>
          </div>
          ${!c.is_default ? `<button class="btn btn-icon-only btn-sm" onclick="CategoriesView.removeCategory(${c.id})">🗑️</button>` : '<span style="font-size: 0.75rem; color: var(--text-muted);">Default</span>'}
        </div>
      `).join("");
    }

    if (pmList) {
      pmList.innerHTML = State.state.paymentMethods.map(p => `
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); margin-bottom: 8px;">
          <span style="font-weight: 600;">${escapeHtml(p.name)}</span>
          <button class="btn btn-icon-only btn-sm" onclick="CategoriesView.removePm(${p.id})">🗑️</button>
        </div>
      `).join("");
    }
  }

  async function removeCategory(id) {
    if (!confirm("Delete custom category?")) return;
    try {
      await API.deleteCategory(id);
      Toast.show("Category removed.");
      load();
    } catch (err) { Toast.show(err.message, "error"); }
  }

  async function removePm(id) {
    if (!confirm("Delete payment method?")) return;
    try {
      await API.deletePaymentMethod(id);
      Toast.show("Payment method removed.");
      load();
    } catch (err) { Toast.show(err.message, "error"); }
  }

  return { load, removeCategory, removePm };
})();
