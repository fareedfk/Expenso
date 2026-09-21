"""Entry point: builds the clean college-style PPTX for Expenso project."""
from scripts.build_college import build_college_pptx
import shutil, os

if __name__ == "__main__":
    out = "Expenso_Fareed_Khilji.pptx"
    build_college_pptx(out)
    dest = os.path.join("apps", "web", "public", out)
    shutil.copy2(out, dest)
    print(f"Copied to {dest}")
