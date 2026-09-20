// Expenso API Client Service
const API = (() => {
  const BASE_URL = "";

  function getToken() { return localStorage.getItem("expenso_token"); }
  function setToken(token) { localStorage.setItem("expenso_token", token); }
  function clearToken() {
    localStorage.removeItem("expenso_token");
    localStorage.removeItem("expenso_user");
  }

  function getCurrentUser() {
    const raw = localStorage.getItem("expenso_user");
    try { return raw ? JSON.parse(raw) : null; } catch { return null; }
  }
  function setCurrentUser(user) { localStorage.setItem("expenso_user", JSON.stringify(user)); }

  async function request(endpoint, options = {}) {
    const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });
    if (response.status === 401) {
      clearToken();
      window.dispatchEvent(new CustomEvent("expenso:unauthorized"));
      throw new Error("Session expired or unauthorized. Please log in.");
    }
    if (!response.ok) {
      let msg = "An error occurred";
      try { const err = await response.json(); msg = err.detail || err.message || msg; }
      catch { msg = await response.text(); }
      throw new Error(msg);
    }
    const cType = response.headers.get("content-type");
    if (cType && cType.includes("application/json")) return await response.json();
    return response;
  }

  return {
    getToken, setToken, clearToken, getCurrentUser, setCurrentUser,
    login: async (email, password) => {
      const res = await request("/api/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
      setToken(res.access_token); setCurrentUser(res.user); return res;
    },
    register: async (name, email, password, currency = "INR") => {
      const res = await request("/api/auth/register", { method: "POST", body: JSON.stringify({ name, email, password, currency }) });
      setToken(res.access_token); setCurrentUser(res.user); return res;
    },
    getMe: async () => {
      const user = await request("/api/auth/me");
      setCurrentUser(user); return user;
    },
    getTransactions: async (params = {}) => {
      const q = new URLSearchParams();
      Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== null && v !== "") q.append(k, v); });
      return await request(`/api/transactions/?${q.toString()}`);
    },
    createTransaction: async (data) => request("/api/transactions/", { method: "POST", body: JSON.stringify(data) }),
    updateTransaction: async (id, data) => request(`/api/transactions/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    deleteTransaction: async (id) => request(`/api/transactions/${id}`, { method: "DELETE" }),
    getCategories: async (type = null) => request(`/api/categories/${type ? `?type=${type}` : ""}`),
    createCategory: async (data) => request("/api/categories/", { method: "POST", body: JSON.stringify(data) }),
    deleteCategory: async (id) => request(`/api/categories/${id}`, { method: "DELETE" }),
    getPaymentMethods: async () => request("/api/payment-methods/"),
    createPaymentMethod: async (data) => request("/api/payment-methods/", { method: "POST", body: JSON.stringify(data) }),
    deletePaymentMethod: async (id) => request(`/api/payment-methods/${id}`, { method: "DELETE" }),
    getBudgets: async (month, year) => request(`/api/budgets/?month=${month}&year=${year}`),
    createBudget: async (data) => request("/api/budgets/", { method: "POST", body: JSON.stringify(data) }),
    deleteBudget: async (id) => request(`/api/budgets/${id}`, { method: "DELETE" }),
    getRecurring: async () => request("/api/recurring/"),
    createRecurring: async (data) => request("/api/recurring/", { method: "POST", body: JSON.stringify(data) }),
    processDueRecurring: async () => request("/api/recurring/process-due", { method: "POST" }),
    deleteRecurring: async (id) => request(`/api/recurring/${id}`, { method: "DELETE" }),
    getSummary: async () => request("/api/analytics/summary"),
    getMonthlyTrends: async (months = 6) => request(`/api/analytics/monthly?months=${months}`),
    getCategoryBreakdown: async (type = "expense", period = "this_month") => request(`/api/analytics/categories?type=${type}&period=${period}`),
    getCalendar: async (month, year) => request(`/api/analytics/calendar?month=${month}&year=${year}`)
  };
})();
