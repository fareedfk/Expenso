// Expenso Chart Component Module
const Charts = (() => {
  let spendingChart = null, doughnutChart = null, cashflowChart = null;

  function getThemeColors() {
    const isLight = document.documentElement.getAttribute("data-theme") === "light";
    return {
      text: isLight ? "#475569" : "#9CA3AF",
      grid: isLight ? "#E2E8F0" : "#262B36",
      tooltipBg: isLight ? "#FFFFFF" : "#171A21",
      tooltipText: isLight ? "#0F172A" : "#F5F5F5"
    };
  }

  function renderSpendingTrend(canvasId, monthlyData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (spendingChart) spendingChart.destroy();
    const th = getThemeColors();

    spendingChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: monthlyData.map(d => d.month_label),
        datasets: [
          { label: "Expense", data: monthlyData.map(d => d.expense), backgroundColor: "rgba(239, 68, 68, 0.75)", borderRadius: 6, barThickness: 24 },
          { label: "Income", data: monthlyData.map(d => d.income), backgroundColor: "rgba(16, 185, 129, 0.75)", borderRadius: 6, barThickness: 24 }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position: "top", align: "end", labels: { color: th.text, boxWidth: 12, usePointStyle: true } },
          tooltip: {
            backgroundColor: th.tooltipBg, titleColor: th.tooltipText, bodyColor: th.tooltipText,
            callbacks: { label: (it) => `${it.dataset.label}: ${State.formatCurrency(it.raw)}` }
          }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: th.text } },
          y: { grid: { color: th.grid }, ticks: { color: th.text, callback: (v) => State.getCurrencySymbol() + (v >= 1000 ? (v/1000).toFixed(0) + "k" : v) } }
        }
      }
    });
  }

  function renderCategoryDoughnut(canvasId, catData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (doughnutChart) doughnutChart.destroy();
    const th = getThemeColors();
    if (!catData || !catData.length) { ctx.getContext("2d").clearRect(0, 0, ctx.width, ctx.height); return; }

    doughnutChart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: catData.map(c => c.category_name),
        datasets: [{ data: catData.map(c => c.amount), backgroundColor: catData.map(c => c.category_color || "#6366F1"), borderWidth: 2, borderColor: th.tooltipBg }]
      },
      options: {
        responsive: true, maintainAspectRatio: false, cutout: "72%",
        plugins: {
          legend: { position: "right", labels: { color: th.text, boxWidth: 10, usePointStyle: true } },
          tooltip: {
            backgroundColor: th.tooltipBg, titleColor: th.tooltipText, bodyColor: th.tooltipText,
            callbacks: { label: (it) => ` ${it.label}: ${State.formatCurrency(it.raw)} (${catData[it.dataIndex]?.percentage || 0}%)` }
          }
        }
      }
    });
  }

  function renderAnalyticsTrends(canvasId, monthlyData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (cashflowChart) cashflowChart.destroy();
    const th = getThemeColors();

    cashflowChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: monthlyData.map(d => d.month_label),
        datasets: [
          { label: "Income", data: monthlyData.map(d => d.income), borderColor: "#10B981", backgroundColor: "rgba(16, 185, 129, 0.1)", fill: true, tension: 0.35 },
          { label: "Expense", data: monthlyData.map(d => d.expense), borderColor: "#EF4444", backgroundColor: "rgba(239, 68, 68, 0.1)", fill: true, tension: 0.35 },
          { label: "Net Savings", data: monthlyData.map(d => d.savings), borderColor: "#6366F1", borderDash: [5, 5], fill: false, tension: 0.3 }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { position: "top", labels: { color: th.text } },
          tooltip: { backgroundColor: th.tooltipBg, titleColor: th.tooltipText, bodyColor: th.tooltipText }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: th.text } },
          y: { grid: { color: th.grid }, ticks: { color: th.text, callback: (v) => State.getCurrencySymbol() + (v >= 1000 ? (v/1000).toFixed(0) + "k" : v) } }
        }
      }
    });
  }

  return { renderSpendingTrend, renderCategoryDoughnut, renderAnalyticsTrends };
})();
