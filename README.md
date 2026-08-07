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

初始化完成后，用户只需要在 R0 总控对话提出需求和审批。R0 会自动规划、
编制任务卡并把获批任务分发给 R1–R3，无需分别管理三个执行对话。

## 仓库结构

```text
coding-rules/
├── README.md
├── LICENSE
└── coding-rules/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/operating-model.md
    └── assets/project-governance/
```

## English

`coding-rules` is a reusable Codex skill for project governance. It bootstraps
approval boundaries, task cards, R0–R3 ownership, multi-conversation routing,
first-run creation or reuse of the R1–R3 execution threads, context recovery,
module-level acceptance, approval-aware next steps, evidence rules, an R0-owned
development-progress artifact, and durable handoffs. It
contains generic governance templates only and does not include product code
or project secrets.

## License

MIT License. See [LICENSE](LICENSE).
