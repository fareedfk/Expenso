// Expenso Application Main Bootstrap Orchestrator
document.addEventListener("DOMContentLoaded", () => {
  State.init();
  Modals.setupShortcuts();
  ProfileMenu.init();

  document.querySelectorAll(".nav-item, .bottom-nav-item").forEach(item => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const view = item.dataset.view;
      if (view) navigateToView(view);
    });
  });

  window.addEventListener("expenso:unauthorized", () => showAuthModal());

  if (!API.getToken()) showAuthModal();
  else loadApp();

  bindFormEvents();
});

function navigateToView(viewId) {
  State.state.currentView = viewId;
  document.body.dataset.view = viewId;

  const isHome = viewId === "home";
  const btnIncome = document.getElementById("btnAddIncome");
  const btnExpense = document.getElementById("btnAddExpense");
  if (btnIncome) btnIncome.style.display = isHome ? "none" : "";
  if (btnExpense) btnExpense.style.display = isHome ? "none" : "";

  document.querySelectorAll(".nav-item, .bottom-nav-item").forEach(el => {
    el.classList.toggle("active", el.dataset.view === viewId);
  });
  document.querySelectorAll(".page-view").forEach(pv => pv.classList.remove("active"));
  const activeView = document.getElementById(`${viewId}View`);
  if (activeView) activeView.classList.add("active");

  if (viewId === "home") HomeView.load();
  else if (viewId === "dashboard") { updateGreeting(); DashboardView.load(); }
  else if (viewId === "transactions") TransactionsView.load();
  else if (viewId === "analytics") AnalyticsView.load();
  else if (viewId === "budgets") BudgetsView.load();
  else if (viewId === "calendar") CalendarView.load();
  else if (viewId === "recurring") RecurringView.load();
  else if (viewId === "categories") CategoriesView.load();
  else if (viewId === "settings") SettingsView.load();
}
window.navigateToView = navigateToView;

async function loadApp() {
  try {
    const user = await API.getMe();
    updateUserSnippet(user);
    await loadCategoriesAndMethods();
    navigateToView("home");
  } catch {
    showAuthModal();
  }
}

function getISTInfo() {
  const now = new Date();
  try {
    const formatter = new Intl.DateTimeFormat("en-GB", {
      timeZone: "Asia/Kolkata",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hourCycle: "h23"
    });
    const parts = formatter.format(now).split(":");
    const hour = parseInt(parts[0], 10);
    const minute = parseInt(parts[1], 10);

    const timeFormatted = new Intl.DateTimeFormat("en-IN", {
      timeZone: "Asia/Kolkata",
      hour: "numeric",
      minute: "2-digit",
      hour12: true
    }).format(now);

    return { hour, minute, timeFormatted };
  } catch {
    const hour = now.getHours();
    return {
      hour,
      minute: now.getMinutes(),
      timeFormatted: now.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })
    };
  }
}

function updateGreeting(user) {
  const currentUser = user || State.state.user;
  if (!currentUser) return;
  State.state.user = currentUser;

  const ist = getISTInfo();
  let greeting = "Good evening";
  let emoji = "👋";

  // Natural Indian time ranges (IST):
  // 04:00 - 11:59: Good morning 🌅
  // 12:00 - 16:59: Good afternoon ☀️
  // 17:00 - 21:59: Good evening 🌆
  // 22:00 - 03:59: Good night 🌙
  if (ist.hour >= 4 && ist.hour < 12) {
    greeting = "Good morning";
    emoji = "🌅";
  } else if (ist.hour >= 12 && ist.hour < 17) {
    greeting = "Good afternoon";
    emoji = "☀️";
  } else if (ist.hour >= 17 && ist.hour < 22) {
    greeting = "Good evening";
    emoji = "🌆";
  } else {
    greeting = "Good night";
    emoji = "🌙";
  }

  const firstName = currentUser.name ? currentUser.name.split(" ")[0] : "";
  const greetingEl = document.getElementById("dashboardGreeting");
  if (greetingEl) {
    greetingEl.innerText = `${greeting}, ${firstName} ${emoji}`;
  }

  const istClockEl = document.getElementById("istLiveTime");
  if (istClockEl) {
    istClockEl.innerText = `${ist.timeFormatted} IST`;
  }
}
window.updateGreeting = updateGreeting;

function updateUserSnippet(user) {
  if (!user) return;
  State.state.user = user;
  document.querySelectorAll(".user-name-display").forEach(el => el.innerText = user.name);
  document.querySelectorAll(".user-email-display").forEach(el => el.innerText = user.email);
  document.querySelectorAll(".user-avatar").forEach(el => el.innerText = user.name.charAt(0).toUpperCase());

  updateGreeting(user);
}

// Live sync: keep IST greeting and time badge updated every 10s
if (!window._istLiveInterval) {
  window._istLiveInterval = setInterval(() => {
    if (State.state.user) updateGreeting();
  }, 10000);
}


async function loadCategoriesAndMethods() {
  try {
    const [cats, pms] = await Promise.all([API.getCategories(), API.getPaymentMethods()]);
    State.state.categories = cats;
    State.state.paymentMethods = pms;
    populateDropdowns();
  } catch (err) { console.error("Loading categories/methods error:", err); }
}
window.loadCategoriesAndMethods = loadCategoriesAndMethods;

function populateDropdowns() {
  document.querySelectorAll(".category-select-dropdown").forEach(sel => {
    const prev = sel.value;
    sel.innerHTML = '<option value="">All Categories</option>';
    State.state.categories.forEach(c => {
      const icon = State.getCategoryIcon(c.name);
      sel.innerHTML += `<option value="${c.id}">${icon}  ${c.name} (${c.type})</option>`;
    });
    if (prev) sel.value = prev;
  });
  document.querySelectorAll(".pm-select-dropdown").forEach(sel => {
    const prev = sel.value;
    sel.innerHTML = '<option value="">All Payment Methods</option>';
    State.state.paymentMethods.forEach(p => {
      const icon = State.getPaymentMethodIcon(p.name);
      sel.innerHTML += `<option value="${p.id}">${icon}  ${p.name}</option>`;
    });
    if (prev) sel.value = prev;
  });
}

function bindFormEvents() {
  document.getElementById("btnAddExpense")?.addEventListener("click", () => Modals.openAddTxModal("expense"));
  document.getElementById("btnAddIncome")?.addEventListener("click", () => Modals.openAddTxModal("income"));
  document.getElementById("mobileFabBtn")?.addEventListener("click", () => Modals.openAddTxModal("expense"));
  document.getElementById("commandBarTrigger")?.addEventListener("click", () => Modals.open("commandModal"));

  document.getElementById("quickCommandForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = document.getElementById("commandBarInput");
    const parsed = Command.parse(input.value);
    if (!parsed) { Toast.show("Format not recognized. Example: 'Add 250 for dinner'", "error"); return; }
    try {
      await API.createTransaction(parsed);
      Modals.close("commandModal");
      input.value = "";
      Toast.show(`✓ Added ${parsed.type}: ${parsed.description} (${State.formatCurrency(parsed.amount)})`);
      navigateToView(State.state.currentView);
    } catch (err) { Toast.show(err.message, "error"); }
  });

  document.getElementById("transactionForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const txId = form.dataset.editId;
    const type = document.getElementById("txType").value;
    const catId = parseInt(document.getElementById("txCategory").value) || null;
    let pmId = parseInt(document.getElementById("txPaymentMethod").value) || null;
    if (!pmId && State.state.paymentMethods?.length) {
      const upi = State.state.paymentMethods.find(p => p.name.toLowerCase().includes("upi"));
      pmId = upi ? upi.id : State.state.paymentMethods[0].id;
    }
    let desc = "";
    if (type === "expense") {
      desc = document.getElementById("txDescription")?.value?.trim() || "";
    }
    if (!desc) {
      const cat = catId ? State.state.categories.find(c => c.id === catId) : null;
      desc = cat ? cat.name : (type === "income" ? "Income" : "Expense");
    }
    const payload = {
      amount: parseFloat(document.getElementById("txAmount").value),
      type,
      description: desc,
      category_id: catId,
      payment_method_id: pmId,
      transaction_date: document.getElementById("txDate").value,
      notes: document.getElementById("txNotes").value.trim() || null
    };
    try {
      if (txId) { await API.updateTransaction(txId, payload); Toast.show("Transaction updated!"); }
      else { await API.createTransaction(payload); Toast.show(`✓ ${payload.type === 'expense' ? 'Expense' : 'Income'} recorded!`); }
      Modals.close("transactionModal");
      form.reset();
      delete form.dataset.editId;
      navigateToView(State.state.currentView);
    } catch (err) { Toast.show(err.message, "error"); }
  });

  document.getElementById("txSearchInput")?.addEventListener("input", debounce((e) => {
    State.state.txFilters.search = e.target.value; State.state.txFilters.page = 1; TransactionsView.load();
  }, 300));
  document.getElementById("txTypeFilter")?.addEventListener("change", (e) => {
    State.state.txFilters.type = e.target.value; State.state.txFilters.page = 1; TransactionsView.load();
  });
  document.getElementById("txCategoryFilter")?.addEventListener("change", (e) => {
    State.state.txFilters.category_id = e.target.value; State.state.txFilters.page = 1; TransactionsView.load();
  });
  document.getElementById("txPmFilter")?.addEventListener("change", (e) => {
    State.state.txFilters.payment_method_id = e.target.value; State.state.txFilters.page = 1; TransactionsView.load();
  });
  document.getElementById("txClearFiltersBtn")?.addEventListener("click", () => {
    State.state.txFilters = { type: "", category_id: "", payment_method_id: "", from_date: "", to_date: "", search: "", page: 1, limit: 50 };
    document.getElementById("txSearchInput").value = "";
    document.getElementById("txTypeFilter").value = "";
    document.getElementById("txCategoryFilter").value = "";
    document.getElementById("txPmFilter").value = "";
    TransactionsView.load();
  });

  document.getElementById("btnExportCsv")?.addEventListener("click", () => {
    fetch("/api/export/csv", { headers: { "Authorization": `Bearer ${API.getToken()}` } })
      .then(res => res.blob()).then(blob => {
        const a = document.createElement("a");
        a.href = window.URL.createObjectURL(blob);
        a.download = `expenso_transactions_${State.getTodayDateString()}.csv`;
        a.click(); a.remove();
        Toast.show("Transactions CSV downloaded!");
      }).catch(() => Toast.show("Export failed", "error"));
  });

  document.getElementById("calPrevMonthBtn")?.addEventListener("click", () => CalendarView.prevMonth());
  document.getElementById("calNextMonthBtn")?.addEventListener("click", () => CalendarView.nextMonth());
  document.getElementById("btnProcessRecurring")?.addEventListener("click", () => RecurringView.processDue());

  document.getElementById("recurringForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await API.createRecurring({
        name: document.getElementById("recName").value.trim(),
        amount: parseFloat(document.getElementById("recAmount").value),
        category_id: parseInt(document.getElementById("recCategory").value) || null,
        frequency: document.getElementById("recFrequency").value,
        start_date: document.getElementById("recStartDate").value,
        is_active: true
      });
      Modals.close("recurringModal");
      Toast.show("Recurring subscription added!");
      RecurringView.load();
    } catch (err) { Toast.show(err.message, "error"); }
  });

  document.getElementById("budgetForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await API.createBudget({
        category_id: parseInt(document.getElementById("budgetCategory").value),
        amount: parseFloat(document.getElementById("budgetAmount").value),
        month: new Date().getMonth() + 1,
        year: new Date().getFullYear()
      });
      Modals.close("budgetModal");
      Toast.show("Budget saved!");
      BudgetsView.load();
    } catch (err) { Toast.show(err.message, "error"); }
  });

  document.getElementById("settingsCurrencySelect")?.addEventListener("change", (e) => SettingsView.changeCurrency(e.target.value));
  document.getElementById("settingsThemeSelect")?.addEventListener("change", (e) => SettingsView.changeTheme(e.target.value));
  document.getElementById("btnLogout")?.addEventListener("click", () => SettingsView.logout());
}

function showAuthModal() {
  Modals.open("authModal");
  const lForm = document.getElementById("loginForm"), rForm = document.getElementById("registerForm");
  const link = document.getElementById("authToggleLink"), err = document.getElementById("authErrorMsg");

  // Clear inputs to ensure clean slate
  const loginEmail = document.getElementById("loginEmail");
  const loginPass = document.getElementById("loginPassword");
  const regName = document.getElementById("regName");
  const regEmail = document.getElementById("regEmail");
  const regPass = document.getElementById("regPassword");
  if (loginEmail) loginEmail.value = "";
  if (loginPass) loginPass.value = "";
  if (regName) regName.value = "";
  if (regEmail) regEmail.value = "";
  if (regPass) regPass.value = "";
  if (err) err.innerText = "";

  lForm.onsubmit = async (e) => {
    e.preventDefault();
    try {
      await API.login(loginEmail.value.trim(), loginPass.value);
      Modals.close("authModal"); Toast.show("Welcome back!"); loadApp();
    } catch (e) { err.innerText = e.message; }
  };

  rForm.onsubmit = async (e) => {
    e.preventDefault();
    try {
      await API.register(regName.value.trim(), regEmail.value.trim(), regPass.value);
      Modals.close("authModal"); Toast.show("Account created successfully!"); loadApp();
    } catch (e) { err.innerText = e.message; }
  };

  link.onclick = (e) => {
    e.preventDefault();
    const isLogin = lForm.style.display !== "none";
    lForm.style.display = isLogin ? "none" : "block";
    rForm.style.display = isLogin ? "block" : "none";
    document.getElementById("authModalTitle").innerText = isLogin ? "Create Account" : "Welcome to Expenso";
    link.innerText = isLogin ? "Already have an account? Log In" : "Don't have an account? Sign Up";
    err.innerText = "";
  };
}
window.showAuthModal = showAuthModal;

function escapeHtml(s) { return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
function debounce(fn, wait) {
  let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), wait); };
}
