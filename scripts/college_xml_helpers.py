# OpenXML Helper Functions for College Presentation Deck
# Generates professional shapes, cards, text runs, and layout wrappers.

W = 12192000   # 13.33 inches in EMU (16:9 Widescreen)
H = 6858000    # 7.5 inches in EMU

def fill(hex_val):
    return f'<a:solidFill><a:srgbClr val="{hex_val}"/></a:solidFill>'

def no_fill():
    return '<a:noFill/>'

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def para(text, sz=1200, bold=False, color="1E293B", align="l", spacing_before=0, underline=False, italic=False):
    b_attr = ' b="1"' if bold else ''
    u_attr = ' u="sng"' if underline else ''
    i_attr = ' i="1"' if italic else ''
    spc = f'<a:spcBef><a:spcPts val="{spacing_before}"/></a:spcBef>' if spacing_before else ''
    return f'''<a:p>
  <a:pPr algn="{align}">{spc}</a:pPr>
  <a:r><a:rPr lang="en-IN" sz="{sz}"{b_attr}{u_attr}{i_attr} dirty="0">{fill(color)}</a:rPr>
  <a:t>{esc(text)}</a:t></a:r>
</a:p>'''

def bullet_para(text, sz=1100, color="334155", spacing_before=80, bullet_char="&#x25AA;", bullet_color="2563EB"):
    return f'''<a:p>
  <a:pPr marL="280000" indent="-280000">
    <a:spcBef><a:spcPts val="{spacing_before}"/></a:spcBef>
    <a:buFont typeface="Arial"/>
    <a:buChar char="{bullet_char}"/>
    <a:buClr><a:srgbClr val="{bullet_color}"/></a:buClr>
  </a:pPr>
  <a:r><a:rPr lang="en-IN" sz="{sz}" dirty="0">{fill(color)}</a:rPr>
  <a:t>{esc(text)}</a:t></a:r>
</a:p>'''

def text_box(shape_id, x, y, cx, cy, paragraphs_xml, anchor="t", wrap=True):
    wrap_attr = 'wrap="square"' if wrap else 'wrap="none"'
    return f'''<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="{shape_id}" name="TB_{shape_id}"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {no_fill()}<a:ln><a:noFill/></a:ln>
  </p:spPr>
  <p:txBody>
    <a:bodyPr {wrap_attr} lIns="72000" tIns="36000" rIns="72000" bIns="36000" anchor="{anchor}"/>
    <a:lstStyle/>
    {paragraphs_xml}
  </p:txBody>
</p:sp>'''

def rect_shape(shape_id, x, y, cx, cy, fill_hex, line_hex=None, line_w=12700, rounded=False):
    geom = "roundRect" if rounded else "rect"
    ln_xml = f'<a:ln w="{line_w}">{fill(line_hex)}</a:ln>' if line_hex else '<a:ln><a:noFill/></a:ln>'
    av_lst = '<a:avLst><a:gd name="adj" fmla="val 3000"/></a:avLst>' if rounded else '<a:avLst/>'
    return f'''<p:sp>
  <p:nvSpPr><p:cNvPr id="{shape_id}" name="R_{shape_id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="{geom}">{av_lst}</a:prstGeom>
    {fill(fill_hex)}{ln_xml}
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>
</p:sp>'''

def pic_shape(shape_id, rel_id, x, y, cx, cy, name="Picture"):
    return f'''<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="{shape_id}" name="{esc(name)}_{shape_id}"/>
    <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="{rel_id}"/>
    <a:stretch><a:fillRect/></a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </p:spPr>
</p:pic>'''

def make_card(start_sid, x, y, cx, cy, bg_hex, border_hex, title, title_color, bullets, icon=""):
    shapes = []
    sid = start_sid
    # 1. Base card container with rounded corners and border
    shapes.append(rect_shape(sid, x, y, cx, cy, bg_hex, border_hex, line_w=19050, rounded=True))
    sid += 1
    # 2. Top accent stripe
    shapes.append(rect_shape(sid, x + 20000, y + 20000, cx - 40000, 60000, title_color, rounded=False))
    sid += 1
    # 3. Header title
    hdr_txt = f"{icon} {title}" if icon else title
    shapes.append(text_box(sid, x + 120000, y + 120000, cx - 240000, 420000,
                           para(hdr_txt, 1300, bold=True, color=title_color), anchor="ctr"))
    sid += 1
    # 4. Bullet items
    b_xml = "".join([bullet_para(item, sz=1050, color="334155", spacing_before=70, bullet_color=title_color) for item in bullets])
    shapes.append(text_box(sid, x + 120000, y + 540000, cx - 240000, cy - 600000, b_xml, anchor="t"))
    sid += 1
    return shapes, sid

def build_header_footer(start_sid, slide_num, total_slides, tag, title, student_info):
    shapes = []
    sid = start_sid

    # 1. White slide background
    shapes.append(rect_shape(sid, 0, 0, W, H, "FFFFFF"))
    sid += 1

    # 2. Header navy banner
    shapes.append(rect_shape(sid, 0, 0, W, 950000, "1E3A8A"))
    sid += 1

    # 3. Gold accent strip below header
    shapes.append(rect_shape(sid, 0, 950000, W, 28000, "D97706"))
    sid += 1

    # 4. College Logo in Header
    shapes.append(pic_shape(sid, "rIdLogo", 280000, 110000, 730000, 730000, "HeaderLogo"))
    sid += 1

    # 5. Tag (Small gold uppercase text)
    shapes.append(text_box(sid, 1150000, 140000, W - 3200000, 260000,
                           para(tag, 850, bold=True, color="FCD34D", align="l"), anchor="ctr"))
    sid += 1

    # 6. Slide Title (White, bold, clean)
    shapes.append(text_box(sid, 1150000, 390000, W - 3200000, 480000,
                           para(title, 2000, bold=True, color="FFFFFF", align="l"), anchor="ctr"))
    sid += 1

    # 7. Slide Number badge
    shapes.append(text_box(sid, W - 1800000, 260000, 1500000, 440000,
                           para(f"{slide_num:02d} / {total_slides:02d}", 1100, bold=True, color="BFDBFE", align="r"), anchor="ctr"))
    sid += 1

    # 8. Footer divider line
    shapes.append(rect_shape(sid, 0, H - 340000, W, 8000, "E2E8F0"))
    sid += 1

    # 9. Footer content text
    footer_text = f"Expenso Project  |  {student_info['name']} ({student_info['roll']})  |  AIETM Jaipur (2025–26)"
    shapes.append(text_box(sid, 400000, H - 320000, W - 800000, 260000,
                           para(footer_text, 850, bold=False, color="64748B", align="ctr"), anchor="ctr"))
    sid += 1

    return shapes, sid

def wrap_slide(shapes_xml):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>
    <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
    <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>
      <a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    {shapes_xml}
  </p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
  <p:transition spd="med" advClick="1"><p:fade/></p:transition>
</p:sld>'''
