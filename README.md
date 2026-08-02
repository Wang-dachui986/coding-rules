# coding-rules

一个面向 Codex 编程项目的通用治理 Skill。它会为新项目或现有项目建立：

- `AGENTS.md` 执行与审批规则；
- R0–R3 角色分工和任务卡；
- 多对话任务分发规范；
- 上下文压缩、中断恢复和交接文档；
- R1–R3 定向验证、R0 轻量接收和模块末单次系统验收；
- 完成汇报、项目总进度、下一步顺序和逐项审批状态；
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

Skill 会先读取已有治理文件，再创建或安全合并规则、任务卡和交接模板。
它不会覆盖更严格的现有规则，也不会因调用而自动修改产品代码、运行测试、
联网、执行 Git 操作、部署或访问服务器。

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
context recovery, module-level acceptance, approval-aware next steps, evidence
rules, and durable handoffs. It contains generic governance templates only and
does not include product code or project secrets.

## License

MIT License. See [LICENSE](LICENSE).
