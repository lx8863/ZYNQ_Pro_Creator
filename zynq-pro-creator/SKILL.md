---
name: zynq-pro-creator
description: Generate the reusable Verilog/ModelSim project scaffold derived from the ADDA workspace. Use when the user asks to create, initialize, or regenerate an FPGA/Verilog project containing prj, rtl, sim, and vscode folders; name the RTL module after the target project folder; prefix the testbench with TB_; and update vscode/tasks.json to match those names.
---

# ZYNQ Pro Creator

Generate the scaffold with the bundled deterministic script. Treat the basename of the target directory as the project name.

## Workflow

1. Resolve the user's target project directory. If none is specified, use the current directory.
2. Run:

   ```powershell
   python <skill-directory>\scripts\create_project.py <target-directory>
   ```

3. If generated files already exist, do not overwrite them unless the user explicitly requests replacement. For an authorized replacement, add `--force`.
4. Verify the reported output paths and confirm that `vscode/tasks.json` contains the target folder's name and `TB_<target-folder-name>`.

## Output contract

Create this structure:

```text
<project>/
|-- prj/
|-- rtl/
|   `-- <project>.v
|-- sim/
|   `-- TB_<project>.v
`-- vscode/
    `-- tasks.json
```

Use the project folder basename exactly, including case. Require it to be a valid Verilog identifier (`[A-Za-z_][A-Za-z0-9_$]*`) so the filenames, module names, and ModelSim hierarchy agree. The testbench filename and module name must always be `TB_` plus the project name.

Keep the source layout's literal `vscode` directory name; do not silently rename it to `.vscode`. Preserve unrelated files when writing into an existing target directory.
