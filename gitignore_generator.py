#!/usr/bin/env python3
"""gitignore-generator — print or write a .gitignore for one or more stacks.

Usage:
    python gitignore_generator.py python node
    python gitignore_generator.py --list
    python gitignore_generator.py python -o .gitignore
    python gitignore_generator.py node --append -o .gitignore

Stdlib only. Exit codes: 0 ok, 2 usage/template error.
"""

import argparse
import sys

TEMPLATES = {
    "python": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/
.venv/
venv/
env/
.env
*.log
*.pot
*.mo
""",
    "node": """# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
package-lock.json
yarn.lock
pnpm-lock.yaml
dist/
build/
.next/
.nuxt/
out/
coverage/
.nyc_output/
.env
.env.local
.env.*.local
*.log
.DS_Store
""",
    "go": """# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
/vendor/
dist/
bin/
""",
    "rust": """# Rust
/target/
**/*.rs.bk
Cargo.lock
*.pdb
""",
    "java": """# Java
*.class
*.log
*.ctxt
.mtj.tmp/
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar
hs_err_pid*
target/
.gradle/
build/
out/
""",
    "django": """# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/
""",
    "react": """# React
node_modules/
build/
.env.local
.env.development.local
.env.test.local
.env.production.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
""",
    "vscode": """# Visual Studio Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
*.code-workspace
""",
    "macos": """# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon
._*
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent
""",
    "windows": """# Windows
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db
*.stackdump
[Dd]esktop.ini
$RECYCLE.BIN/
*.cab
*.msi
*.msix
*.msm
*.msp
*.lnk
""",
    "linux": """# Linux
*~
.fuse_hidden*
.directory
.Trash-*
.nfs*
""",
}


def build(stacks):
    """Combine the requested templates into one .gitignore string."""
    unknown = [s for s in stacks if s not in TEMPLATES]
    if unknown:
        print(
            "unknown template(s): %s (run --list to see available ones)"
            % ", ".join(unknown),
            file=sys.stderr,
        )
        return None
    parts = []
    for stack in stacks:
        parts.append("# ---- %s ----\n%s" % (stack, TEMPLATES[stack].rstrip()))
    return "\n\n".join(parts) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate a .gitignore for one or more stacks."
    )
    parser.add_argument("stacks", nargs="*", help="template names, e.g. python node")
    parser.add_argument("--list", action="store_true", help="list available templates")
    parser.add_argument("-o", "--output", help="write to FILE instead of stdout")
    parser.add_argument(
        "--append",
        action="store_true",
        help="append to FILE, skipping lines already present (needs -o)",
    )
    args = parser.parse_args(argv)

    if args.list:
        print("\n".join(sorted(TEMPLATES)))
        return 0

    if args.append and not args.output:
        parser.error("--append requires -o/--output")

    if not args.stacks:
        parser.error("give at least one stack, or use --list")

    content = build([s.lower() for s in args.stacks])
    if content is None:
        return 2

    if args.output:
        if args.append:
            try:
                with open(args.output, "r", encoding="utf-8") as fh:
                    existing = set(fh.read().splitlines())
            except FileNotFoundError:
                existing = set()
            new_lines = [ln for ln in content.splitlines() if ln not in existing]
            with open(args.output, "a", encoding="utf-8") as fh:
                if new_lines:
                    fh.write("\n".join(new_lines) + "\n")
            print("appended %d new line(s) to %s" % (len(new_lines), args.output))
        else:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(content)
            print("wrote %s" % args.output)
    else:
        sys.stdout.write(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
