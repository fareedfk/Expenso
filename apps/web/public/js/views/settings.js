// Expenso Settings View Controller
const SettingsView = (() => {
  function load() {
    const curSelect = document.getElementById("settingsCurrencySelect");
    if (curSelect) curSelect.value = State.state.currency;
    const thSelect = document.getElementById("settingsThemeSelect");
    if (thSelect) thSelect.value = State.state.theme;
  }

  function changeCurrency(newCurrency) {
    State.state.currency = newCurrency;
    Toast.show(`Currency updated to ${newCurrency}`);
    window.navigateToView(State.state.currentView);
  }

  function changeTheme(theme) {
    State.setTheme(theme);
  }

  function logout() {
    API.clearToken();
    window.location.reload();
  }

  return { load, changeCurrency, changeTheme, logout };
})();
