// College Deck Interactive Controller & DOM Renderer
// Decomposed to ensure modularity (< 500 LOC per file)

const CollegeDeck = (() => {
  let currentIndex = 0;
  let totalSlides = 0;
  let slides = [];
  let indicator = null;

  function renderSlideHTML(sld, idx, total, student) {
    const snumStr = String(idx + 1).padStart(2, "0");
    const totalStr = String(total).padStart(2, "0");
    const activeClass = idx === 0 ? " active" : "";

    // 1. Cover Slide
    if (sld.type === "cover") {
      return `
      <section class="slide cover-slide${activeClass}">
        <img src="/static/aietm_logo.png" alt="AIETM Crest" class="cover-logo">
        <h1 class="cover-title">${sld.title}</h1>
        <h2 class="cover-subtitle">${sld.subtitle}</h2>
        <p class="cover-course">${student.course}</p>
        <p class="cover-college">${student.college}</p>
        <p class="cover-session">${student.year}</p>
        <div class="cover-divider"></div>
        <div class="cover-footer-grid">
          <div class="cover-footer-box">
            <div class="label">Submitted by:</div>
            <div class="person">${student.name}</div>
            <div style="color: #64748B;">Roll No: ${student.roll}</div>
          </div>
          <div class="cover-footer-box right">
            <div class="label">Submitted to:</div>
            <div class="person">${student.submitted_to}</div>
            <div style="color: #64748B;">${student.designation}</div>
          </div>
        </div>
      </section>`;
    }

    // 2. Closing Slide
    if (sld.type === "closing") {
      return `
      <section class="slide cover-slide${activeClass}">
        <img src="/static/aietm_logo.png" alt="AIETM Crest" class="cover-logo">
        <h1 class="cover-title" style="font-size: 2.8rem; color: var(--primary-navy);">${sld.title}</h1>
        <h2 class="cover-subtitle" style="color: var(--accent-gold); font-size: 1.6rem; font-style: normal;">${sld.subtitle}</h2>
        <div class="cover-divider" style="margin: 20px 0;"></div>
        <p style="font-size: 1.15rem; font-weight: 700; color: #1E293B;">${student.project}</p>
        <p style="font-size: 1rem; color: #334155; margin-top: 6px;"><strong>Presented by:</strong> ${student.name} (Roll No: ${student.roll})</p>
        <p style="font-size: 0.95rem; color: #475569; margin-top: 4px;"><strong>Guided by:</strong> ${student.submitted_to} ${student.designation}</p>
        <p style="font-size: 0.9rem; color: #64748B; margin-top: 4px;">${student.college}</p>
      </section>`;
    }

    // Standard Header & Footer builder
    const headerHtml = `
      <div class="slide-header">
        <div class="slide-header-left">
          <img src="/static/aietm_logo.png" alt="AIETM">
          <div>
            <div class="slide-tag">${sld.tag}</div>
            <div class="slide-title">${sld.title}</div>
          </div>
        </div>
        <div class="slide-page-num">${snumStr} / ${totalStr}</div>
      </div>`;

    const footerHtml = `
      <div class="slide-footer">
        <span>Expenso Project Presentation</span>
        <span>${student.name} (${student.roll}) | AIETM Jaipur</span>
      </div>`;

    let bodyHtml = "";

    // 3. UI Screenshot Slide
    if (sld.type === "screenshot") {
      const bulletsList = sld.bullets.map(b => `<li>${b}</li>`).join("");
      bodyHtml = `
        <div class="grid-2" style="align-items: center; gap: 24px;">
          <div style="background: #F8FAFC; border: 1.5px solid #CBD5E1; border-radius: 12px; padding: 10px; box-shadow: 0 4px 14px rgba(0,0,0,0.06); text-align: center;">
            <span style="background: ${sld.bg}; color: ${sld.accent}; font-weight: 700; padding: 4px 12px; border-radius: 12px; font-size: 0.76rem; margin-bottom: 8px; display: inline-block;">📸 LIVE APPLICATION VIEW</span>
            <img src="${sld.img}" alt="${sld.alt}" style="width: 100%; border-radius: 8px; border: 1px solid #E2E8F0; display: block;">
          </div>
          <div class="card" style="border-color: ${sld.border}; padding: 18px;">
            <div class="card-top-stripe" style="background: ${sld.accent};"></div>
            <div class="card-title" style="color: ${sld.accent}; font-size: 1.15rem; margin-bottom: 8px;">💡 What You See Here (Beginner Guide)</div>
            <p style="color: #475569; font-size: 0.88rem; line-height: 1.4; margin-bottom: 12px;">${sld.overview}</p>
            <ul class="bullet-list" style="font-size: 0.84rem; line-height: 1.42;">${bulletsList}</ul>
            <div style="background: ${sld.bg}; border: 1px solid ${sld.border}; border-radius: 8px; padding: 10px; margin-top: 14px;">
              <span style="font-weight: 700; color: ${sld.text_color}; font-size: 0.82rem;">✨ Beginner Benefit:</span>
              <span style="color: ${sld.text_color}; font-size: 0.82rem;"> ${sld.tip}</span>
            </div>
          </div>
        </div>`;
    }
    // 4. Two Column Cards Slide
    else if (sld.type === "two_column_cards") {
      const leftBg = sld.left.bg ? `background: ${sld.left.bg}; border-color: ${sld.left.border};` : "";
      const rightBg = sld.right.bg ? `background: ${sld.right.bg}; border-color: ${sld.right.border};` : "";
      const leftItems = sld.left.items.map(i => `<li>${i}</li>`).join("");
      const rightItems = sld.right.items.map(i => `<li>${i}</li>`).join("");

      let pillsHtml = "";
      if (sld.pills) {
        const pillsContent = sld.pills.map(p => `
          <div class="card" style="flex: 1; text-align: center; background: #EFF6FF; border-color: #93C5FD;">
            <div style="font-weight: 800; font-size: 1.15rem; color: #1E3A8A;">${p.title}</div>
            <div style="font-size: 0.82rem; color: #475569; margin-top: 4px;">${p.sub}</div>
          </div>`).join("");
        pillsHtml = `<div style="display: flex; gap: 16px; margin-top: 16px;">${pillsContent}</div>`;
      }

      bodyHtml = `
        <div class="grid-2">
          <div class="card" style="${leftBg}">
            <div class="card-top-stripe" style="background: ${sld.left.stripe};"></div>
            <div class="card-title" style="color: ${sld.left.stripe};">${sld.left.title}</div>
            <ul class="bullet-list">${leftItems}</ul>
          </div>
          <div class="card" style="${rightBg}">
            <div class="card-top-stripe" style="background: ${sld.right.stripe};"></div>
            <div class="card-title" style="color: ${sld.right.stripe};">${sld.right.title}</div>
            <ul class="bullet-list">${rightItems}</ul>
          </div>
        </div>
        ${pillsHtml}`;
    }
    // 5. Grid of 4 Cards
    else if (sld.type === "grid_4") {
      const cardsHtml = sld.cards.map(c => {
        let content = c.desc ? `<p style="font-size: 0.88rem; color: #475569; line-height: 1.45;">${c.desc}</p>` : "";
        if (c.list) {
          content = `<ul class="bullet-list" style="font-size: 0.84rem;">${c.list.map(li => `<li>${li}</li>`).join("")}</ul>`;
        }
        return `
          <div class="card">
            <div class="card-top-stripe" style="background: ${c.stripe};"></div>
            <div class="card-title" style="color: ${c.stripe};">${c.title}</div>
            ${content}
          </div>`;
      }).join("");
      bodyHtml = `<div class="grid-4">${cardsHtml}</div>`;
    }
    // 6. Three Tiers Architecture
    else if (sld.type === "tiers") {
      const tiersHtml = sld.tiers.map((t, tidx) => `
        <div class="tier-card">
          <div class="tier-header">
            <div class="tier-number">${tidx + 1}</div>
            <div>
              <div class="tier-title">${t.num}</div>
              <div class="tier-sub">${t.sub}</div>
            </div>
          </div>
          <ul class="bullet-list" style="margin-top: 12px; font-size: 0.84rem;">
            ${t.bullets.map(b => `<li>${b}</li>`).join("")}
          </ul>
        </div>`).join("");
      bodyHtml = `<div class="grid-3">${tiersHtml}</div>`;
    }
    // 7. Database Design
    else if (sld.type === "database") {
      bodyHtml = `
        <div class="grid-2" style="margin-bottom: 16px;">
          <div class="card" style="border-color: #93C5FD;">
            <div class="card-top-stripe" style="background: var(--primary-navy);"></div>
            <div class="card-title" style="color: var(--primary-navy);">👤 Table: users</div>
            <table class="presentation-table">
              <tr><th>Column</th><th>Type</th><th>Constraint</th></tr>
              <tr><td>id</td><td>INTEGER</td><td>PRIMARY KEY</td></tr>
              <tr><td>username</td><td>VARCHAR(50)</td><td>UNIQUE, NOT NULL</td></tr>
              <tr><td>email</td><td>VARCHAR(100)</td><td>UNIQUE, NOT NULL</td></tr>
              <tr><td>full_name</td><td>VARCHAR(100)</td><td>NULLABLE</td></tr>
              <tr><td>hashed_password</td><td>VARCHAR(255)</td><td>Bcrypt Hash</td></tr>
              <tr><td>created_at</td><td>TIMESTAMP</td><td>DEFAULT UTC NOW</td></tr>
            </table>
          </div>
          <div class="card" style="border-color: #C4B5FD;">
            <div class="card-top-stripe" style="background: var(--accent-purple);"></div>
            <div class="card-title" style="color: var(--accent-purple);">💳 Table: transactions</div>
            <table class="presentation-table">
              <tr><th>Column</th><th>Type</th><th>Constraint</th></tr>
              <tr><td>id</td><td>INTEGER</td><td>PRIMARY KEY</td></tr>
              <tr><td>user_id</td><td>INTEGER</td><td>FOREIGN KEY (users.id)</td></tr>
              <tr><td>type</td><td>VARCHAR(10)</td><td>'expense' | 'income'</td></tr>
              <tr><td>amount</td><td>FLOAT</td><td>NOT NULL (> 0.0)</td></tr>
              <tr><td>category</td><td>VARCHAR(50)</td><td>Food, Travel, etc.</td></tr>
              <tr><td>payment_mode</td><td>VARCHAR(30)</td><td>DEFAULT 'UPI'</td></tr>
            </table>
          </div>
        </div>
        <div class="card" style="background: #FEF3C7; border-color: #F59E0B; text-align: center; padding: 10px;">
          <span style="font-weight: 700; color: #92400E; font-size: 0.95rem;">🔗 Foreign Key Constraint: transactions.user_id ➔ users.id [ON DELETE CASCADE]</span>
        </div>`;
    }
    // 8. QA Testing
    else if (sld.type === "qa_testing") {
      const rowsHtml = sld.tests.map(tc => `
        <tr>
          <td style="font-weight: 700; color: #1E3A8A;">${tc.name}</td>
          <td>${tc.desc}</td>
          <td><span class="badge badge-success">${tc.status}</span></td>
        </tr>`).join("");
      const statsHtml = sld.stats.map(st => `
        <div class="card" style="flex: 1; text-align: center; background: #F0FDF4; border-color: #86EFAC;">
          <div style="font-weight: 800; font-size: 1.25rem; color: #16A34A;">${st.val}</div>
          <div style="font-size: 0.8rem; color: #475569; margin-top: 4px;">${st.label}</div>
        </div>`).join("");

      bodyHtml = `
        <div class="card" style="margin-bottom: 16px;">
          <div class="card-top-stripe" style="background: var(--accent-green);"></div>
          <table class="presentation-table">
            <tr><th>Test Module</th><th>Description & Assertion</th><th>Status</th></tr>
            ${rowsHtml}
          </table>
        </div>
        <div style="display: flex; gap: 16px;">${statsHtml}</div>`;
    }

    return `
      <section class="slide${activeClass}">
        ${headerHtml}
        <div class="slide-body">${bodyHtml}</div>
        ${footerHtml}
      </section>`;
  }

  function init() {
    const canvas = document.getElementById("slideCanvas");
    indicator = document.getElementById("slideIndicator");
    if (!canvas || typeof COLLEGE_WEB_SLIDES === "undefined") return;

    totalSlides = COLLEGE_WEB_SLIDES.length;
    const slidesHtml = COLLEGE_WEB_SLIDES.map((s, i) =>
      renderSlideHTML(s, i, totalSlides, COLLEGE_STUDENT_INFO)
    ).join("\n");

    canvas.innerHTML = slidesHtml;
    slides = canvas.querySelectorAll(".slide");

    updateSlide(0);

    window.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === " " || e.key === "PageDown") {
        nextSlide();
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        prevSlide();
      } else if (e.key === "f" || e.key === "F") {
        toggleFullScreen();
      }
    });
  }

  function updateSlide(index) {
    if (!slides.length) return;
    if (index < 0) index = 0;
    if (index >= totalSlides) index = totalSlides - 1;
    currentIndex = index;
    slides.forEach((s, i) => {
      s.classList.toggle("active", i === currentIndex);
    });
    if (indicator) {
      indicator.textContent = `Slide ${currentIndex + 1} of ${totalSlides}`;
    }
  }

  function nextSlide() { updateSlide(currentIndex + 1); }
  function prevSlide() { updateSlide(currentIndex - 1); }

  function toggleFullScreen() {
    const elem = document.getElementById("slideCanvas");
    if (!document.fullscreenElement) {
      elem.requestFullscreen().catch(err => alert(`Fullscreen error: ${err.message}`));
    } else {
      document.exitFullscreen();
    }
  }

  window.addEventListener("DOMContentLoaded", init);

  return {
    nextSlide,
    prevSlide,
    toggleFullScreen,
    updateSlide
  };
})();
