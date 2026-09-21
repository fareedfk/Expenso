import os
import shutil
import zipfile
from scripts.college_data import STUDENT, SLIDES_CONTENT
from scripts.college_xml_helpers import W, H
from scripts.build_college_slide1 import create_slide_1_xml
import scripts.build_college_content_slides as bcs
from scripts.build_college_ui_slides import UI_SLIDES, build_ui_slide_xml_and_rels

def build_presentation(output_path):
    logo_path = os.path.join(os.path.dirname(__file__), "aietm_logo.png")
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"College logo not found at {logo_path}")

    with open(logo_path, "rb") as f:
        logo_bytes = f.read()

    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    screenshot_bytes = {}
    for usld in UI_SLIDES:
        fname = usld["img_filename"]
        fpath = os.path.join(screenshots_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "rb") as sf:
                screenshot_bytes[fname] = sf.read()

    slides_xml = []
    slides_rels = []

    # Slide 1 (Cover)
    slides_xml.append(create_slide_1_xml(STUDENT))
    slides_rels.append('''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rIdLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/>
</Relationships>''')

    standard_rels = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rIdLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/>
</Relationships>'''

    first_batch = [
        bcs.build_slide_2,
        bcs.build_slide_3,
        bcs.build_slide_4,
        bcs.build_slide_5,
        bcs.build_slide_6,
        bcs.build_slide_7,
        bcs.build_slide_8,
    ]
    second_batch = [
        bcs.build_slide_9,
        bcs.build_slide_10,
        bcs.build_slide_11,
        bcs.build_slide_12,
    ]

    total_slides = 1 + len(first_batch) + len(UI_SLIDES) + len(second_batch)

    # 1. Slides 2 to 8 (Architecture & Core Design)
    for idx, builder in enumerate(first_batch):
        snum = len(slides_xml) + 1
        sld = SLIDES_CONTENT[idx]
        slides_xml.append(builder(sld, snum, total_slides, STUDENT))
        slides_rels.append(standard_rels)

    # 2. Slides 9 to 12 (UI Screenshots with beginner guides)
    for usld in UI_SLIDES:
        snum = len(slides_xml) + 1
        s_xml, s_rels = build_ui_slide_xml_and_rels(usld, snum, total_slides, STUDENT)
        slides_xml.append(s_xml)
        slides_rels.append(s_rels)

    # 3. Slides 13 to 16 (Implementation, Testing, Conclusion, Closing)
    for idx, builder in enumerate(second_batch):
        snum = len(slides_xml) + 1
        sld = SLIDES_CONTENT[len(first_batch) + idx]
        slides_xml.append(builder(sld, snum, total_slides, STUDENT))
        slides_rels.append(standard_rels)

    n = len(slides_xml)
    print(f"Assembling {n} professional slides (including 4 visual UI walkthroughs)...")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        # [Content_Types].xml
        overrides = "".join([
            f'<Override PartName="/ppt/slides/slide{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            for i in range(n)
        ])
        z.writestr("[Content_Types].xml", f'''<?xml version="1.0" encoding="UTF-8"?>
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

        # _rels/.rels
        z.writestr("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>''')

        # ppt/presentation.xml
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

        # ppt/_rels/presentation.xml.rels
        pres_rels = [
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
        ]
        for i in range(n):
            pres_rels.append(f'<Relationship Id="rId{i+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i+1}.xml"/>')
        z.writestr("ppt/_rels/presentation.xml.rels", f'''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {"".join(pres_rels)}
</Relationships>''')

        # Master & Layout
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

        # Theme
        z.writestr("ppt/theme/theme1.xml", '''<?xml version="1.0" encoding="UTF-8"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="CollegeTheme">
  <a:themeElements>
    <a:clrScheme name="College">
      <a:dk1><a:srgbClr val="1E3A8A"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="0F172A"/></a:dk2><a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>
      <a:accent1><a:srgbClr val="D97706"/></a:accent1><a:accent2><a:srgbClr val="16A34A"/></a:accent2>
      <a:accent3><a:srgbClr val="2563EB"/></a:accent3><a:accent4><a:srgbClr val="7C3AED"/></a:accent4>
      <a:accent5><a:srgbClr val="DC2626"/></a:accent5><a:accent6><a:srgbClr val="0D9488"/></a:accent6>
      <a:hlink><a:srgbClr val="1E3A8A"/></a:hlink><a:folHlink><a:srgbClr val="16A34A"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="CollegeFonts">
      <a:majorFont><a:latin typeface="Segoe UI"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="Segoe UI"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="CollegeFormat"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme>
  </a:themeElements>
</a:theme>''')

        # Add image media (Logo + 4 Screenshots)
        z.writestr("ppt/media/image1.png", logo_bytes)
        for fname, sbytes in screenshot_bytes.items():
            z.writestr(f"ppt/media/{fname}", sbytes)

        # Add all slides & rels
        for i, (sxml, srels) in enumerate(zip(slides_xml, slides_rels)):
            z.writestr(f"ppt/slides/slide{i+1}.xml", sxml)
            z.writestr(f"ppt/slides/_rels/slide{i+1}.xml.rels", srels)

    print(f"Presentation successfully generated at: {output_path}")

if __name__ == "__main__":
    out_file = r"c:\Users\samee\Downloads\expenso\Expenso_Fareed_Khilji.pptx"
    build_presentation(out_file)
    web_copy = r"c:\Users\samee\Downloads\expenso\apps\web\public\Expenso_Fareed_Khilji.pptx"
    shutil.copy2(out_file, web_copy)
    print(f"Copied to web public: {web_copy}")

