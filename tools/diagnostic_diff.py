#!/usr/bin/env python3
"""
Diagnostic Metadata Diff Tool

Compares two diagnostic metadata JSON files and prints a human-readable diff.
Useful for reviewers to quickly understand what changed between build submissions.

Usage:
    python3 tools/diagnostic_diff.py <file1.json> <file2.json>
    python3 tools/diagnostic_diff.py <file1.json> <file2.json> --json
    python3 tools/diagnostic_diff.py --help
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple


def load_json(path: str) -> dict:
    """Load and parse a JSON file, exiting with code 1 on failure."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)


def _get_module_key(module: dict) -> str:
    """Extract a unique key for a module entry."""
    return module.get("name", module.get("module", module.get("id", str(module))))


def _status_changed(old_status: str, new_status: str) -> bool:
    """Check if a status has meaningfully changed."""
    return old_status.strip().lower() != new_status.strip().lower()


def compare_metadata(old: dict, new: dict) -> dict:
    """
    Compare two diagnostic metadata dicts and produce a structured diff.

    Returns a dict with keys:
      - added_modules: modules present in new but not old
      - removed_modules: modules present in old but not new
      - changed_modules: modules with status/duration/command changes
      - artifact_diff: changes in artifact names
      - summary: human-readable summary strings
    """
    result: Dict[str, Any] = {
        "added_modules": [],
        "removed_modules": [],
        "changed_modules": [],
        "metadata_changes": {},
        "artifact_diff": {"added": [], "removed": [], "changed": []},
    }

    # ----- Module-level comparison -----
    old_modules = {_get_module_key(m): m for m in old.get("modules", [])}
    new_modules = {_get_module_key(m): m for m in new.get("modules", [])}

    old_keys = set(old_modules.keys())
    new_keys = set(new_modules.keys())

    # Added modules
    for key in sorted(new_keys - old_keys):
        result["added_modules"].append(new_modules[key])

    # Removed modules
    for key in sorted(old_keys - new_keys):
        result["removed_modules"].append(old_modules[key])

    # Changed modules
    for key in sorted(old_keys & new_keys):
        om = old_modules[key]
        nm = new_modules[key]
        changes = {}

        # Status change
        os_ = om.get("status", "unknown")
        ns_ = nm.get("status", "unknown")
        if _status_changed(os_, ns_):
            changes["status"] = {"old": os_, "new": ns_}

        # Duration change
        od = om.get("duration", om.get("duration_ms", None))
        nd = nm.get("duration", nm.get("duration_ms", None))
        if od is not None and nd is not None and od != nd:
            delta = nd - od if isinstance(od, (int, float)) and isinstance(nd, (int, float)) else None
            changes["duration"] = {"old": od, "new": nd, "delta": delta}

        # Command change
        oc = om.get("command", "")
        nc = nm.get("command", "")
        if oc != nc:
            changes["command"] = {"old": oc, "new": nc}

        # Artifact name change
        oa = om.get("artifact", "")
        na = nm.get("artifact", "")
        if oa != na:
            if (not oa) and na:
                result["artifact_diff"]["added"].append(na)
            elif oa and (not na):
                result["artifact_diff"]["removed"].append(oa)
            else:
                result["artifact_diff"]["changed"].append({"old": oa, "new": na})

        if changes:
            changes["module"] = key
            result["changed_modules"].append(changes)

    # ----- Top-level metadata changes -----
    for key in ("version", "timestamp", "build_id", "commit", "branch", "platform"):
        ov = old.get(key)
        nv = new.get(key)
        if ov != nv:
            result["metadata_changes"][key] = {"old": ov, "new": nv}

    return result


def format_diff_human(diff: dict) -> str:
    """Format a diff dict as a human-readable string."""
    lines = []
    sep = "-" * 60

    # Summary header
    lines.append("Diagnostic Metadata Diff")
    lines.append(sep)

    # Metadata changes
    if diff["metadata_changes"]:
        lines.append("\nMetadata Changes:")
        for key, val in diff["metadata_changes"].items():
            lines.append(f"  {key}: {val['old']} -> {val['new']}")
    else:
        lines.append("\nMetadata: unchanged")

    # Added modules
    if diff["added_modules"]:
        lines.append(f"\nAdded Modules ({len(diff['added_modules'])}):")
        for m in diff["added_modules"]:
            name = _get_module_key(m)
            status = m.get("status", "?")
            lines.append(f"  [+] {name} ({status})")

    # Removed modules
    if diff["removed_modules"]:
        lines.append(f"\nRemoved Modules ({len(diff['removed_modules'])}):")
        for m in diff["removed_modules"]:
            name = _get_module_key(m)
            status = m.get("status", "?")
            lines.append(f"  [-] {name} ({status})")

    # Changed modules
    if diff["changed_modules"]:
        lines.append(f"\nChanged Modules ({len(diff['changed_modules'])}):")
        for change in diff["changed_modules"]:
            lines.append(f"  [~] {change['module']}:")
            if "status" in change:
                s = change["status"]
                lines.append(f"       status: {s['old']} -> {s['new']}")
            if "duration" in change:
                d = change["duration"]
                delta_str = f" (delta: {d['delta']:+.2f}s)" if d.get("delta") is not None else ""
                lines.append(f"       duration: {d['old']} -> {d['new']}{delta_str}")
            if "command" in change:
                c = change["command"]
                lines.append(f"       command: {c['old']} -> {c['new']}")

    # Artifact changes
    ad = diff["artifact_diff"]
    if ad["added"] or ad["removed"] or ad["changed"]:
        lines.append("\nArtifact Changes:")
        for a in ad["added"]:
            lines.append(f"  [+] {a}")
        for a in ad["removed"]:
            lines.append(f"  [-] {a}")
        for c in ad["changed"]:
            lines.append(f"  [~] {c['old']} -> {c['new']}")

    # Overall summary
    total_changes = len(diff["added_modules"]) + len(diff["removed_modules"]) + len(diff["changed_modules"])
    lines.append(f"\n{sep}")
    lines.append(f"Summary: {total_changes} changes "
                 f"({len(diff['added_modules'])} added, "
                 f"{len(diff['removed_modules'])} removed, "
                 f"{len(diff['changed_modules'])} modified)")

    return "\n".join(lines)


def format_diff_json(diff: dict) -> str:
    """Format a diff dict as JSON."""
    return json.dumps(diff, indent=2, default=str)


def main():
    parser = argparse.ArgumentParser(
        description="Compare two diagnostic metadata JSON files and print a diff."
    )
    parser.add_argument("file1", help="Path to the first (old) diagnostic metadata JSON")
    parser.add_argument("file2", help="Path to the second (new) diagnostic metadata JSON")
    parser.add_argument("--json", action="store_true",
                        help="Output diff in JSON format (machine-readable)")
    args = parser.parse_args()

    old = load_json(args.file1)
    new = load_json(args.file2)

    diff = compare_metadata(old, new)

    if args.json:
        print(format_diff_json(diff))
    else:
        print(format_diff_human(diff))


if __name__ == "__main__":
    main()
