// Expenso Profile Menu & Account Actions Component
const ProfileMenu = (() => {
  let isOpen = false;
  let activeTrigger = null;

  function init() {
    createDropdownDOM();
    createModalsDOM();
    bindEvents();
  }

  function createDropdownDOM() {
    if (document.getElementById("profileDropdownMenu")) return;
    const menu = document.createElement("div");
    menu.id = "profileDropdownMenu";
    menu.className = "profile-dropdown";
    menu.innerHTML = `
      <div class="profile-dropdown-header">
        <div class="profile-dropdown-avatar user-avatar">U</div>
        <div class="profile-dropdown-meta">
          <div class="profile-dropdown-name user-name-display">Account</div>
          <div class="profile-dropdown-email user-email-display">user@example.com</div>
        </div>
      </div>
      <div class="profile-dropdown-divider"></div>
      <div class="profile-dropdown-list">
        <button type="button" class="profile-dropdown-item" id="pMenuEditProfile">
          <span class="pmenu-icon">✏️</span>
          <span>Edit Profile</span>
        </button>
        <button type="button" class="profile-dropdown-item" id="pMenuChangePass">
          <span class="pmenu-icon">🔑</span>
          <span>Change Password</span>
        </button>
        <button type="button" class="profile-dropdown-item" id="pMenuSettings">
          <span class="pmenu-icon">⚙️</span>
          <span>Settings</span>
        </button>
        <button type="button" class="profile-dropdown-item" id="pMenuToggleTheme">
          <span class="pmenu-icon" id="pMenuThemeIcon">🌓</span>
          <span id="pMenuThemeText">Toggle Theme</span>
        </button>
      </div>
      <div class="profile-dropdown-divider"></div>
      <div class="profile-dropdown-list">
        <button type="button" class="profile-dropdown-item danger" id="pMenuLogout">
          <span class="pmenu-icon">🚪</span>
          <span>Sign Out</span>
        </button>
      </div>
    `;
    document.body.appendChild(menu);
  }

  function createModalsDOM() {
    if (document.getElementById("editProfileModal")) return;
    const modalsContainer = document.createElement("div");
    modalsContainer.innerHTML = `
      <!-- Edit Profile Modal -->
      <div class="modal-overlay" id="editProfileModal">
        <div class="modal-card" style="max-width: 440px;">
          <div class="modal-header">
            <h3 class="modal-title">Edit Profile</h3>
            <button class="btn btn-icon-only" onclick="Modals.close('editProfileModal')">✕</button>
          </div>
          <form id="editProfileForm">
            <div class="modal-body">
              <div class="form-group">
                <label class="form-label">Full Name *</label>
                <input type="text" class="form-control" id="epName" required placeholder="Your full name">
              </div>
              <div class="form-group">
                <label class="form-label">Email (Read Only)</label>
                <input type="email" class="form-control" id="epEmail" disabled style="opacity: 0.7; cursor: not-allowed;">
              </div>
              <div class="form-group">
                <label class="form-label">Default Currency</label>
                <select class="form-control" id="epCurrency">
                  <option value="INR">₹ INR (Indian Rupee)</option>
                  <option value="USD">$ USD (US Dollar)</option>
                  <option value="EUR">€ EUR (Euro)</option>
                  <option value="GBP">£ GBP (British Pound)</option>
                </select>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" onclick="Modals.close('editProfileModal')">Cancel</button>
              <button type="submit" class="btn btn-primary" id="epSubmitBtn">Save Changes</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Change Password Modal -->
      <div class="modal-overlay" id="changePasswordModal">
        <div class="modal-card" style="max-width: 440px;">
          <div class="modal-header">
            <h3 class="modal-title">Change Password</h3>
            <button class="btn btn-icon-only" onclick="Modals.close('changePasswordModal')">✕</button>
          </div>
          <form id="changePasswordForm">
            <div class="modal-body">
              <div class="form-group">
                <label class="form-label">Current Password *</label>
                <input type="password" class="form-control" id="cpCurrent" required placeholder="••••••••">
              </div>
              <div class="form-group">
                <label class="form-label">New Password *</label>
                <input type="password" class="form-control" id="cpNew" required placeholder="At least 6 characters" minlength="6">
              </div>
              <div class="form-group">
                <label class="form-label">Confirm New Password *</label>
                <input type="password" class="form-control" id="cpConfirm" required placeholder="Repeat new password" minlength="6">
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" onclick="Modals.close('changePasswordModal')">Cancel</button>
              <button type="submit" class="btn btn-primary" id="cpSubmitBtn">Update Password</button>
            </div>
          </form>
        </div>
      </div>
    `;
    document.body.appendChild(modalsContainer);
  }

  function bindEvents() {
    const dropdown = document.getElementById("profileDropdownMenu");

    // Click outside to close
    document.addEventListener("click", (e) => {
      if (!isOpen) return;
      if (dropdown && !dropdown.contains(e.target) && !e.target.closest("#sidebarUserSnippet") && !e.target.closest("#topbarUserAvatar")) {
        close();
      }
    });

    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && isOpen) close();
    });

    // Dropdown Items
    document.getElementById("pMenuEditProfile")?.addEventListener("click", () => {
      close();
      openEditProfile();
    });

    document.getElementById("pMenuChangePass")?.addEventListener("click", () => {
      close();
      openChangePassword();
    });

    document.getElementById("pMenuSettings")?.addEventListener("click", () => {
      close();
      window.navigateToView("settings");
    });

    document.getElementById("pMenuToggleTheme")?.addEventListener("click", () => {
      const nextTheme = State.toggleTheme();
      updateThemeLabels(nextTheme);
      Toast.show(`Theme switched to ${nextTheme} mode`);
    });

    document.getElementById("pMenuLogout")?.addEventListener("click", () => {
      close();
      SettingsView.logout();
    });

    // Form handlers
    document.getElementById("editProfileForm")?.addEventListener("submit", handleProfileSubmit);
    document.getElementById("changePasswordForm")?.addEventListener("submit", handlePasswordSubmit);
  }

  function toggle(triggerEl) {
    if (isOpen && activeTrigger === triggerEl) {
      close();
    } else {
      open(triggerEl);
    }
  }

  function open(triggerEl) {
    const dropdown = document.getElementById("profileDropdownMenu");
    if (!dropdown) return;

    activeTrigger = triggerEl;
    const rect = triggerEl.getBoundingClientRect();

    // Position: check if trigger is in sidebar (bottom left) or topbar (top right)
    dropdown.style.display = "block";
    const isSidebar = triggerEl.closest(".sidebar") !== null;

    if (isSidebar) {
      dropdown.style.left = `${rect.left}px`;
      dropdown.style.bottom = `${window.innerHeight - rect.top + 8}px`;
      dropdown.style.top = "auto";
      dropdown.style.right = "auto";
    } else {
      dropdown.style.right = `${window.innerWidth - rect.right}px`;
      dropdown.style.top = `${rect.bottom + 8}px`;
      dropdown.style.left = "auto";
      dropdown.style.bottom = "auto";
    }

    updateThemeLabels(State.state.theme);
    isOpen = true;
    requestAnimationFrame(() => dropdown.classList.add("active"));
  }

  function close() {
    const dropdown = document.getElementById("profileDropdownMenu");
    if (!dropdown) return;
    dropdown.classList.remove("active");
    isOpen = false;
    activeTrigger = null;
    setTimeout(() => {
      if (!isOpen) dropdown.style.display = "none";
    }, 150);
  }

  function updateThemeLabels(theme) {
    const icon = document.getElementById("pMenuThemeIcon");
    const text = document.getElementById("pMenuThemeText");
    if (icon) icon.innerText = theme === "dark" ? "☀️" : "🌙";
    if (text) text.innerText = theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode";
  }

  function openEditProfile() {
    const u = State.state.user;
    if (u) {
      document.getElementById("epName").value = u.name || "";
      document.getElementById("epEmail").value = u.email || "";
      document.getElementById("epCurrency").value = u.currency || State.state.currency || "INR";
    }
    Modals.open("editProfileModal");
  }

  function openChangePassword() {
    document.getElementById("changePasswordForm")?.reset();
    Modals.open("changePasswordModal");
  }

  async function handleProfileSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById("epSubmitBtn");
    const name = document.getElementById("epName").value.trim();
    const currency = document.getElementById("epCurrency").value;

    if (!name) return Toast.show("Please enter your name", "error");
    btn.disabled = true;
    try {
      const updated = await API.updateProfile({ name, currency });
      State.state.user = updated;
      State.state.currency = currency;
      window.updateUserSnippet(updated);
      Modals.close("editProfileModal");
      Toast.show("✓ Profile updated successfully!");
    } catch (err) {
      Toast.show(err.message, "error");
    } finally {
      btn.disabled = false;
    }
  }

  async function handlePasswordSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById("cpSubmitBtn");
    const currentPass = document.getElementById("cpCurrent").value;
    const newPass = document.getElementById("cpNew").value;
    const confirmPass = document.getElementById("cpConfirm").value;

    if (newPass !== confirmPass) {
      return Toast.show("New passwords do not match", "error");
    }
    if (newPass.length < 6) {
      return Toast.show("Password must be at least 6 characters", "error");
    }

    btn.disabled = true;
    try {
      await API.changePassword(currentPass, newPass);
      Modals.close("changePasswordModal");
      document.getElementById("changePasswordForm")?.reset();
      Toast.show("✓ Password changed successfully!");
    } catch (err) {
      Toast.show(err.message, "error");
    } finally {
      btn.disabled = false;
    }
  }

  return {
    init,
    toggle,
    open,
    close,
    openEditProfile,
    openChangePassword
  };
})();
