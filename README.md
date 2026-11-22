# gitignore-generator

Print or write a `.gitignore` for one or more stacks. Stdlib-only Python, no dependencies.

## Usage

```bash
# Print a .gitignore for Python to stdout
python gitignore_generator.py python

# Combine stacks (Python + Node + macOS)
python gitignore_generator.py python node macos

# Write it straight to a file
python gitignore_generator.py python -o .gitignore

# Add Node rules to an existing .gitignore without duplicating lines
python gitignore_generator.py node --append -o .gitignore

# See every available template
python gitignore_generator.py --list
```

## Templates

| Template | Covers |
| --- | --- |
| `python` | `__pycache__`, virtualenvs, build/dist, pytest, coverage |
| `node` | `node_modules`, lockfiles, build output, `.env` files |
| `go` | Binaries, test output, `vendor/` |
| `rust` | `target/`, backup files |
| `java` | `.class` files, jars, `target/`, Gradle |
| `django` | SQLite db, media, staticfiles |
| `react` | Build output, env files, logs |
| `vscode` | Editor settings (keeps the shared ones) |
| `macos` | `.DS_Store` and friends |
| `windows` | `Thumbs.db`, `Desktop.ini`, installers |
| `linux` | Backup files, trash, `.nfs` files |

## Example output

```bash
$ python gitignore_generator.py python node | head -8
# ---- python ----
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
```

Exit codes: `0` on success, `2` on a usage error (unknown template, missing stack, `--append` without `-o`).

## License

MIT — do whatever you like with it.
