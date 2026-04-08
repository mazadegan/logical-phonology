"""Generate the API reference docs and landing page."""

import shutil
import subprocess
import tempfile
from pathlib import Path

if shutil.which("pydoc-markdown") is None:
    raise SystemExit(
        "pydoc-markdown not found. Install it with: pip install pydoc-markdown"
    )

src = Path("src/logical_phonology")
docs = Path("docs")

skip = {"__init__", "__pycache__"}
modules = sorted(f.stem for f in src.glob("*.py") if f.stem not in skip)

with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    for module in modules:
        qualified = f"logical_phonology.{module}"
        output = tmp_path / f"{module}.md"
        print(f"Generating {output.name}...")
        subprocess.run(
            ["pydoc-markdown", "-I", "src", "-m", qualified, "--render-toc"],
            stdout=output.open("w"),
            check=True,
        )
    links = "\n".join(f"- [{m}]({m}.md)" for m in modules)
    content = f"# API Reference\n\n{links}\n"
    (tmp_path / "api_reference.md").write_text(content)

    # Only replace docs/ if everything succeeded
    if docs.exists():
        shutil.rmtree(docs)
    shutil.copytree(tmp_path, docs)

print("Generated docs/api_reference.md")
