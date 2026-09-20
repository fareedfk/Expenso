// Expenso Calendar View Controller
const CalendarView = (() => {
  let month = new Date().getMonth() + 1;
  let year = new Date().getFullYear();

  async function load() {
    const title = document.getElementById("calendarTitle");
    if (title) {
      const names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
      title.innerText = `${names[month - 1]} ${year}`;
    }
    try {
      const data = await API.getCalendar(month, year);
      renderGrid(data);
    } catch (err) {
      console.error("Calendar load failed:", err);
    }
  }

  function renderGrid(data) {
    const grid = document.getElementById("calendarDaysGrid");
    if (!grid) return;
    grid.innerHTML = "";

    ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].forEach(d => {
      const el = document.createElement("div"); el.className = "calendar-day-header"; el.innerText = d; grid.appendChild(el);
    });

    const firstDay = new Date(year, month - 1, 1).getDay();
    const daysInMonth = new Date(year, month, 0).getDate();

    for (let i = 0; i < firstDay; i++) {
      const empty = document.createElement("div"); empty.className = "calendar-cell empty"; grid.appendChild(empty);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      const dStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const dayData = data[dStr];
      const cell = document.createElement("div");
      cell.className = "calendar-cell";
      cell.onclick = () => showDetail(dStr, dayData);
      cell.innerHTML = `
        <span class="cell-date">${day}</span>
        ${dayData && dayData.total_expense > 0 ? `<span class="cell-spent">${State.formatCurrency(dayData.total_expense)}</span>` : ''}
      `;
      grid.appendChild(cell);
    }
  }

  function showDetail(dStr, dData) {
    const panel = document.getElementById("calendarDayDetails");
    if (!panel) return;
    panel.style.display = "block";
    document.getElementById("calSelectedDate").innerText = State.formatDate(dStr);
    const list = document.getElementById("calDayItemsList");

    if (!dData || !dData.items || !dData.items.length) {
      list.innerHTML = '<p style="color: var(--text-muted); padding: 12px 0;">No expenses on this day.</p>';
      document.getElementById("calSelectedTotal").innerText = State.formatCurrency(0);
      return;
    }
    document.getElementById("calSelectedTotal").innerText = State.formatCurrency(dData.total_expense);
    list.innerHTML = dData.items.map(it => `
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border-subtle);">
        <div><div style="font-weight: 600;">${escapeHtml(it.description)}</div><div style="font-size: 0.75rem; color: var(--text-muted);">${escapeHtml(it.category_name)}</div></div>
        <div style="font-weight: 700; color: var(--danger);">-${State.formatCurrency(it.amount)}</div>
      </div>
    `).join("");
  }

  function prevMonth() { month--; if (month < 1) { month = 12; year--; } load(); }
  function nextMonth() { month++; if (month > 12) { month = 1; year++; } load(); }

  return { load, prevMonth, nextMonth };
})();
