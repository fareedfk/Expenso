// Expenso Analytics View Controller
const AnalyticsView = (() => {
  async function load() {
    const period = document.getElementById("analyticsPeriodSelect")?.value || "this_month";
    try {
      const [summary, monthlyTrends, categoryBreakdown] = await Promise.all([
        API.getSummary(),
        API.getMonthlyTrends(6),
        API.getCategoryBreakdown("expense", period)
      ]);
      document.getElementById("analyticsAvgDaily").innerText = State.formatCurrency(summary.monthly_expense / 30);
      document.getElementById("analyticsSavingsRate").innerText = `${summary.savings_rate}%`;
      document.getElementById("analyticsTotalTxs").innerText = summary.transaction_count;

      const top = categoryBreakdown[0];
      document.getElementById("analyticsTopCat").innerText = top ? `${top.category_name} (${top.percentage}%)` : "None";

      Charts.renderAnalyticsTrends("analyticsCashflowChart", monthlyTrends);
      Charts.renderCategoryDoughnut("analyticsCategoryChart", categoryBreakdown);
    } catch (err) {
      console.error("Analytics load failed:", err);
    }
  }

  return { load };
})();
