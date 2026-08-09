# coding-rules

一个面向 Codex 编程项目的通用治理 Skill。它会为新项目或现有项目建立：

- `AGENTS.md` 执行与审批规则；
- R0–R3 角色分工和任务卡；
- 多对话任务分发规范；
- 上下文压缩、中断恢复和交接文档；
- R1–R3 定向验证、R0 轻量接收和模块末单次系统验收；
- 完成汇报、项目总进度、下一步顺序和逐项审批状态；
- R0 唯一维护开发进度制品，并在每次任务闭环后同步功能、审批和更新日志；
- 首次调用时检查已有项目或空项目，非破坏性部署规则并创建或复用 R1–R3
  长期执行对话；
- `LIGHT` 轻量问答与 `FULL` 全量问答两种需求收集模式；
- 每次只询问一个最高优先级问题，需求覆盖率达到 95% 后才提交计划审阅；
- 现有项目先扫描非秘密文件和开发文档，再给出已验证现状、缺口和非破坏性
  调整建议；
- 空项目直接进行需求发现，不臆造技术栈或业务需求；
- 计划先进入 `WAITING_REVIEW`，获得批准后才允许执行；
- 独立的需求、计划、任务、审批、验证、对话、预检和接收状态命名空间；
- 确定性治理合并规则与可直接运行的 Skill 验证器；
- 证据真实性、CodeGraph 和验收闭环规则。

本仓库只包含通用项目开发治理规则和空白模板，不包含任何具体项目源码、凭据或运行证据。

## 安装

```bash
git clone https://github.com/Wang-dachui986/coding-rules.git
mkdir -p ~/.codex/skills
cp -R coding-rules/coding-rules ~/.codex/skills/coding-rules
```

重新打开 Codex 后即可使用。

## 调用

在目标项目的 Codex 对话中输入：

```text
$coding-rules
```

Skill 会先判断项目是否已有有效文件。已有项目只安全合并规则，不删除、移动、
重命名或覆盖项目文件；空项目直接生成治理和交接模板。首次调用还会复用已有
R1–R3 对话并补建缺失角色，三个角色保持 `IDLE` 等待 R0 分发获批任务卡。
它不会因调用而自动修改产品代码、运行测试、联网、执行 Git 操作、部署或
访问服务器。

初始化完成后可以选择：

- `LIGHT`：适合小项目或边界清晰的需求，问题更少、更直接；
- `FULL`：适合大型项目，详细覆盖用户、流程、功能、数据、接口、非功能需求、
  环境、交付、风险和验收。

无论选择哪种模式，Skill 每次只问一个问题。只有加权需求覆盖率至少达到
95%、阻塞维度已经明确且不存在重大歧义时，才会生成状态为
`WAITING_REVIEW` 的计划供用户审阅。计划获批后，R0 才会编制任务卡并把获批
任务分发给 R1–R3；用户无需分别管理三个执行对话。

对于已经拥有需求基线、路线图、合同和任务卡流水线的成熟项目，可以在项目
`AGENTS.md` 中声明免除重复的初始问答，直接恢复当前任务和审批状态。新产品、
重大重构或没有获批需求基线的新模块仍应重新进入合适的问答模式。

## 合并与验证

现有项目采用确定性、非破坏性合并顺序：相同规则去重，项目中更严格的规则
保留，缺失且不冲突的治理门槛补入；路径或角色名称不同但语义一致时保留项目
现有命名；目标或权限发生冲突时停止写入并交由用户决定。

安装后可以运行内置检查：

```bash
cd ~/.codex/skills/coding-rules
uv run scripts/validate_skill.py
```

## 仓库结构

```text
coding-rules/
├── README.md
├── LICENSE
└── coding-rules/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── scripts/validate_skill.py
    ├── scripts/test_validate_skill.py
    ├── references/intake-model.md
    ├── references/operating-model.md
    └── assets/project-governance/
```

## English

`coding-rules` is a reusable Codex skill for project governance. It bootstraps
approval boundaries, task cards, R0–R3 ownership, multi-conversation routing,
first-run creation or reuse of the R1–R3 execution threads, context recovery,
module-level acceptance, approval-aware next steps, evidence rules, an R0-owned
development-progress artifact, and durable handoffs. It also provides LIGHT and
FULL requirements-intake modes, asks one question at a time, scans existing
project documentation non-destructively, and waits until weighted requirements
coverage reaches 95% before presenting a `WAITING_REVIEW` plan. It contains
generic governance templates only and does not include product code or project
secrets.

## License

MIT License. See [LICENSE](LICENSE).
