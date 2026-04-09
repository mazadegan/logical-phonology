# scripts/tag_release.py
import subprocess
import tomllib

with open("pyproject.toml", "rb") as f:
    version = tomllib.load(f)["project"]["version"]

tag = f"v{version}"
print(f"Tagging release {tag}...")
subprocess.run(["git", "tag", tag], check=True)
subprocess.run(["git", "push", "origin", tag], check=True)
print(f"Tagged and pushed {tag}")
