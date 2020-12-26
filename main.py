from pathlib import Path
from md_parser import md_parser

def main():
    md_path=Path("Sample.md")
    md_parser.parse_md_to_hatena(md_path)

if __name__ == "__main__":
    main()