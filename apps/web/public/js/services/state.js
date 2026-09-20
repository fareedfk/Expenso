// Expenso State Store & Formatters Service
const State = (() => {
  const CURRENCY_SYMBOLS = {
    INR: "₹", USD: "$", EUR: "€", GBP: "£", JPY: "¥", CAD: "CA$", AUD: "AU$", AED: "AED ", PKR: "₨ "
  };

  const state = {
    user: null,
    currentView: "dashboard",
    categories: [],
    paymentMethods: [],
    currency: "INR",
    theme: "dark",
    txFilters: { type: "", category_id: "", payment_method_id: "", from_date: "", to_date: "", search: "", page: 1, limit: 50 }
  };

  function init() {
    state.user = API.getCurrentUser();
    if (state.user && state.user.currency) state.currency = state.user.currency;
    const savedTheme = localStorage.getItem("expenso_theme") || "dark";
    setTheme(savedTheme);
  }

  function getCurrencySymbol() { return CURRENCY_SYMBOLS[state.currency] || "₹"; }

  function formatCurrency(amount) {
    if (amount === undefined || amount === null) return `${getCurrencySymbol()}0`;
    const formatted = Math.abs(amount).toLocaleString("en-IN", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2
    });
    return `${getCurrencySymbol()}${formatted}`;
  }

  function formatDate(dateStr) {
    if (!dateStr) return "";
    return new Date(dateStr).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
  }

  function setTheme(theme) {
    state.theme = theme;
    localStorage.setItem("expenso_theme", theme);
    document.documentElement.setAttribute("data-theme", theme);
  }

  return { state, init, getCurrencySymbol, formatCurrency, formatDate, setTheme };
})();
