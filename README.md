# ZYNQ_Pro_Creator

`ZYNQ_Pro_Creator` 是一个面向 Codex 的 skill，用于按固定约定生成 Verilog/ModelSim 项目骨架。项目名称取自目标文件夹名称，并同步用于 RTL 模块名、测试平台名称和 ModelSim 运行任务。

## 主要功能

- 创建 `prj`、`rtl`、`sim` 和 `vscode` 四个目录。
- 生成与项目文件夹同名的 RTL 文件和模块。
- 生成以 `TB_` 为前缀的 testbench 文件和模块。
- 生成与项目名、testbench 名一致的 ModelSim 任务配置。
- 默认保护已有生成文件；只有明确使用 `--force` 时才替换这些文件。
- 写入已有项目时保留其他无关文件。

## 仓库结构

```text
ZYNQ_Pro_Creator/
|-- README.md
`-- zynq-pro-creator/
    |-- SKILL.md
    |-- agents/
    |   `-- openai.yaml
    |-- scripts/
    |   `-- create_project.py
    `-- assets/
        `-- templates/
            |-- rtl.v.tmpl
            |-- tb.v.tmpl
            `-- tasks.json.tmpl
```

## 各目录和文件的作用

| 路径 | 作用 |
| --- | --- |
| `README.md` | 仓库级说明文档，介绍用途、结构、安装和使用方法。 |
| `zynq-pro-creator/SKILL.md` | skill 的触发说明、执行流程、输出结构和命名约束。 |
| `zynq-pro-creator/agents/` | 存放 Codex 界面所需的 skill 元数据。 |
| `zynq-pro-creator/agents/openai.yaml` | 定义显示名称、简短说明和默认提示词。 |
| `zynq-pro-creator/scripts/` | 存放可重复执行的确定性脚本。 |
| `zynq-pro-creator/scripts/create_project.py` | 根据目标目录名创建项目目录，并用模板生成 RTL、testbench 和 ModelSim 任务文件。 |
| `zynq-pro-creator/assets/` | 存放 skill 生成输出时使用的资源。 |
| `zynq-pro-creator/assets/templates/` | 存放 Verilog 和任务配置模板。 |
| `rtl.v.tmpl` | RTL 顶层模块模板；`{{PROJECT_NAME}}` 会替换为项目名称。 |
| `tb.v.tmpl` | testbench 模板；`{{TB_NAME}}` 和 `{{PROJECT_NAME}}` 会替换为实际名称。 |
| `tasks.json.tmpl` | ModelSim/VS Code 任务模板，包含编译、仿真、波形添加和运行命令。 |

## 安装

将仓库中的 `zynq-pro-creator` 目录复制到 Codex 的 skills 目录：

```text
<CODEX_HOME>/skills/zynq-pro-creator
```

安装后目录中应直接包含 `SKILL.md`、`agents/`、`scripts/` 和 `assets/`。

## 使用

在 Codex 中可以这样请求：

```text
使用 $zynq-pro-creator，在 D:\zynq\Myproject\Demo_Project 创建项目。
```

也可以直接运行脚本：

```powershell
python <skill-directory>\scripts\create_project.py <target-directory>
```

如果目标项目中已经存在将要生成的文件，脚本会停止且不修改文件。只有确认需要替换时才使用：

```powershell
python <skill-directory>\scripts\create_project.py <target-directory> --force
```

## 生成结果

假设目标目录名为 `Demo_Project`，生成结构如下：

```text
Demo_Project/
|-- prj/
|-- rtl/
|   `-- Demo_Project.v
|-- sim/
|   `-- TB_Demo_Project.v
`-- vscode/
    `-- tasks.json
```

项目文件夹名称必须是合法的 Verilog 标识符：以字母或下划线开头，后续只能包含字母、数字、下划线或 `$`。目录名的大小写会被原样保留。

> 注意：该 skill 按原始项目约定生成名为 `vscode` 的目录，而不是 `.vscode`。

## 运行要求

- Python 3，用于运行项目生成脚本。
- ModelSim 或兼容的 `vsim` 命令，用于执行生成的仿真任务。

## 验证状态

当前版本已通过以下检查：

- skill 必需文件和 YAML frontmatter 检查。
- 使用 `Demo_Project` 作为项目名的实际生成测试。
- RTL、testbench 和任务配置中的名称一致性检查。
- 已有生成文件的默认防覆盖行为由脚本逻辑保护。
