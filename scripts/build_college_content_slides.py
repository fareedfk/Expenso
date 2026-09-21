# Builder for Slides 2 to 12 of Expenso College Presentation
from scripts.college_xml_helpers import (
    W, H, para, bullet_para, text_box, rect_shape, pic_shape,
    make_card, build_header_footer, wrap_slide
)

def build_slide_2(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    # 2 Big Cards
    card_w, card_h, y = 5250000, 3600000, 1180000
    for idx, c in enumerate(sld["cards"]):
        x = 600000 if idx == 0 else 6350000
        c_shapes, sid = make_card(sid, x, y, card_w, card_h, c["bg"], c["border"], c["title"], c["accent"], c["items"])
        shapes.extend(c_shapes)
    # Bottom 3 metric pills
    py, pw, ph = 4980000, 3350000, 1150000
    for idx, (title, subtitle) in enumerate(sld["metrics"]):
        px = 600000 + idx * (pw + 225000)
        shapes.append(rect_shape(sid, px, py, pw, ph, "EFF6FF", "93C5FD", line_w=15000, rounded=True)); sid += 1
        shapes.append(text_box(sid, px + 80000, py + 120000, pw - 160000, 420000,
                               para(title, 1250, bold=True, color="1E3A8A", align="ctr"), anchor="ctr")); sid += 1
        shapes.append(text_box(sid, px + 80000, py + 560000, pw - 160000, 450000,
                               para(subtitle, 950, color="475569", align="ctr"), anchor="ctr")); sid += 1
    return wrap_slide("\n".join(shapes))

def build_slide_3(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    col_w, col_h, y = 5250000, 5000000, 1180000
    # Left column: Industry Problems
    l = sld["left"]
    l_shapes, sid = make_card(sid, 600000, y, col_w, col_h, l["bg"], l["border"], l["title"], l["accent"], l["items"])
    shapes.extend(l_shapes)
    # Right column: Expenso Solution
    r = sld["right"]
    r_shapes, sid = make_card(sid, 6350000, y, col_w, col_h, r["bg"], r["border"], r["title"], r["accent"], r["items"])
    shapes.extend(r_shapes)
    return wrap_slide("\n".join(shapes))

def build_slide_4(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    cw, ch = 5250000, 2350000
    coords = [(600000, 1180000), (6350000, 1180000), (600000, 3800000), (6350000, 3800000)]
    for idx, (title, desc, color) in enumerate(sld["cards"]):
        x, y = coords[idx]
        shapes.append(rect_shape(sid, x, y, cw, ch, "F8FAFC", "CBD5E1", line_w=16000, rounded=True)); sid += 1
        shapes.append(rect_shape(sid, x + 20000, y + 20000, cw - 40000, 50000, color)); sid += 1
        shapes.append(text_box(sid, x + 120000, y + 120000, cw - 240000, 450000,
                               para(title, 1300, bold=True, color=color), anchor="ctr")); sid += 1
        shapes.append(text_box(sid, x + 120000, y + 620000, cw - 240000, ch - 720000,
                               para(desc, 1050, color="334155"), anchor="t")); sid += 1
    return wrap_slide("\n".join(shapes))

def build_slide_5(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    tw, th, y = 3300000, 4300000, 1180000
    x_positions = [600000, 4446000, 8292000]
    for idx, tier in enumerate(sld["tiers"]):
        tx = x_positions[idx]
        shapes.append(rect_shape(sid, tx, y, tw, th, "F8FAFC", "94A3B8", line_w=18000, rounded=True)); sid += 1
        shapes.append(rect_shape(sid, tx + 20000, y + 20000, tw - 40000, 60000, "1E3A8A")); sid += 1
        shapes.append(text_box(sid, tx + 80000, y + 120000, tw - 160000, 450000,
                               para(tier["tier"], 1200, bold=True, color="1E3A8A", align="ctr"), anchor="ctr")); sid += 1
        shapes.append(text_box(sid, tx + 80000, y + 580000, tw - 160000, 360000,
                               para(tier["sub"], 950, bold=True, color="2563EB", align="ctr"), anchor="ctr")); sid += 1
        b_xml = "".join([bullet_para(item, sz=1000, color="334155", spacing_before=70) for item in tier["details"]])
        shapes.append(text_box(sid, tx + 80000, y + 1000000, tw - 160000, th - 1100000, b_xml, anchor="t")); sid += 1
        if idx < 2:
            arr_x = tx + tw + 120000
            shapes.append(text_box(sid, arr_x, y + 1800000, 300000, 500000,
                                   para("➔", 2200, bold=True, color="D97706", align="ctr"), anchor="ctr")); sid += 1
    # Bottom Note
    shapes.append(rect_shape(sid, 600000, 5650000, W - 1200000, 550000, "EFF6FF", "BFDBFE", line_w=12000, rounded=True)); sid += 1
    shapes.append(text_box(sid, 700000, 5650000, W - 1400000, 550000,
                           para("💡 Clean Architecture: Presentation, Business Logic & Database are strictly decoupled (<500 LOC/file).", 1000, bold=True, color="1E3A8A", align="ctr"), anchor="ctr")); sid += 1
    return wrap_slide("\n".join(shapes))

def build_slide_6(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    cw, ch = 5250000, 2350000
    coords = [(600000, 1180000), (6350000, 1180000), (600000, 3800000), (6350000, 3800000)]
    for idx, d in enumerate(sld["domains"]):
        x, y = coords[idx]
        d_shapes, sid = make_card(sid, x, y, cw, ch, "FFFFFF", "CBD5E1", d["title"], "1E3A8A", d["items"])
        shapes.extend(d_shapes)
    return wrap_slide("\n".join(shapes))

def build_slide_7(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    tw, th, y = 5250000, 4800000, 1180000
    # Users table card
    shapes.append(rect_shape(sid, 600000, y, tw, th, "FFFFFF", "93C5FD", line_w=18000, rounded=True)); sid += 1
    shapes.append(rect_shape(sid, 620000, y + 20000, tw - 40000, 60000, "1E3A8A")); sid += 1
    shapes.append(text_box(sid, 720000, y + 120000, tw - 240000, 400000,
                           para("👤 Table: users (Authentication & Profile)", 1250, bold=True, color="1E3A8A"), anchor="ctr")); sid += 1
    u_lines = "".join([para(f"• {col}: {dt} — {desc}", 1000, color="334155", spacing_before=50) for col, dt, desc in sld["users_table"]])
    shapes.append(text_box(sid, 720000, y + 560000, tw - 240000, th - 650000, u_lines, anchor="t")); sid += 1

    # Transactions table card
    shapes.append(rect_shape(sid, 6350000, y, tw, th, "FFFFFF", "C4B5FD", line_w=18000, rounded=True)); sid += 1
    shapes.append(rect_shape(sid, 6370000, y + 20000, tw - 40000, 60000, "6D28D9")); sid += 1
    shapes.append(text_box(sid, 6470000, y + 120000, tw - 240000, 400000,
                           para("💳 Table: transactions (Expenses & Incomes)", 1250, bold=True, color="6D28D9"), anchor="ctr")); sid += 1
    t_lines = "".join([para(f"• {col}: {dt} — {desc}", 1000, color="334155", spacing_before=45) for col, dt, desc in sld["transactions_table"]])
    shapes.append(text_box(sid, 6470000, y + 560000, tw - 240000, th - 650000, t_lines, anchor="t")); sid += 1

    # Connection badge
    shapes.append(rect_shape(sid, 3400000, 6100000, 5400000, 360000, "FEF3C7", "F59E0B", line_w=12000, rounded=True)); sid += 1
    shapes.append(text_box(sid, 3400000, 6100000, 5400000, 360000,
                           para("🔗 Foreign Key: transactions.user_id ➔ users.id [ON DELETE CASCADE]", 950, bold=True, color="92400E", align="ctr"), anchor="ctr")); sid += 1
    return wrap_slide("\n".join(shapes))

def build_slide_8(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    cw, ch = 5250000, 2350000
    coords = [(600000, 1180000), (6350000, 1180000), (600000, 3800000), (6350000, 3800000)]
    for idx, f in enumerate(sld["features"]):
        x, y = coords[idx]
        shapes.append(rect_shape(sid, x, y, cw, ch, "F8FAFC", "CBD5E1", line_w=16000, rounded=True)); sid += 1
        shapes.append(rect_shape(sid, x + 20000, y + 20000, cw - 40000, 50000, "2563EB")); sid += 1
        shapes.append(text_box(sid, x + 120000, y + 120000, cw - 240000, 450000,
                               para(f"{f['icon']} {f['name']}", 1300, bold=True, color="1E3A8A"), anchor="ctr")); sid += 1
        shapes.append(text_box(sid, x + 120000, y + 620000, cw - 240000, ch - 720000,
                               para(f['desc'], 1050, color="334155"), anchor="t")); sid += 1
    return wrap_slide("\n".join(shapes))

def build_slide_9(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    cw, ch, y = 5250000, 5000000, 1180000
    b_shapes, sid = make_card(sid, 600000, y, cw, ch, "FFFFFF", "93C5FD", "⚙️ FastAPI Backend Architecture", "1E3A8A", sld["backend"])
    shapes.extend(b_shapes)
    f_shapes, sid = make_card(sid, 6350000, y, cw, ch, "FFFFFF", "A7F3D0", "💻 Frontend Modular Architecture", "065F46", sld["frontend"])
    shapes.extend(f_shapes)
    return wrap_slide("\n".join(shapes))

def build_slide_10(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    # Testing Table Box
    tbl_w, tbl_h, y = W - 1200000, 3600000, 1180000
    shapes.append(rect_shape(sid, 600000, y, tbl_w, tbl_h, "FFFFFF", "CBD5E1", line_w=18000, rounded=True)); sid += 1
    # Table header bar
    shapes.append(rect_shape(sid, 620000, y + 20000, tbl_w - 40000, 480000, "1E3A8A", rounded=False)); sid += 1
    shapes.append(text_box(sid, 700000, y + 100000, 3000000, 360000,
                           para("Test Module", 1150, bold=True, color="FFFFFF"), anchor="ctr")); sid += 1
    shapes.append(text_box(sid, 3700000, y + 100000, 5200000, 360000,
                           para("Validation Criteria", 1150, bold=True, color="FFFFFF"), anchor="ctr")); sid += 1
    shapes.append(text_box(sid, W - 2800000, y + 100000, 2000000, 360000,
                           para("Result", 1150, bold=True, color="FFFFFF", align="r"), anchor="ctr")); sid += 1
    # Rows
    for idx, (tname, tdesc, tstatus) in enumerate(sld["test_cases"]):
        ry = y + 540000 + idx * 580000
        bg_col = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        shapes.append(rect_shape(sid, 620000, ry, tbl_w - 40000, 540000, bg_col)); sid += 1
        shapes.append(text_box(sid, 700000, ry + 80000, 3000000, 400000,
                               para(tname, 1050, bold=True, color="1E293B"), anchor="ctr")); sid += 1
        shapes.append(text_box(sid, 3700000, ry + 80000, 5200000, 400000,
                               para(tdesc, 950, color="475569"), anchor="ctr")); sid += 1
        shapes.append(text_box(sid, W - 2800000, ry + 80000, 2000000, 400000,
                               para(tstatus, 1050, bold=True, color="16A34A", align="r"), anchor="ctr")); sid += 1

    # Bottom 3 Stats Cards
    sy, sw, sh = 4980000, 3350000, 1150000
    for idx, (stat, label) in enumerate(sld["stats"]):
        sx = 600000 + idx * (sw + 225000)
        shapes.append(rect_shape(sid, sx, sy, sw, sh, "F0FDF4", "86EFAC", line_w=15000, rounded=True)); sid += 1
        shapes.append(text_box(sid, sx + 80000, sy + 120000, sw - 160000, 420000,
                               para(stat, 1400, bold=True, color="15803D", align="ctr"), anchor="ctr")); sid += 1
        shapes.append(text_box(sid, sx + 80000, sy + 580000, sw - 160000, 450000,
                               para(label, 1000, color="475569", align="ctr"), anchor="ctr")); sid += 1
    return wrap_slide("\n".join(shapes))

def build_slide_11(sld, snum, total, student):
    shapes, sid = build_header_footer(2, snum, total, sld["tag"], sld["title"], student)
    cw, ch, y = 5250000, 5000000, 1180000
    ach_shapes, sid = make_card(sid, 600000, y, cw, ch, "FFFFFF", "93C5FD", "🏆 Key Project Accomplishments", "1E3A8A", sld["achievements"])
    shapes.extend(ach_shapes)
    rdm_shapes, sid = make_card(sid, 6350000, y, cw, ch, "FFFFFF", "FDE68A", "🚀 Future Development Roadmap", "B45309", sld["roadmap"])
    shapes.extend(rdm_shapes)
    return wrap_slide("\n".join(shapes))

def build_slide_12(sld, snum, total, student):
    shapes = []
    sid = 2
    # White background with top & bottom navy stripes
    shapes.append(rect_shape(sid, 0, 0, W, H, "FFFFFF")); sid += 1
    shapes.append(rect_shape(sid, 0, 0, W, 90000, "1E3A8A")); sid += 1
    shapes.append(rect_shape(sid, 0, H - 90000, W, 90000, "1E3A8A")); sid += 1
    # Center Card
    cw, ch = 9000000, 5200000
    cx = (W - cw) // 2
    cy = (H - ch) // 2
    shapes.append(rect_shape(sid, cx, cy, cw, ch, "F8FAFC", "CBD5E1", line_w=20000, rounded=True)); sid += 1
    # AIETM Logo in center
    lw, lh = 1500000, 1500000
    shapes.append(pic_shape(sid, "rIdLogo", (W - lw) // 2, cy + 240000, lw, lh, "LogoCenter")); sid += 1
    # Thank You text
    shapes.append(text_box(sid, cx + 400000, cy + 1850000, cw - 800000, 700000,
                           para("Thank You!", 3200, bold=True, color="1E3A8A", align="ctr"), anchor="ctr")); sid += 1
    shapes.append(text_box(sid, cx + 400000, cy + 2600000, cw - 800000, 500000,
                           para("Questions & Discussion (Q&A)", 1800, bold=True, color="D97706", align="ctr"), anchor="ctr")); sid += 1
    shapes.append(rect_shape(sid, cx + 1800000, cy + 3250000, cw - 3600000, 16000, "1E3A8A")); sid += 1
    info_xml = f'''{para("Project: " + student["project"], 1350, bold=True, color="1E293B", align="ctr")}
{para("Presented by: " + student["name"] + " (Roll No: " + student["roll"] + ")", 1300, bold=False, color="334155", align="ctr", spacing_before=30)}
{para("Guided by: " + student["submitted_to"] + " " + student["designation"], 1300, bold=False, color="334155", align="ctr", spacing_before=30)}
{para(student["college"], 1200, bold=False, color="64748B", align="ctr", spacing_before=30)}'''
    shapes.append(text_box(sid, cx + 400000, cy + 3400000, cw - 800000, 1500000, info_xml, anchor="t")); sid += 1
    return wrap_slide("\n".join(shapes))
