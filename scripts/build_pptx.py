import os
import shutil
import zipfile
from scripts.pptx_data import SLIDES_DATA
from scripts.pptx_ui_data import DARK_UI_SLIDES

def build_expenso_pptx(output_path):
    # 16:9 Widescreen (13.33 x 7.5 inches) in EMUs
    SLIDE_WIDTH = 12192000
    SLIDE_HEIGHT = 6858000

    def color_xml(hex_val):
        return f'<a:solidFill><a:srgbClr val="{hex_val}"/></a:solidFill>'

    def esc(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def make_card_shape(shape_id, x, y, cx, cy, title, color_hex, lines, body_size=1200):
        paragraphs = [
            f'''<a:p>
              <a:pPr algn="l"/>
              <a:r>
                <a:rPr lang="en-US" sz="1600" b="1">{color_xml(color_hex)}</a:rPr>
                <a:t>{esc(title)}</a:t>
              </a:r>
            </a:p>''',
            '<a:p><a:pPr sz="500"/><a:endParaRPr sz="500"/></a:p>'
        ]

        for line in lines:
            paragraphs.append(f'''<a:p>
              <a:pPr algn="l" marL="220000" indent="-220000">
                <a:buFont typeface="Arial"/>
                <a:buChar char="₹"/>
              </a:pPr>
              <a:r>
                <a:rPr lang="en-US" sz="{body_size}">{color_xml("E2E8F0")}</a:rPr>
                <a:t>{esc(line)}</a:t>
              </a:r>
            </a:p>''')

        return f'''<p:sp>
          <p:nvSpPr>
            <p:cNvPr id="{shape_id}" name="Card_{shape_id}"/>
            <p:cNvSpPr/>
            <p:nvPr/>
          </p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
            <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 4500"/></a:avLst></a:prstGeom>
            {color_xml("141E33")}
            <a:ln w="22000">{color_xml(color_hex)}</a:ln>
          </p:spPr>
          <p:txBody>
            <a:bodyPr vert="horz" lIns="200000" tIns="200000" rIns="200000" bIns="200000" anchor="t"/>
            <a:lstStyle/>
            {''.join(paragraphs)}
          </p:txBody>
        </p:sp>'''

    all_slides = SLIDES_DATA[:8] + DARK_UI_SLIDES + SLIDES_DATA[8:]
    total_count = len(all_slides)

    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    screenshot_bytes = {}
    for usld in DARK_UI_SLIDES:
        fname = usld["screenshot"]
        fpath = os.path.join(screenshots_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "rb") as sf:
                screenshot_bytes[fname] = sf.read()

    slide_xmls = []
    slide_rels = []

    for idx, s in enumerate(all_slides):
        slide_num = idx + 1
        shapes = []
        shape_id = 2

        # 1. Slide Background
        shapes.append(f'''<p:sp>
          <p:nvSpPr><p:cNvPr id="{shape_id}" name="BG"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_WIDTH}" cy="{SLIDE_HEIGHT}"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
            {color_xml("0B1328")}
          </p:spPr>
          <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>
        </p:sp>''')
        shape_id += 1

        # 2. Golden Accent Header Stripe
        shapes.append(f'''<p:sp>
          <p:nvSpPr><p:cNvPr id="{shape_id}" name="TopBar"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="0" y="0"/><a:ext cx="{SLIDE_WIDTH}" cy="60000"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
            {color_xml("F59E0B")}
          </p:spPr>
          <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>
        </p:sp>''')
        shape_id += 1

        # 3. Slide Header Box
        shapes.append(f'''<p:sp>
          <p:nvSpPr><p:cNvPr id="{shape_id}" name="Header"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="720000" y="460000"/><a:ext cx="8800000" cy="1300000"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
            <a:noFill/><a:ln><a:noFill/></a:ln>
          </p:spPr>
          <p:txBody>
            <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"/>
            <a:lstStyle/>
            <a:p>
              <a:r>
                <a:rPr lang="en-US" sz="1050" b="1">{color_xml("F59E0B")}</a:rPr>
                <a:t>₹ {esc(s["tag"])}</a:t>
              </a:r>
            </a:p>
            <a:p>
              <a:r>
                <a:rPr lang="en-US" sz="2600" b="1">{color_xml("FFFFFF")}</a:rPr>
                <a:t>{esc(s["title"])}</a:t>
              </a:r>
            </a:p>
            <a:p>
              <a:r>
                <a:rPr lang="en-US" sz="1250">{color_xml("94A3B8")}</a:rPr>
                <a:t>{esc(s["subtitle"])}</a:t>
              </a:r>
            </a:p>
          </p:txBody>
        </p:sp>''')
        shape_id += 1

        # 4a. Golden Rupee Coin
        shapes.append(f'''<p:sp>
          <p:nvSpPr><p:cNvPr id="{shape_id}" name="RupeeCoin"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="9120000" y="520000"/><a:ext cx="420000" cy="420000"/></a:xfrm>
            <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
            {color_xml("F59E0B")}
            <a:ln w="20000">{color_xml("FEF08A")}</a:ln>
          </p:spPr>
          <p:txBody>
            <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/>
            <a:lstStyle/>
            <a:p>
              <a:pPr algn="ctr"/>
              <a:r>
                <a:rPr lang="en-US" sz="1400" b="1">{color_xml("451A03")}</a:rPr>
                <a:t>₹</a:t>
              </a:r>
            </a:p>
          </p:txBody>
        </p:sp>''')
        shape_id += 1

        # 4b. Golden Rupee Badge Pill
        badge_text = s.get("badge", "EXPENSO")
        shapes.append(f'''<p:sp>
          <p:nvSpPr><p:cNvPr id="{shape_id}" name="Badge"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="9650000" y="520000"/><a:ext cx="1820000" cy="420000"/></a:xfrm>
            <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 20000"/></a:avLst></a:prstGeom>
            {color_xml("1E293B")}
            <a:ln w="16000">{color_xml("F59E0B")}</a:ln>
          </p:spPr>
          <p:txBody>
            <a:bodyPr vert="horz" lIns="60000" tIns="60000" rIns="60000" bIns="60000" anchor="ctr"/>
            <a:lstStyle/>
            <a:p>
              <a:pPr algn="ctr"/>
              <a:r>
                <a:rPr lang="en-US" sz="950" b="1">{color_xml("F59E0B")}</a:rPr>
                <a:t>₹ {esc(badge_text)}</a:t>
              </a:r>
            </a:p>
          </p:txBody>
        </p:sp>''')
        shape_id += 1

        # 5. Content Layout (Screenshots vs Multi-Boxes)
        if s.get("type") == "screenshot":
            accent = s["accent"]
            fx, fy, fw, fh = 720000, 1950000, 5800000, 4220000
            shapes.append(f'''<p:sp>
              <p:nvSpPr><p:cNvPr id="{shape_id}" name="PicFrame_{shape_id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
              <p:spPr>
                <a:xfrm><a:off x="{fx}" y="{fy}"/><a:ext cx="{fw}" cy="{fh}"/></a:xfrm>
                <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 4500"/></a:avLst></a:prstGeom>
                {color_xml("141E33")}
                <a:ln w="22000">{color_xml(accent)}</a:ln>
              </p:spPr>
              <p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody>
            </p:sp>''')
            shape_id += 1

            aspect = s.get("aspect", 1.66)
            pw = fw - 320000
            ph = int(pw / aspect)
            if ph > fh - 320000:
                ph = fh - 320000
                pw = int(ph * aspect)
            px = fx + (fw - pw) // 2
            py = fy + (fh - ph) // 2
            shapes.append(f'''<p:pic>
              <p:nvPicPr>
                <p:cNvPr id="{shape_id}" name="Screenshot_{shape_id}"/>
                <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
                <p:nvPr/>
              </p:nvPicPr>
              <p:blipFill>
                <a:blip r:embed="rIdScreenshot"/>
                <a:stretch><a:fillRect/></a:stretch>
              </p:blipFill>
              <p:spPr>
                <a:xfrm><a:off x="{px}" y="{py}"/><a:ext cx="{pw}" cy="{ph}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </p:spPr>
            </p:pic>''')
            shape_id += 1

            cx, cy, cw, ch = 6720000, 1950000, 4752000, 4220000
            c_paras = [
                f'''<a:p>
                  <a:pPr algn="l"/>
                  <a:r>
                    <a:rPr lang="en-US" sz="1400" b="1">{color_xml(accent)}</a:rPr>
                    <a:t>💡 What You See Here (Beginner Guide)</a:t>
                  </a:r>
                </a:p>''',
                f'''<a:p>
                  <a:pPr algn="l"><a:spcBef><a:spcPts val="60"/></a:spcBef></a:pPr>
                  <a:r>
                    <a:rPr lang="en-US" sz="1000">{color_xml("94A3B8")}</a:rPr>
                    <a:t>{esc(s["overview"])}</a:t>
                  </a:r>
                </a:p>''',
                '<a:p><a:pPr sz="300"/><a:endParaRPr sz="300"/></a:p>'
            ]
            for callout in s["callouts"]:
                c_paras.append(f'''<a:p>
                  <a:pPr algn="l" marL="200000" indent="-200000">
                    <a:spcBef><a:spcPts val="50"/></a:spcBef>
                    <a:buFont typeface="Arial"/>
                    <a:buChar char="₹"/>
                    <a:buClr><a:srgbClr val="{accent}"/></a:buClr>
                  </a:pPr>
                  <a:r>
                    <a:rPr lang="en-US" sz="950">{color_xml("E2E8F0")}</a:rPr>
                    <a:t>{esc(callout)}</a:t>
                  </a:r>
                </a:p>''')

            c_paras.append(f'''<a:p>
              <a:pPr algn="l"><a:spcBef><a:spcPts val="80"/></a:spcBef></a:pPr>
              <a:r>
                <a:rPr lang="en-US" sz="900" b="1">{color_xml("F59E0B")}</a:rPr>
                <a:t>✨ Beginner Benefit: </a:t>
              </a:r>
              <a:r>
                <a:rPr lang="en-US" sz="900">{color_xml("FEF08A")}</a:rPr>
                <a:t>{esc(s["tip"])}</a:t>
              </a:r>
            </a:p>''')

            shapes.append(f'''<p:sp>
              <p:nvSpPr><p:cNvPr id="{shape_id}" name="Card_{shape_id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
              <p:spPr>
                <a:xfrm><a:off x="{cx}" y="{cy}"/><a:ext cx="{cw}" cy="{ch}"/></a:xfrm>
                <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 4500"/></a:avLst></a:prstGeom>
                {color_xml("141E33")}
                <a:ln w="22000">{color_xml(accent)}</a:ln>
              </p:spPr>
              <p:txBody>
                <a:bodyPr vert="horz" lIns="180000" tIns="180000" rIns="180000" bIns="180000" anchor="t"/>
                <a:lstStyle/>
                {''.join(c_paras)}
              </p:txBody>
            </p:sp>''')
            shape_id += 1

            slide_rels.append(f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rIdScreenshot" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{s["screenshot"]}"/>
</Relationships>''')

        else:
            boxes = s["boxes"]
            num_boxes = len(boxes)
            content_y = 1950000
            content_h = 4220000
            total_w = 10752000
            gap = 250000

            if num_boxes == 2:
                box_w = (total_w - gap) // 2
                for b_idx, b in enumerate(boxes):
                    bx = 720000 + b_idx * (box_w + gap)
                    shapes.append(make_card_shape(shape_id, bx, content_y, box_w, content_h, b["title"], b["color"], b["lines"], 1250))
                    shape_id += 1
            elif num_boxes == 3:
                box_w = (total_w - 2 * gap) // 3
                for b_idx, b in enumerate(boxes):
                    bx = 720000 + b_idx * (box_w + gap)
                    shapes.append(make_card_shape(shape_id, bx, content_y, box_w, content_h, b["title"], b["color"], b["lines"], 1150))
                    shape_id += 1

            slide_rels.append('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>''')

        # 6. Bottom Footer
        shapes.append(f'''<p:sp>
          <p:nvSpPr><p:cNvPr id="{shape_id}" name="Footer"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="720000" y="6350000"/><a:ext cx="10752000" cy="300000"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
            <a:noFill/><a:ln><a:noFill/></a:ln>
          </p:spPr>
          <p:txBody>
            <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0" anchor="b"/>
            <a:lstStyle/>
            <a:p>
              <a:r>
                <a:rPr lang="en-US" sz="950">{color_xml("64748B")}</a:rPr>
                <a:t>Expenso • Smart Indian Finance • Slide {slide_num} of {total_count} • ₹ ₹ ₹</a:t>
              </a:r>
            </a:p>
          </p:txBody>
        </p:sp>''')

        # Slide XML with Native Push Transition
        slide_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      {''.join(shapes)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
  <p:transition spd="med" advClick="1">
    <p:push dir="l"/>
  </p:transition>
</p:sld>'''
        slide_xmls.append(slide_xml)

    # Write OpenXML ZIP archive
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        overrides = "".join([
            f'<Override PartName="/ppt/slides/slide{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            for i in range(total_count)
        ])
        z.writestr("[Content_Types].xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {overrides}
</Types>''')

        z.writestr("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>''')

        sld_id_lst = "".join([f'<p:sldId id="{256 + i}" r:id="rId{i+3}"/>' for i in range(total_count)])
        z.writestr("ppt/presentation.xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{sld_id_lst}</p:sldIdLst>
  <p:sldSz cx="{SLIDE_WIDTH}" cy="{SLIDE_HEIGHT}" type="custom"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>''')

        pres_rels = [
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
        ]
        for i in range(total_count):
            pres_rels.append(f'<Relationship Id="rId{i+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i+1}.xml"/>')

        z.writestr("ppt/_rels/presentation.xml.rels", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {''.join(pres_rels)}
</Relationships>''')

        z.writestr("ppt/slideMasters/slideMaster1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/><p:sp><p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
</p:sldMaster>''')

        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>''')

        z.writestr("ppt/slideLayouts/slideLayout1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>''')

        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>''')

        z.writestr("ppt/theme/theme1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="ExpensoRupeeTheme">
  <a:themeElements>
    <a:clrScheme name="RupeeColors">
      <a:dk1><a:srgbClr val="0B1328"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="141E33"/></a:dk2>
      <a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>
      <a:accent1><a:srgbClr val="F59E0B"/></a:accent1>
      <a:accent2><a:srgbClr val="10B981"/></a:accent2>
      <a:accent3><a:srgbClr val="3B82F6"/></a:accent3>
      <a:accent4><a:srgbClr val="8B5CF6"/></a:accent4>
      <a:accent5><a:srgbClr val="EF4444"/></a:accent5>
      <a:accent6><a:srgbClr val="FBBF24"/></a:accent6>
      <a:hlink><a:srgbClr val="F59E0B"/></a:hlink>
      <a:folHlink><a:srgbClr val="10B981"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="RupeeFonts">
      <a:majorFont><a:latin typeface="Segoe UI Semibold"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="Segoe UI"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="RupeeFormat"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme>
  </a:themeElements>
</a:theme>''')

        # Add image media
        for fname, sbytes in screenshot_bytes.items():
            z.writestr(f"ppt/media/{fname}", sbytes)

        for i, (s_xml, s_rel) in enumerate(zip(slide_xmls, slide_rels)):
            s_idx = i + 1
            z.writestr(f"ppt/slides/slide{s_idx}.xml", s_xml)
            z.writestr(f"ppt/slides/_rels/slide{s_idx}.xml.rels", s_rel)

    print(f"Rupee Theme Presentation ({total_count} slides) compiled at: {output_path}")

if __name__ == "__main__":
    out_file = "Expenso_College_Presentation.pptx"
    build_expenso_pptx(out_file)
    web_copy = os.path.join("apps", "web", "public", out_file)
    shutil.copy2(out_file, web_copy)
    print(f"Copied to web public: {web_copy}")

