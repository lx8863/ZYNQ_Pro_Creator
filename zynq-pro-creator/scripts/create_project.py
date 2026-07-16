#!/usr/bin/env python3
"""Create the reusable Verilog/ModelSim project scaffold."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


VALID_VERILOG_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")
DIRECTORIES = ("prj", "rtl", "sim", "vscode")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create prj/rtl/sim/vscode folders, an RTL module, a TB_<project> "
            "testbench, and matching ModelSim tasks.json."
        )
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Project directory to create or populate (default: current directory).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace only the generated files if they already exist.",
    )
    return parser.parse_args()


def render_template(template_path: Path, project_name: str, tb_name: str) -> str:
    text = template_path.read_text(encoding="utf-8")
    return text.replace("{{PROJECT_NAME}}", project_name).replace("{{TB_NAME}}", tb_name)


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    project_name = target.name

    if not project_name or not VALID_VERILOG_IDENTIFIER.fullmatch(project_name):
        print(
            "Error: the target folder name must be a valid Verilog identifier "
            "([A-Za-z_][A-Za-z0-9_$]*).",
            file=sys.stderr,
        )
        return 2

    tb_name = f"TB_{project_name}"
    skill_root = Path(__file__).resolve().parent.parent
    templates = skill_root / "assets" / "templates"

    outputs = {
        target / "rtl" / f"{project_name}.v": templates / "rtl.v.tmpl",
        target / "sim" / f"{tb_name}.v": templates / "tb.v.tmpl",
        target / "vscode" / "tasks.json": templates / "tasks.json.tmpl",
    }

    conflicts = [path for path in outputs if path.exists()]
    if conflicts and not args.force:
        print("Error: generated files already exist; no files were changed:", file=sys.stderr)
        for path in conflicts:
            print(f"  {path}", file=sys.stderr)
        print("Use --force only when replacement is intended.", file=sys.stderr)
        return 3

    for directory in DIRECTORIES:
        (target / directory).mkdir(parents=True, exist_ok=True)

    for output_path, template_path in outputs.items():
        output_path.write_text(
            render_template(template_path, project_name, tb_name),
            encoding="utf-8",
            newline="\n",
        )

    print(f"Created ModelSim Verilog project: {target}")
    print(f"Project module: {project_name}")
    print(f"Testbench module: {tb_name}")
    for directory in DIRECTORIES:
        print(f"  {target / directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

