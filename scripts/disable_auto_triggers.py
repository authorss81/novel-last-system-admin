#!/usr/bin/env python3
"""Stop a finished novel from triggering itself, without losing manual control.

Removes the `schedule` and `repository_dispatch` triggers from novels.yml and
keeps `workflow_dispatch`, so a completed novel stops waking itself every ten
minutes while a deliberate manual run is still possible. Idempotent: running it
again on an already-edited file changes nothing.

Operates on the local checkout. Exits 0 whether or not it changed anything.
"""

from __future__ import annotations

import re
import sys

DROP = ("schedule", "repository_dispatch")
KEEP = "workflow_dispatch"
CHILD = re.compile(r"^(\s+)(\S[^:]*):\s*$")


def strip_triggers(text: str) -> tuple[str, list[str]]:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    removed: list[str] = []
    index = 0
    total = len(lines)

    while index < total:
        line = lines[index]
        out.append(line)
        index += 1
        if line.rstrip("\n") != "on:":
            continue

        # Walk every key under `on:`. A dropped key takes its whole subtree with
        # it; a kept key is copied along with all of its nested lines.
        while index < total:
            child = CHILD.match(lines[index].rstrip("\n"))
            if not child:
                break
            indent = len(child.group(1))
            name = child.group(2).strip()

            if name in DROP:
                removed.append(name)
                index += 1
                while index < total:
                    nxt = lines[index]
                    if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= indent:
                        break
                    index += 1
                continue

            out.append(lines[index])
            index += 1
            while index < total:
                nxt = lines[index]
                if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= indent:
                    break
                out.append(nxt)
                index += 1
    return "".join(out), removed


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else ".github/workflows/novels.yml"
    with open(path, encoding="utf-8") as handle:
        original = handle.read()

    updated, removed = strip_triggers(original)
    if not removed and KEEP in original:
        print("automatic triggers already disabled")
        return 0
    if KEEP not in updated:
        print(f"refusing to edit {path}: workflow_dispatch would be lost", file=sys.stderr)
        return 0

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(updated)
    print(f"disabled automatic triggers: {', '.join(removed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())