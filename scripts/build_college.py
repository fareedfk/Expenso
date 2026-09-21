import os
import zipfile
from scripts.college_slides import STUDENT, COLLEGE_SLIDES

def build_college_pptx(output_path):
    """Build a clean, simple college-style PPTX presentation."""
    W = 12192000   # 13.33 inches in EMU
    H = 6858000    # 7.5 inches in EMU

    # ── Color helpers ─────────────────────────────────────────────────────────
    def fill(hex_val):
        return f'<a:solidFill><a:srgbClr val="{hex_val}"/></a:solidFill>'

    def no_fill():
        return '<a:noFill/>'

    def esc(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # ── Text shape builder ────────────────────────────────────────────────────
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
    <a:bodyPr {wrap_attr} lIns="91440" tIns="45720" rIns="91440" bIns="45720" anchor="{anchor}"/>
    <a:lstStyle/>
    {paragraphs_xml}
  </p:txBody>
</p:sp>'''

    def para(text, sz, bold=False, color="1E293B", align="l", spacing_before=0):
        b_attr = ' b="1"' if bold else ''
        spc = f'<a:spcBef><a:spcPts val="{spacing_before}"/></a:spcBef>' if spacing_before else ''
        return f'''<a:p>
  <a:pPr algn="{align}">{spc}</a:pPr>
  <a:r><a:rPr lang="en-IN" sz="{sz}"{b_attr} dirty="0">{fill(color)}</a:rPr>
  <a:t>{esc(text)}</a:t></a:r>
</a:p>'''

    def rect_shape(shape_id, x, y, cx, cy, fill_hex, line_hex=None, line_w=12700):
        ln_xml = f'<a:ln w="{line_w}">{fill(line_hex)}</a:ln>' if line_hex else '<a:ln><a:noFill/></a:ln>'
        return f'''<p:sp>
  <p:nvSpPr><p:cNvPr id="{shape_id}" name="R_{shape_id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    {fill(fill_hex)}{ln_xml}
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>
</p:sp>'''

    # ── Slide wrapper ──────────────────────────────────────────────────────────
    def wrap_slide(shapes_xml, has_transition=True):
        trans = '''<p:transition spd="med" advClick="1"><p:fade/></p:transition>''' if has_transition else ''
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
  {trans}
</p:sld>'''

    slide_xmls = []

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDE 1 — TITLE / COVER SLIDE (White, college-style)
    # ═══════════════════════════════════════════════════════════════════════════
    s = []
    sid = 2

    # White background
    s.append(rect_shape(sid, 0, 0, W, H, "FFFFFF")); sid += 1

    # Top navy stripe
    s.append(rect_shape(sid, 0, 0, W, 120000, "1E3A5F")); sid += 1
    # Bottom navy stripe
    s.append(rect_shape(sid, 0, H - 120000, W, 120000, "1E3A5F")); sid += 1

    # College logo circle (navy ring + gold inner circle + white "AIETM" text)
    logo_cx, logo_cy, logo_x, logo_y = 640000, 640000, (W - 640000) // 2, 180000
    s.append(f'''<p:sp>
  <p:nvSpPr><p:cNvPr id="{sid}" name="LogoRing"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{logo_x}" y="{logo_y}"/><a:ext cx="{logo_cx}" cy="{logo_cy}"/></a:xfrm>
    <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
    {fill("1E3A5F")}<a:ln w="30000">{fill("FFD700")}</a:ln>
  </p:spPr>
  <p:txBody><a:bodyPr anchor="ctr"/>
    <a:lstStyle/>
    <a:p><a:pPr algn="ctr"/>
      <a:r><a:rPr lang="en-IN" sz="1000" b="1" dirty="0">{fill("FFFFFF")}</a:rPr>
        <a:t>AIETM</a:t></a:r></a:p>
    <a:p><a:pPr algn="ctr"/>
      <a:r><a:rPr lang="en-IN" sz="700" dirty="0">{fill("FFD700")}</a:rPr>
        <a:t>JAIPUR</a:t></a:r></a:p>
  </p:txBody>
</p:sp>''')
    sid += 1

    # Main title
    title_y = logo_y + logo_cy + 120000
    s.append(text_box(sid, 600000, title_y, W - 1200000, 650000, f'''
      {para("Industrial Training / Major Project", 1600, bold=False, color="555555", align="ctr")}
      {para(STUDENT["project"], 2800, bold=True, color="1E3A5F", align="ctr")}
    ''', anchor="ctr"))
    sid += 1

    # Course & college info
    info_y = title_y + 750000
    s.append(text_box(sid, 600000, info_y, W - 1200000, 650000, f'''
      {para(STUDENT["course"], 1400, bold=False, color="333333", align="ctr")}
      {para(STUDENT["college"], 1300, bold=False, color="444444", align="ctr")}
      {para(STUDENT["year"], 1300, bold=False, color="444444", align="ctr")}
    ''', anchor="ctr"))
    sid += 1

    # Divider line
    s.append(rect_shape(sid, 1500000, info_y + 700000, W - 3000000, 18000, "1E3A5F")); sid += 1

    # Bottom: Submitted by (left) | Submitted to (right)
    sub_y = info_y + 780000
    s.append(text_box(sid, 600000, sub_y, 4000000, 520000, f'''
      {para("Submitted by:", 1300, bold=True, color="1E3A5F")}
      {para(STUDENT["name"], 1300, bold=False, color="222222")}
      {para(STUDENT["roll"], 1300, bold=False, color="222222")}
    ''', anchor="t"))
    sid += 1

    s.append(text_box(sid, W - 4600000, sub_y, 4000000, 520000, f'''
      {para("Submitted to:", 1300, bold=True, color="1E3A5F", align="r")}
      {para(STUDENT["submitted_to"], 1300, bold=False, color="222222", align="r")}
      {para(STUDENT["designation"], 1300, bold=False, color="222222", align="r")}
    ''', anchor="t"))
    sid += 1

    slide_xmls.append(wrap_slide("\n".join(s), has_transition=False))

    # ═══════════════════════════════════════════════════════════════════════════
    # SLIDES 2–12 — Content Slides (clean white with navy header)
    # ═══════════════════════════════════════════════════════════════════════════
    total_slides = 1 + len(COLLEGE_SLIDES)

    for slide_idx, sld in enumerate(COLLEGE_SLIDES):
        s = []
        sid = 2
        slide_num = slide_idx + 2

        # White background
        s.append(rect_shape(sid, 0, 0, W, H, "FFFFFF")); sid += 1

        # Navy header bar
        s.append(rect_shape(sid, 0, 0, W, 900000, "1E3A5F")); sid += 1

        # Gold accent line below header
        s.append(rect_shape(sid, 0, 900000, W, 24000, "FFD700")); sid += 1

        # Slide tag (small white text in header)
        s.append(text_box(sid, 400000, 120000, W - 800000, 300000,
            para(sld["tag"], 900, bold=True, color="FFD700", align="l"), anchor="ctr"))
        sid += 1

        # Slide title (white in header)
        s.append(text_box(sid, 400000, 380000, W - 2000000, 450000,
            para(sld["title"], 2200, bold=True, color="FFFFFF", align="l"), anchor="ctr"))
        sid += 1

        # Slide number (top right in header)
        s.append(text_box(sid, W - 1600000, 200000, 1200000, 500000,
            para(f"{slide_num} / {total_slides}", 1100, bold=False, color="BFD7F0", align="r"),
            anchor="ctr"))
        sid += 1

        # Content bullet points
        bullets_xml = ""
        for point in sld["points"]:
            bullets_xml += f'''<a:p>
  <a:pPr marL="342900" indent="-342900">
    <a:spcBef><a:spcPts val="280"/></a:spcBef>
    <a:buFont typeface="Arial"/>
    <a:buChar char="&#x2022;"/>
  </a:pPr>
  <a:r><a:rPr lang="en-IN" sz="1500" dirty="0">{fill("1E293B")}</a:rPr>
    <a:t>{esc(point)}</a:t></a:r>
</a:p>
<a:p><a:pPr><a:spcBef><a:spcPts val="80"/></a:spcBef></a:pPr>
  <a:endParaRPr sz="600"/></a:p>'''

        s.append(text_box(sid, 500000, 1020000, W - 1000000, H - 1200000,
            bullets_xml, anchor="t"))
        sid += 1

        # Bottom footer bar
        s.append(rect_shape(sid, 0, H - 220000, W, 220000, "F0F4F8")); sid += 1
        s.append(rect_shape(sid, 0, H - 222000, W, 6000, "1E3A5F")); sid += 1

        footer_txt = (f'{para("Expenso  |  " + STUDENT["name"] + "  |  " + STUDENT["roll"] + "  |  " + sld["footer"], 850, bold=False, color="555555", align="ctr")}')
        s.append(text_box(sid, 400000, H - 210000, W - 800000, 200000, footer_txt, anchor="ctr"))
        sid += 1

        slide_xmls.append(wrap_slide("\n".join(s)))

    # ═══════════════════════════════════════════════════════════════════════════
    # Write ZIP / PPTX
    # ═══════════════════════════════════════════════════════════════════════════
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        n = len(slide_xmls)
        overrides = "".join([
            f'<Override PartName="/ppt/slides/slide{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            for i in range(n)
        ])
        z.writestr("[Content_Types].xml", f'''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {overrides}
</Types>''')

        z.writestr("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>''')

        sld_ids = "".join([f'<p:sldId id="{256+i}" r:id="rId{i+3}"/>' for i in range(n)])
        z.writestr("ppt/presentation.xml", f'''<?xml version="1.0" encoding="UTF-8"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{sld_ids}</p:sldIdLst>
  <p:sldSz cx="{W}" cy="{H}" type="custom"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>''')

        pres_rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
                     '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>']
        for i in range(n):
            pres_rels.append(f'<Relationship Id="rId{i+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i+1}.xml"/>')
        z.writestr("ppt/_rels/presentation.xml.rels", f'''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {"".join(pres_rels)}
</Relationships>''')

        z.writestr("ppt/slideMasters/slideMaster1.xml", '''<?xml version="1.0" encoding="UTF-8"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
</p:sldMaster>''')

        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>''')

        z.writestr("ppt/slideLayouts/slideLayout1.xml", '''<?xml version="1.0" encoding="UTF-8"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>''')

        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>''')

        z.writestr("ppt/theme/theme1.xml", '''<?xml version="1.0" encoding="UTF-8"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="CollegeTheme">
  <a:themeElements>
    <a:clrScheme name="College">
      <a:dk1><a:srgbClr val="1E3A5F"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1E293B"/></a:dk2>
      <a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>
      <a:accent1><a:srgbClr val="FFD700"/></a:accent1>
      <a:accent2><a:srgbClr val="10B981"/></a:accent2>
      <a:accent3><a:srgbClr val="3B82F6"/></a:accent3>
      <a:accent4><a:srgbClr val="8B5CF6"/></a:accent4>
      <a:accent5><a:srgbClr val="EF4444"/></a:accent5>
      <a:accent6><a:srgbClr val="F59E0B"/></a:accent6>
      <a:hlink><a:srgbClr val="1E3A5F"/></a:hlink>
      <a:folHlink><a:srgbClr val="10B981"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="CollegeFonts">
      <a:majorFont><a:latin typeface="Calibri Light"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="CollegeFormat"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme>
  </a:themeElements>
</a:theme>''')

        for i, sxml in enumerate(slide_xmls):
            z.writestr(f"ppt/slides/slide{i+1}.xml", sxml)
            z.writestr(f"ppt/slides/_rels/slide{i+1}.xml.rels", '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>''')

    print(f"College PPT compiled: {output_path}  ({n} slides)")
