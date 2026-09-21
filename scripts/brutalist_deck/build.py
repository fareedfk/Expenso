# Master Builder for Neo-Brutalist Presentation
import os
import shutil
import pptx
from pptx.util import Inches
from scripts.brutalist_deck.theme import SLIDE_WIDTH, SLIDE_HEIGHT
from scripts.brutalist_deck.slides_part1 import (
    make_slide_1, make_slide_2, make_slide_3, make_slide_4, make_slide_5, make_slide_6
)
from scripts.brutalist_deck.slides_part2 import (
    make_slide_7, make_slide_8, make_slide_9, make_slide_10, make_slide_11, make_slide_12
)

def build_all_slides():
    prs = pptx.Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    print("Building Slide 1: Cover / Title...")
    make_slide_1(prs)
    print("Building Slide 2: Overview & Concept...")
    make_slide_2(prs)
    print("Building Slide 3: Problem Statement...")
    make_slide_3(prs)
    print("Building Slide 4: Proposed Solution...")
    make_slide_4(prs)
    print("Building Slide 5: System Architecture...")
    make_slide_5(prs)
    print("Building Slide 6: Database Design & Schema...")
    make_slide_6(prs)
    print("Building Slide 7: Security & Authentication...")
    make_slide_7(prs)
    print("Building Slide 8: Functional Modules & UX...")
    make_slide_8(prs)
    print("Building Slide 9: Tech Stack & Rationale...")
    make_slide_9(prs)
    print("Building Slide 10: Engineering Standards & Clean Code...")
    make_slide_10(prs)
    print("Building Slide 11: Future Roadmap...")
    make_slide_11(prs)
    print("Building Slide 12: Conclusion & Viva...")
    make_slide_12(prs)

    # Destination paths
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_root = os.path.join(workspace_root, "Expenso_Fareed_Khilji.pptx")
    out_web = os.path.join(workspace_root, "apps", "web", "public", "Expenso_Fareed_Khilji.pptx")
    out_downloads = os.path.join(os.path.expanduser("~"), "Downloads", "Expenso_Fareed_Khilji.pptx")

    print(f"Saving to {out_root}...")
    prs.save(out_root)

    print(f"Copying to {out_web}...")
    os.makedirs(os.path.dirname(out_web), exist_ok=True)
    shutil.copy2(out_root, out_web)

    if os.path.exists(os.path.dirname(out_downloads)):
        print(f"Copying to {out_downloads}...")
        try:
            shutil.copy2(out_root, out_downloads)
        except Exception as e:
            print(f"Notice: could not copy to user downloads: {e}")

    print("SUCCESS: 12 Neo-Brutalist Presentation Slides built successfully!")

if __name__ == "__main__":
    build_all_slides()
