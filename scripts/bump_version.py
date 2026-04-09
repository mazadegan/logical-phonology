# scripts/bump_version.py
import re
import tomllib
from pathlib import Path

with open("pyproject.toml", "rb") as f:
    current = tomllib.load(f)["project"]["version"]

major, minor, patch = map(int, current.split("."))

print(f"Current version: {current}")
print("Bump type:")
print("  1. patch")
print("  2. minor")
print("  3. major")

choice = input("Enter 1, 2, or 3: ").strip()

if choice == "1":
    patch += 1
elif choice == "2":
    minor += 1
    patch = 0
elif choice == "3":
    major += 1
    minor = 0
    patch = 0
else:
    raise SystemExit("Invalid choice.")

new_version = f"{major}.{minor}.{patch}"
print(f"Bumping {current} → {new_version}")
confirm = input("Confirm? (y/n): ").strip().lower()
if confirm != "y":
    raise SystemExit("Aborted.")

# update pyproject.toml
toml = Path("pyproject.toml").read_text()
toml = toml.replace(f'version = "{current}"', f'version = "{new_version}"')
Path("pyproject.toml").write_text(toml)

# update __init__.py
init = Path("src/logical_phonology/__init__.py").read_text()
init = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{new_version}"', init)
Path("src/logical_phonology/__init__.py").write_text(init)

print(f"Version bumped to {new_version}")
