"""Build the Flow plugin ZIP from the tested source; no credentials required."""
import hashlib
import json
import os
from pathlib import Path
import re
import zipfile

root = Path(__file__).resolve().parents[2]
manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
version = manifest["Version"]
if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    raise SystemExit("Version must be a numeric semantic version")
files = [Path("main.py"), Path("plugin.json"), Path("SettingsTemplate.yaml"), Path("README.md")]
files += sorted(p.relative_to(root) for p in (root / "Images").rglob("*.png"))
files += sorted(p.relative_to(root) for p in (root / "tests").rglob("*.py"))
if not (root / "Images/app.png").is_file():
    raise SystemExit("Missing plugin icon")
out = root / "dist"
out.mkdir(exist_ok=True)
asset = out / ("LeoTranslate-" + version + ".zip")
with zipfile.ZipFile(asset, "w", zipfile.ZIP_DEFLATED) as archive:
    for rel in files:
        info = zipfile.ZipInfo(rel.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, (root / rel).read_bytes())
with zipfile.ZipFile(asset) as archive:
    if archive.testzip():
        raise SystemExit("Corrupted archive")
checksum = hashlib.sha256(asset.read_bytes()).hexdigest()
(out / "SHA256SUMS.txt").write_text(checksum + "  " + asset.name + "\n", encoding="ascii")
if os.environ.get("GITHUB_OUTPUT"):
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as handle:
        handle.write("version=" + version + "\n")
        handle.write("asset=dist/" + asset.name + "\n")
print(asset.name + "  " + checksum)
