# 检查清单

这些清单只服务三个既有闸门：子任务之间的轻量接收、模块末一次系统性验收、
发布或部署前检查。清单不新增状态词，不代替任务卡、交接或证据，也不批准
下一张任务卡或本次发布。

每一项用现有验证状态填写：`PASS`、`FAILED`、`NOT_RUN`、`LIMITED`。未执行的
检查保持 `NOT_RUN`，不得写成通过。不适用时写明 `NOT_APPLICABLE`，并保留
是谁确认的。

R0 把对应章节抄入本次交接或证据后再填写。R1–R3 不代填项目总进度，也不用
清单自行开始下一任务。

## 1. R0 轻量接收

在子任务之间使用。不重跑全仓测试、完整构建或完整浏览器矩阵。

- [ ] 任务卡 ID、版本和摘要与分发记录一致：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 负责人、允许路径和允许命令没有被扩大：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 角色交接已更新，并写明结果已返回 R0：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 证据只包含实际执行的命令、退出状态和脱敏输出：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] `NOT_RUN`、`FAILED`、`BLOCKED` 与 `APPROVED_NOT_EXECUTED` 没有被写成通过：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 依赖和高风险停止条件已核对：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 接收结论仅为 `ACCEPTED_AS_MODULE_INPUT`、`REJECTED` 或 `BLOCKED_SAFE_STOP_ACCEPTED_NOT_MODULE_INPUT`：`[填写一个]`

## 2. 模块系统性验收

仅在该模块全部子任务、共享集成和必要运行表面完成后使用一次。

- [ ] 各子任务已被接受为模块输入，或已记录明确排除：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 共享集成已执行并单独记录证据：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 定向验证和本次系统验收分开记录：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 真实用户表面的手工 QA 已记录，或不适用：`[PASS/NOT_APPLICABLE/NOT_RUN]`
- [ ] 未验证的平台、系统或客户端标记为 `NOT_RUN`：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 任务卡、证据和交接没有写入秘密：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 验收结论已写入 `docs/handoffs/PROJECT.md`，且没有替代原始证据：`[PASS/FAILED/NOT_RUN/LIMITED]`

## 3. 发布检查

发布、部署或打标签前使用。当前任务获批不自动批准发布。

- [ ] 发布范围与已批准任务卡一致：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 已区分源码、构建候选、已部署版本和正式发布版本：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 制品摘要、适用平台、测试结果和已知限制已记录：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 安装、使用、升级、回滚、卸载和排错说明已覆盖，或不适用：`[PASS/NOT_APPLICABLE/NOT_RUN]`
- [ ] 回滚和清理步骤已写在获批任务卡中：`[PASS/FAILED/NOT_RUN/LIMITED]`
- [ ] 部署前只读预检和可恢复备份已记录，或不适用：`[PASS/NOT_APPLICABLE/NOT_RUN]`
- [ ] 部署后的真实运行表面检查已记录，或仍为 `NOT_RUN`：`[PASS/NOT_RUN/LIMITED]`
- [ ] 项目所有者已批准这一精确发布版本：`[WAITING_APPROVAL/APPROVED_NOT_EXECUTED/COMPLETED/BLOCKED]`
