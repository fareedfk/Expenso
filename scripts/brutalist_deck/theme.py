# Neo-Brutalist Theme Constants & PPTX Helper Functions
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Colors
C_BG = RGBColor(248, 250, 252)        # Slate 50
C_CARD_BG = RGBColor(255, 255, 255)   # Pure White
C_BORDER = RGBColor(15, 23, 42)       # Slate 900
C_TEXT_DARK = RGBColor(15, 23, 42)    # Slate 900
C_TEXT_MUTED = RGBColor(71, 85, 105)  # Slate 600
C_WHITE = RGBColor(255, 255, 255)

# Accent Colors
C_YELLOW = RGBColor(251, 191, 36)     # Amber 400
C_YELLOW_BG = RGBColor(254, 243, 199) # Amber 100
C_GREEN = RGBColor(16, 185, 129)      # Emerald 500
C_GREEN_BG = RGBColor(209, 250, 229)  # Emerald 100
C_INDIGO = RGBColor(79, 70, 229)      # Indigo 600
C_INDIGO_BG = RGBColor(224, 231, 255) # Indigo 100
C_RED = RGBColor(239, 68, 68)         # Rose 500
C_RED_BG = RGBColor(254, 226, 226)    # Rose 100
C_CYAN = RGBColor(6, 182, 212)        # Cyan 500
C_CYAN_BG = RGBColor(207, 250, 254)   # Cyan 100

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"

def apply_slide_background(slide):
    """Sets a clean canvas background with subtle top accent bar."""
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = C_BG
    bg_shape.line.color.rgb = C_BG

    # Top Neo-Brutalist Accent Line
    top_line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(0.08)
    )
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = C_BORDER
    top_line.line.color.rgb = C_BORDER

def add_badge(slide, left, top, width, height, text, bg_color=C_BORDER, text_color=C_WHITE, font_size=10):
    """Adds a punchy pill/rectangle tag with thick border."""
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.color.rgb = C_BORDER
    badge.line.width = Pt(1.5)
    tf = badge.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_HEADING
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = text_color
    return badge

def create_header(slide, tag_text, title_text, subtitle_text, slide_num, total_slides=12):
    """Creates a consistent, sharp Neo-Brutalist header for content slides."""
    apply_slide_background(slide)
    
    # Pill Tag
    add_badge(slide, Inches(0.8), Inches(0.35), Inches(2.2), Inches(0.35), tag_text, C_BORDER, C_WHITE, 10)
    
    # Slide Number Badge (Top Right)
    num_text = f"{slide_num:02d} / {total_slides:02d}"
    add_badge(slide, Inches(11.5), Inches(0.35), Inches(1.0), Inches(0.35), num_text, C_YELLOW, C_BORDER, 11)

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = FONT_HEADING
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_BORDER

    # Subtitle
    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(3)

    # Clean border divider
    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(0.025))
    divider.fill.solid()
    divider.fill.fore_color.rgb = C_BORDER
    divider.line.color.rgb = C_BORDER

def add_neo_card(slide, left, top, width, height, title, items, tag=None, accent_color=C_INDIGO, bg_color=C_CARD_BG, icon="⚡"):
    """Adds a high-contrast brutalist card with solid borders and bullet items."""
    # Hard Shadow offset shape behind
    shadow = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.06), top + Inches(0.06), width, height)
    shadow.fill.solid()
    shadow.fill.fore_color.rgb = C_BORDER
    shadow.line.color.rgb = C_BORDER

    # Main Card Box
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = C_BORDER
    card.line.width = Pt(2.0)

    # Card Top Accent Strip
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.1))
    strip.fill.solid()
    strip.fill.fore_color.rgb = accent_color
    strip.line.color.rgb = C_BORDER
    strip.line.width = Pt(1.0)

    # Text Box
    tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Card Title
    p_title = tf.paragraphs[0]
    p_title.text = f"{icon}  {title}" if icon else title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(15)
    p_title.font.bold = True
    p_title.font.color.rgb = C_BORDER

    if tag:
        p_tag = tf.add_paragraph()
        p_tag.text = tag.upper()
        p_tag.font.name = FONT_MONO
        p_tag.font.size = Pt(9)
        p_tag.font.bold = True
        p_tag.font.color.rgb = accent_color
        p_tag.space_before = Pt(2)

    # Bullet Items
    for it in items:
        p = tf.add_paragraph()
        p.text = f"•  {it}"
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_DARK
        p.space_before = Pt(6)

    return card

def add_footer_brand(slide):
    """Subtle bottom branding bar."""
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.7), Inches(0.3))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "Expenso — Personal Finance Platform  |  Fareed Khilji (23EA0CA030)  |  AIETM, Jaipur"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_TEXT_MUTED
