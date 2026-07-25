from pathlib import Path
from xml.etree import ElementTree


root = Path(__file__).resolve().parents[1] / "salesforce"
xml_files = list(root.rglob("*.xml"))
if not xml_files:
    raise SystemExit("no Salesforce metadata found")
for path in xml_files:
    ElementTree.parse(path)
print(f"validated {len(xml_files)} Salesforce metadata files")

