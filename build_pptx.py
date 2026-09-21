import sys
from scripts.build_pptx import build_expenso_pptx

if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "Expenso_College_Presentation.pptx"
    build_expenso_pptx(output)
