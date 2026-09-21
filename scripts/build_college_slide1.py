import os
import shutil
import zipfile
from scripts.college_data import STUDENT, SLIDES_CONTENT
from scripts.college_xml_helpers import (
    W, H, fill, para, bullet_para, text_box, rect_shape, pic_shape,
    make_card, build_header_footer, wrap_slide
)

def create_slide_1_xml(student):
    """Slide 1: College Title Cover Slide matching user reference photo."""
    shapes = []
    sid = 2

    # 1. White Background
    shapes.append(rect_shape(sid, 0, 0, W, H, "FFFFFF")); sid += 1

    # 2. Top and bottom elegant navy bands
    shapes.append(rect_shape(sid, 0, 0, W, 90000, "1E3A8A")); sid += 1
    shapes.append(rect_shape(sid, 0, H - 90000, W, 90000, "1E3A8A")); sid += 1

    # 3. AIETM College Crest Logo (centered at top)
    logo_w = 1750000
    logo_h = 1750000
    logo_x = (W - logo_w) // 2
    logo_y = 240000
    shapes.append(pic_shape(sid, "rIdLogo", logo_x, logo_y, logo_w, logo_h, "CollegeCrest")); sid += 1

    # 4. Main Title: "Industrial Training Presentation"
    t_y = logo_y + logo_h + 100000
    shapes.append(text_box(sid, 600000, t_y, W - 1200000, 650000,
                           para(student["presentation_type"], 2800, bold=True, color="1E293B", align="ctr"),
                           anchor="ctr")); sid += 1

    # 5. Project Subtitle: "Expenso — Personal Finance & Expense Tracker" (Italic Blue)
    sub_y = t_y + 600000
    shapes.append(text_box(sid, 600000, sub_y, W - 1200000, 520000,
                           para(student["project"], 1850, bold=True, color="2563EB", align="ctr", italic=True),
                           anchor="ctr")); sid += 1

    # 6. Branch / Course (Underlined)
    c_y = sub_y + 540000
    shapes.append(text_box(sid, 600000, c_y, W - 1200000, 420000,
                           para(student["course"], 1450, bold=False, color="334155", align="ctr", underline=True),
                           anchor="ctr")); sid += 1

    # 7. College Name
    col_y = c_y + 400000
    shapes.append(text_box(sid, 600000, col_y, W - 1200000, 420000,
                           para(student["college"], 1350, bold=False, color="475569", align="ctr"),
                           anchor="ctr")); sid += 1

    # 8. Year & Session
    yr_y = col_y + 360000
    shapes.append(text_box(sid, 600000, yr_y, W - 1200000, 380000,
                           para(student["year"], 1250, bold=False, color="64748B", align="ctr"),
                           anchor="ctr")); sid += 1

    # 9. Divider Line
    div_y = yr_y + 460000
    shapes.append(rect_shape(sid, 1800000, div_y, W - 3600000, 20000, "1E3A8A")); sid += 1

    # 10. Bottom Left: Submitted by
    bot_y = div_y + 80000
    sub_left = f'''{para("Submitted by:", 1350, bold=True, color="1E3A8A")}
{para(student["name"], 1500, bold=True, color="0F172A", spacing_before=40)}
{para("Roll No: " + student["roll"], 1300, bold=False, color="334155", spacing_before=30)}'''
    shapes.append(text_box(sid, 1600000, bot_y, 4200000, 1100000, sub_left, anchor="t")); sid += 1

    # 11. Bottom Right: Submitted to
    sub_right = f'''{para("Submitted to:", 1350, bold=True, color="1E3A8A", align="r")}
{para(student["submitted_to"], 1500, bold=True, color="0F172A", align="r", spacing_before=40)}
{para(student["designation"], 1300, bold=False, color="334155", align="r", spacing_before=30)}'''
    shapes.append(text_box(sid, W - 5800000, bot_y, 4200000, 1100000, sub_right, anchor="t")); sid += 1

    return wrap_slide("\n".join(shapes))
