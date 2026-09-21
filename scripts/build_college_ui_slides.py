# UI Screenshot Slides for Expenso Presentation Deck
# Designed for college defense / viva: visual, intuitive, and beginner-friendly.
from scripts.college_xml_helpers import (
    W, H, para, bullet_para, text_box, rect_shape, pic_shape,
    build_header_footer, wrap_slide
)

UI_SLIDES = [
    {
        "id": "quick_record",
        "tag": "LIVE DEMO • 1-TAP QUICK RECORD",
        "title": "Home Screen: Fast 1-Tap Expense Logger",
        "img_filename": "quick_record_ui.png",
        "accent": "059669",
        "tip_bg": "ECFDF5",
        "tip_border": "A7F3D0",
        "tip_text_color": "065F46",
        "aspect": 1.662,
        "overview": "Designed for zero-effort habit tracking. Anyone can record daily expenses in under 2 seconds without navigating through complex sub-menus.",
        "bullets": [
            "Big Green (+) Action: Centered for instant thumb reach; opens the entry popup in one single tap.",
            "Live Balance Ticker: See your available balance (₹4,383) and today's total spending (₹3,851) at all times.",
            "Quick-Category Chips: One tap on Food (₹930) or Shopping (₹1,214) pre-fills your most frequent expenses.",
            "Smart Natural Input (Ctrl+K): Type 'Add ₹250 for dinner' and AI detects the category automatically."
        ],
        "tip": "No accounting knowledge needed. It works like sending a quick chat message."
    },
    {
        "id": "dashboard",
        "tag": "LIVE DEMO • FINANCIAL DASHBOARD",
        "title": "Interactive Dashboard & Visual Analytics",
        "img_filename": "dashboard_ui.png",
        "accent": "2563EB",
        "tip_bg": "EFF6FF",
        "tip_border": "BFDBFE",
        "tip_text_color": "1E40AF",
        "aspect": 1.595,
        "overview": "Translates complex numbers into simple, colorful charts so beginners instantly know where their money went and how much they saved.",
        "bullets": [
            "4 Core Summary Cards: Clear numbers for Total Balance, Monthly Income, Monthly Expenses, and Savings.",
            "Savings Rate (53.2%): Tells you in green if you are saving enough money this month.",
            "Spending Overview Bar Chart: Compares cash coming in vs going out across months.",
            "Category Donut Chart: Shows exact percentage spent on Food, Transport, Shopping, and Health."
        ],
        "tip": "You understand your complete monthly financial health in just 5 seconds."
    },
    {
        "id": "transactions",
        "tag": "LIVE DEMO • FINANCIAL LEDGER",
        "title": "Smart Ledger: Filterable Money Diary",
        "img_filename": "transactions_ui.png",
        "accent": "7C3AED",
        "tip_bg": "F5F3FF",
        "tip_border": "DDD6FE",
        "tip_text_color": "5B21B6",
        "aspect": 1.660,
        "overview": "An organized digital passbook where every rupee is tracked with clear color codes, instant search, and export capabilities.",
        "bullets": [
            "Color-Coded Badges: Green (+₹7,000) for Income and Red (-₹890) for Expenses — impossible to confuse.",
            "Instant Keyword Search: Find past spends like 'gym', 'movie', or 'groceries' in milliseconds.",
            "Category & Mode Filters: Filter by Payment Method (UPI, Cash) or Category with 1 click.",
            "One-Click CSV Export: Download your full transaction history to Excel for personal records or taxes."
        ],
        "tip": "Never wonder where your cash disappeared at the end of the month."
    },
    {
        "id": "budgets",
        "tag": "LIVE DEMO • CATEGORY BUDGETS",
        "title": "Budget Guardrails: Avoid Month-End Deficit",
        "img_filename": "budgets_ui.png",
        "accent": "D97706",
        "tip_bg": "FFFBEB",
        "tip_border": "FDE68A",
        "tip_text_color": "92400E",
        "aspect": 1.806,
        "overview": "Set monthly spending limits for categories like Food and Shopping. Visual progress meters guide you before you overspend.",
        "bullets": [
            "Visual Progress Meters: Green bars show percentage consumed (e.g., Shopping: 60.7%, Food: 46.5%).",
            "Live Remaining Balances: Exact cash left displayed upfront (e.g. '₹1,070 remaining' for food).",
            "Safe vs Danger Status: Clear 'NORMAL' green badge alerts you before a category limit is exceeded.",
            "Flexible Custom Limits: Tap '+ Set New Budget' anytime to adjust limits as your lifestyle changes."
        ],
        "tip": "Acts like a financial guardian, preventing impulse overspending before it happens."
    }
]

def build_ui_slide_xml_and_rels(sld_data, snum, total_slides, student):
    shapes, sid = build_header_footer(2, snum, total_slides, sld_data["tag"], sld_data["title"], student)
    accent = sld_data["accent"]

    # ── Left Column: Screenshot Frame & Image ──────────────────────────────────
    fw, fh = 6350000, 5050000
    fx, fy = 550000, 1160000
    # Outer frame
    shapes.append(rect_shape(sid, fx, fy, fw, fh, "F8FAFC", "CBD5E1", line_w=18000, rounded=True)); sid += 1
    # Top badge above screenshot
    shapes.append(rect_shape(sid, fx + 160000, fy + 120000, 2400000, 320000, sld_data["tip_bg"], sld_data["tip_border"], line_w=12000, rounded=True)); sid += 1
    shapes.append(text_box(sid, fx + 200000, fy + 140000, 2320000, 280000,
                           para("📸 LIVE APPLICATION VIEW", 800, bold=True, color=accent), anchor="ctr")); sid += 1

    # Picture sizing
    aspect = sld_data.get("aspect", 1.66)
    pw = fw - 320000
    ph = int(pw / aspect)
    if ph > fh - 620000:
        ph = fh - 620000
        pw = int(ph * aspect)
    px = fx + (fw - pw) // 2
    py = fy + 500000 + (fh - 500000 - ph) // 2
    shapes.append(pic_shape(sid, "rIdScreenshot", px, py, pw, ph, sld_data["id"])); sid += 1

    # ── Right Column: Beginner's Explanatory Card ──────────────────────────────
    cw, ch = 4600000, 5050000
    cx, cy = 7040000, 1160000
    shapes.append(rect_shape(sid, cx, cy, cw, ch, "FFFFFF", "CBD5E1", line_w=18000, rounded=True)); sid += 1
    # Accent top stripe
    shapes.append(rect_shape(sid, cx + 20000, cy + 20000, cw - 40000, 60000, accent, rounded=False)); sid += 1

    # Card Title
    shapes.append(text_box(sid, cx + 180000, cy + 120000, cw - 360000, 380000,
                           para("💡 What You See Here (Beginner Guide)", 1250, bold=True, color=accent), anchor="ctr")); sid += 1

    # Overview text
    shapes.append(text_box(sid, cx + 180000, cy + 520000, cw - 360000, 650000,
                           para(sld_data["overview"], 950, color="475569"), anchor="t")); sid += 1

    # 4 Bullet points
    b_xml = "".join([
        bullet_para(b, sz=920, color="1E293B", spacing_before=65, bullet_color=accent)
        for b in sld_data["bullets"]
    ])
    shapes.append(text_box(sid, cx + 180000, cy + 1220000, cw - 360000, 2750000, b_xml, anchor="t")); sid += 1

    # Pro-tip pill at bottom
    tpy = cy + ch - 960000
    tpw = cw - 360000
    tph = 820000
    shapes.append(rect_shape(sid, cx + 180000, tpy, tpw, tph, sld_data["tip_bg"], sld_data["tip_border"], line_w=14000, rounded=True)); sid += 1
    shapes.append(text_box(sid, cx + 240000, tpy + 100000, tpw - 120000, tph - 200000,
                           para("✨ Beginner Benefit:\n" + sld_data["tip"], 880, bold=False, color=sld_data["tip_text_color"]), anchor="ctr")); sid += 1

    slide_xml = wrap_slide("\n".join(shapes))
    slide_rels = f'''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rIdLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/>
  <Relationship Id="rIdScreenshot" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{sld_data["img_filename"]}"/>
</Relationships>'''

    return slide_xml, slide_rels
