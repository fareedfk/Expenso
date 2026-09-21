// Expenso Settings View Controller - Clean, Minimal & Essential
const SettingsView = (() => {
  function load() {
    const container = document.getElementById("settingsContainer");
    if (!container) return;

    const user = State.state.user || API.getCurrentUser() || {};
    const cur = State.state.currency || user.currency || "INR";
    const theme = State.state.theme || "dark";

    container.innerHTML = `
      <div class="settings-grid">
        <!-- 1. Profile Information -->
        <div class="card settings-card">
          <div class="card-header">
            <h3 class="card-title"><span>👤</span> Personal Profile</h3>
          </div>
          <form id="settingsProfileForm">
            <div class="form-group">
              <label class="form-label">Full Name</label>
              <input type="text" class="form-control" id="settingsName" value="${esc(user.name || '')}" placeholder="Your Name" required>
            </div>
            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" class="form-control" value="${esc(user.email || '')}" disabled style="opacity: 0.65; cursor: not-allowed;">
            </div>
            <div class="form-group">
              <label class="form-label">Default Currency</label>
              <select class="form-control" id="settingsCurrencySelect">
                <option value="INR" ${cur === 'INR' ? 'selected' : ''}>₹ INR (Indian Rupee)</option>
                <option value="USD" ${cur === 'USD' ? 'selected' : ''}>$ USD (US Dollar)</option>
                <option value="EUR" ${cur === 'EUR' ? 'selected' : ''}>€ EUR (Euro)</option>
                <option value="GBP" ${cur === 'GBP' ? 'selected' : ''}>£ GBP (British Pound)</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary btn-sm" id="btnSaveProfile">Save Profile</button>
          </form>
        </div>

        <!-- 2. Security & Password -->
        <div class="card settings-card">
          <div class="card-header">
            <h3 class="card-title"><span>🔒</span> Security & Password</h3>
          </div>
          <form id="settingsPasswordForm">
            <div class="form-group">
              <label class="form-label">Current Password</label>
              <input type="password" class="form-control" id="spCurrent" placeholder="••••••••" required>
            </div>
            <div class="form-group">
              <label class="form-label">New Password</label>
              <input type="password" class="form-control" id="spNew" placeholder="Min 6 characters" minlength="6" required>
            </div>
            <div class="form-group">
              <label class="form-label">Confirm New Password</label>
              <input type="password" class="form-control" id="spConfirm" placeholder="Repeat new password" minlength="6" required>
            </div>
            <button type="submit" class="btn btn-secondary btn-sm" id="btnSavePassword">Update Password</button>
          </form>
        </div>

        <!-- 3. Appearance & Theme -->
        <div class="card settings-card">
          <div class="card-header">
            <h3 class="card-title"><span>🎨</span> Appearance</h3>
          </div>
          <div class="form-group">
            <label class="form-label">Color Theme</label>
            <div class="theme-options-grid">
              <button type="button" class="theme-choice-card ${theme === 'dark' ? 'active' : ''}" onclick="SettingsView.changeTheme('dark')">
                <span class="theme-choice-icon">🌙</span>
                <span class="theme-choice-name">Dark Mode</span>
                <span class="theme-choice-sub">#0F1115 (OLED friendly)</span>
              </button>
              <button type="button" class="theme-choice-card ${theme === 'light' ? 'active' : ''}" onclick="SettingsView.changeTheme('light')">
                <span class="theme-choice-icon">☀️</span>
                <span class="theme-choice-name">Light Mode</span>
                <span class="theme-choice-sub">Clean & Crisp</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 4. Account Session -->
        <div class="card settings-card">
          <div class="card-header">
            <h3 class="card-title" style="color: var(--danger);"><span>🚪</span> Account Session</h3>
          </div>
          <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 16px;">
            Signed in as <strong style="color: var(--text-primary);">${esc(user.email || '')}</strong>.
          </p>
          <button type="button" class="btn btn-danger btn-sm" onclick="SettingsView.logout()">Sign Out of Expenso</button>
        </div>
      </div>
    `;

    bindSettingsEvents();
  }

  function bindSettingsEvents() {
    // Profile save
    document.getElementById("settingsProfileForm")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = document.getElementById("btnSaveProfile");
      const name = document.getElementById("settingsName").value.trim();
      const currency = document.getElementById("settingsCurrencySelect").value;
      if (!name) return Toast.show("Please enter your name", "error");

      btn.disabled = true;
      try {
        const updated = await API.updateProfile({ name, currency });
        State.state.user = updated;
        State.state.currency = currency;
        window.updateUserSnippet(updated);
        Toast.show("✓ Profile settings saved!");
      } catch (err) {
        Toast.show(err.message, "error");
      } finally {
        btn.disabled = false;
      }
    });

    // Password update
    document.getElementById("settingsPasswordForm")?.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = document.getElementById("btnSavePassword");
      const currentPass = document.getElementById("spCurrent").value;
      const newPass = document.getElementById("spNew").value;
      const confirmPass = document.getElementById("spConfirm").value;

      if (newPass !== confirmPass) {
        return Toast.show("New passwords do not match", "error");
      }
      if (newPass.length < 6) {
        return Toast.show("Password must be at least 6 characters", "error");
      }

      btn.disabled = true;
      try {
        await API.changePassword(currentPass, newPass);
        document.getElementById("settingsPasswordForm")?.reset();
        Toast.show("✓ Password changed successfully!");
      } catch (err) {
        Toast.show(err.message, "error");
      } finally {
        btn.disabled = false;
      }
    });
  }

  function changeTheme(theme) {
    State.setTheme(theme);
    load();
    Toast.show(`Switched to ${theme} mode`);
  }

  function logout() {
    API.clearToken();
    window.location.reload();
  }

  function esc(s) {
    return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  return { load, changeTheme, logout };
})();
