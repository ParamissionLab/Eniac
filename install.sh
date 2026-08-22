#!/usr/bin/env sh
# Install the skill from a POSIX terminal. Everything real happens in scripts/install.py;
# this only finds an interpreter and forwards the arguments, so there is one
# implementation of the install and one place to fix it.
#
#   ./install.sh                     # every runtime detected on this machine
#   ./install.sh --list
#   ./install.sh --runtime claude --backup
#   ./install.sh --project ../my-app
#   ./install.sh --dry-run
#
# With no clone, skip this file entirely and pipe the installer itself:
#   curl -fsSL https://raw.githubusercontent.com/ParamissionLab/Eniac/main/scripts/install.py | python3 -

set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
script="$here/scripts/install.py"

# Probe rather than trust `command -v`: on Windows the `python3` on PATH is often the
# Microsoft Store stub, which exists, prints an advert, and exits non-zero. A candidate
# counts only if it can report a version.
for candidate in python3 python py; do
    if command -v "$candidate" >/dev/null 2>&1 \
       && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' \
          >/dev/null 2>&1; then
        exec "$candidate" "$script" "$@"
    fi
done

echo "No Python found on PATH. Install Python 3.8+ (nothing else is needed - the skill" >&2
echo "is Markdown), or copy skills/Eniac into your runtime's skills directory by hand;" >&2
echo "INSTALL.md has the paths." >&2
exit 1
