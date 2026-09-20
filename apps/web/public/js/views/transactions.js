// Expenso Transactions Ledger View Controller
const TransactionsView = (() => {
  async function load() {
    try {
      const res = await API.getTransactions(State.state.txFilters);
      renderTable(res.transactions);
      renderPagination(res.total, res.page, res.limit);
    } catch (err) {
      console.error("Transactions load failed:", err);
    }
  }

  function renderTable(txs) {
    const tbody = document.getElementById("txTableBody");
    if (!tbody) return;
    if (!txs || !txs.length) {
      tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 36px; color: var(--text-muted);">No transactions match your search/filter criteria.</td></tr>';
      return;
    }
    tbody.innerHTML = txs.map(t => {
      const isInc = t.type === "income";
      return `
        <tr>
          <td style="white-space: nowrap; color: var(--text-secondary); font-size: 0.825rem;">${State.formatDate(t.transaction_date)}</td>
          <td><div style="font-weight: 600;">${escapeHtml(t.description)}</div>${t.notes ? `<div style="font-size: 0.75rem; color: var(--text-muted);">${escapeHtml(t.notes)}</div>` : ''}</td>
          <td><span class="category-tag"><span class="category-dot" style="background: ${t.category?.color || '#71717A'};"></span>${escapeHtml(t.category?.name || 'Uncategorized')}</span></td>
          <td><span style="font-size: 0.8rem; color: var(--text-secondary);">${escapeHtml(t.payment_method?.name || 'N/A')}</span></td>
          <td><span class="badge ${isInc ? 'badge-success' : 'badge-danger'}">${t.type.toUpperCase()}</span></td>
          <td class="${isInc ? 'amount-income' : 'amount-expense'}" style="text-align: right;">${isInc ? '+' : '-'}${State.formatCurrency(t.amount)}</td>
          <td style="text-align: right; white-space: nowrap;">
            <button class="btn btn-icon-only btn-sm" title="Edit" onclick="TransactionsView.openEdit(${t.id})">✏️</button>
            <button class="btn btn-icon-only btn-sm" title="Delete" style="margin-left: 4px;" onclick="TransactionsView.remove(${t.id})">🗑️</button>
          </td>
        </tr>
      `;
    }).join("");
  }

  function renderPagination(total, page, limit) {
    const el = document.getElementById("txPagination");
    if (!el) return;
    const totalPages = Math.ceil(total / limit) || 1;
    el.innerHTML = `
      <span style="font-size: 0.85rem; color: var(--text-muted);">Showing ${(page - 1) * limit + 1} - ${Math.min(page * limit, total)} of ${total}</span>
      <div style="display: flex; gap: 8px;">
        <button class="btn btn-secondary btn-sm" ${page <= 1 ? 'disabled' : ''} onclick="TransactionsView.changePage(${page - 1})">Prev</button>
        <span class="btn btn-secondary btn-sm" style="pointer-events: none;">${page} / ${totalPages}</span>
        <button class="btn btn-secondary btn-sm" ${page >= totalPages ? 'disabled' : ''} onclick="TransactionsView.changePage(${page + 1})">Next</button>
      </div>
    `;
  }

  function changePage(p) { State.state.txFilters.page = p; load(); }

  async function openEdit(id) {
    try {
      const res = await fetch(`/api/transactions/${id}`, { headers: { "Authorization": `Bearer ${API.getToken()}` } });
      const data = await res.json();
      const form = document.getElementById("transactionForm");
      form.dataset.editId = data.id;
      document.getElementById("txModalTitle").innerText = "Edit Transaction";
      document.getElementById("txAmount").value = data.amount;
      document.getElementById("txType").value = data.type;
      document.getElementById("txDescription").value = data.description;
      document.getElementById("txDate").value = data.transaction_date;
      document.getElementById("txNotes").value = data.notes || "";
      Modals.openAddTxModal(data.type);
      document.getElementById("txCategory").value = data.category_id || "";
      document.getElementById("txPaymentMethod").value = data.payment_method_id || "";
    } catch {
      Toast.show("Could not load transaction", "error");
    }
  }

  async function remove(id) {
    if (!confirm("Are you sure you want to delete this transaction?")) return;
    try {
      const res = await API.deleteTransaction(id);
      Toast.show("Transaction deleted", "info", async () => {
        if (res.deleted_data) {
          await API.createTransaction(res.deleted_data);
          Toast.show("Transaction restored!");
          load();
        }
      });
      load();
    } catch (err) { Toast.show(err.message, "error"); }
  }

  return { load, changePage, openEdit, remove };
})();
