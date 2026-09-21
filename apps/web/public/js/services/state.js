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
    if (amount === undefined || amount === null || isNaN(amount)) return `${getCurrencySymbol()}0`;
    const isNegative = amount < 0;
    const formatted = Math.abs(amount).toLocaleString("en-IN", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 2
    });
    return `${isNegative ? "-" : ""}${getCurrencySymbol()}${formatted}`;
  }

  function getTodayDateString() {
    try {
      return new Intl.DateTimeFormat("en-CA", {
        timeZone: "Asia/Kolkata",
        year: "numeric",
        month: "2-digit",
        day: "2-digit"
      }).format(new Date());
    } catch {
      const d = new Date();
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    }
  }

  function formatDate(dateStr) {
    if (!dateStr) return "";
    const str = String(dateStr).slice(0, 10);
    const parts = str.split("-");
    if (parts.length === 3) {
      const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      const y = parts[0], m = parseInt(parts[1], 10), d = parseInt(parts[2], 10);
      return `${d} ${monthNames[m - 1]} ${y}`;
    }
    return dateStr;
  }

  const CATEGORY_ICONS = {
    "food": "🍔", "dining": "🍽️", "restaurant": "🍽️", "groceries": "🥦", "shopping": "🛒",
    "transport": "🚕", "travel": "✈️", "fuel": "⛽", "petrol": "⛽", "bills": "💡",
    "utilities": "⚡", "rent": "🏠", "housing": "🏡", "entertainment": "🎬", "movie": "🍿",
    "health": "💊", "medical": "🏥", "fitness": "🏋️", "education": "📚", "books": "📖",
    "salary": "💼", "freelance": "🚀", "freelancing": "🚀", "investment": "📈", "investments": "📈",
    "dividend": "🪙", "crypto": "🪙", "bonus": "🎁", "gift": "🎀", "personal": "👤",
    "work": "💻", "tech": "💻", "others": "📦", "general": "🏷️"
  };

  const PAYMENT_ICONS = {
    "upi": "📱", "gpay": "📱", "phonepe": "📱", "paytm": "📱", "cash": "💵",
    "credit card": "💳", "credit": "💳", "debit card": "💳", "debit": "💳",
    "card": "💳", "bank transfer": "🏦", "bank": "🏦", "net banking": "🌐",
    "wallet": "👛", "cheque": "📜"
  };

  function getCategoryIcon(name) {
    if (!name) return "🏷️";
    const lower = name.toLowerCase().trim();
    for (const key in CATEGORY_ICONS) {
      if (lower.includes(key)) return CATEGORY_ICONS[key];
    }
    return "🏷️";
  }

  function getPaymentMethodIcon(name) {
    if (!name) return "💳";
    const lower = name.toLowerCase().trim();
    for (const key in PAYMENT_ICONS) {
      if (lower.includes(key)) return PAYMENT_ICONS[key];
    }
    return "💳";
  }

  function setTheme(theme) {
    state.theme = theme;
    localStorage.setItem("expenso_theme", theme);
    document.documentElement.setAttribute("data-theme", theme);
  }

  function toggleTheme() {
    const next = state.theme === "dark" ? "light" : "dark";
    setTheme(next);
    return next;
  }

  return { state, init, getCurrencySymbol, formatCurrency, formatDate, getTodayDateString, setTheme, toggleTheme, getCategoryIcon, getPaymentMethodIcon };
})();
