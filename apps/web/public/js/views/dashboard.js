// Expenso Dashboard View Controller
const DashboardView = (() => {
  async function load() {
    try {
      const [summary, monthlyTrends, categoryBreakdown, budgets, recentTx] = await Promise.all([
        API.getSummary(),
        API.getMonthlyTrends(6),
        API.getCategoryBreakdown("expense", "this_month"),
        API.getBudgets(new Date().getMonth() + 1, new Date().getFullYear()),
        API.getTransactions({ limit: 5 })
      ]);

      document.getElementById("dbBalanceVal").innerText = State.formatCurrency(summary.total_balance);
      document.getElementById("dbIncomeVal").innerText = State.formatCurrency(summary.monthly_income);
      document.getElementById("dbExpenseVal").innerText = State.formatCurrency(summary.monthly_expense);
      document.getElementById("dbSavingsVal").innerText = State.formatCurrency(summary.monthly_savings);
      document.getElementById("dbTodayExpense").innerText = State.formatCurrency(summary.today_expense);
      document.getElementById("dbSavingsRate").innerText = `${summary.savings_rate}%`;

      Charts.renderSpendingTrend("dashboardTrendChart", monthlyTrends);
      Charts.renderCategoryDoughnut("dashboardCategoryChart", categoryBreakdown);
      renderBudgets(budgets);
      renderRecent(recentTx.transactions);
    } catch (err) {
      console.error("Dashboard load failed:", err);
    }
  }

  function renderBudgets(budgets) {
    const el = document.getElementById("dbBudgetList");
    if (!el) return;
    if (!budgets || !budgets.length) {
      el.innerHTML = '<div style="text-align: center; padding: 24px; color: var(--text-muted);"><p>No budgets set for this month.</p><button class="btn btn-secondary btn-sm" style="margin-top: 8px;" onclick="Modals.openBudgetModal()">+ Set Budget</button></div>';
      return;
    }
    el.innerHTML = budgets.slice(0, 4).map(b => `
      <div class="budget-item">
        <div class="budget-header">
          <span class="budget-title"><span class="category-dot" style="background: ${b.category?.color || '#6366F1'}"></span>${b.category?.name || 'General'}</span>
          <span class="budget-values"><strong>${State.formatCurrency(b.spent)}</strong> / ${State.formatCurrency(b.amount)} <span class="badge badge-${b.status === 'exceeded' ? 'danger' : (b.status === 'warning' ? 'warning' : 'success')}">${b.percentage}%</span></span>
        </div>
        <div class="progress-bar-bg"><div class="progress-bar-fill ${b.status}" style="width: ${Math.min(b.percentage, 100)}%;"></div></div>
      </div>
    `).join("");
  }

  function renderRecent(txs) {
    const el = document.getElementById("dbRecentTransactions");
    if (!el) return;
    if (!txs || !txs.length) {
      el.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 24px; color: var(--text-muted);">No recent activity.</td></tr>';
      return;
    }
    el.innerHTML = txs.map(t => {
      const isInc = t.type === "income";
      return `
        <tr style="cursor: pointer;" onclick="TransactionsView.openEdit(${t.id})">
          <td><div style="font-weight: 600;">${escapeHtml(t.description)}</div><div style="font-size: 0.75rem; color: var(--text-muted);">${State.formatDate(t.transaction_date)}</div></td>
          <td><span class="category-tag"><span class="category-dot" style="background: ${t.category?.color || '#71717A'};"></span>${escapeHtml(t.category?.name || 'Uncategorized')}</span></td>
          <td><span style="font-size: 0.8rem; color: var(--text-secondary);">${escapeHtml(t.payment_method?.name || 'Cash')}</span></td>
          <td class="${isInc ? 'amount-income' : 'amount-expense'}" style="text-align: right;">${isInc ? '+' : '-'}${State.formatCurrency(t.amount)}</td>
        </tr>
      `;
    }).join("");
  }

  return { load };
})();
