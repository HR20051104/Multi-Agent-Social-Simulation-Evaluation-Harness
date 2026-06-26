# Playtest Package v2.7 M5

## 1. What this package is

这是当前 CLI 治理模拟的第一套可试玩包。目标是让玩家连续试玩 20 到 30 分钟，并观察：

- 当前局势是否能看懂
- 不同治理命令是否会产生不同但有边界的反馈
- 记录、核查、传闻、说明、审计之间是否有可理解的区别
- save/load 是否稳定

## 2. What this package is not

这不是：

- 完整 UI
- 完整会议系统
- 完整调查系统
- 真相裁决器
- 惩罚系统

## 3. How to start the CLI

在项目根目录运行 CLI 入口，然后使用内置命令和治理命令交替试玩。

## 4. Available built-in commands

- `help`
- `status`
- `context`
- `clues`
- `norms`
- `residents`
- `reports`
- `events`
- `interactions`
- `availability`
- `assistant`
- `r101`
- `inbox`
- `self`
- `presence`
- `nearby`
- `focus <id>`
- `unfocus`
- `r101 on`
- `r101 off`
- `speech whisper|normal|raised|announcement`
- `scenarios`
- `scenario`
- `new <id>`
- `snapshot`
- `save [name]`
- `load <path-or-name>`
- `saves`
- `quit`

## 5. Available scenarios

当前推荐场景：

- `b2_resource_governance`
- `b2_resource_governance_high_tension`
- `empty_smoke_test`

## 6. Recommended scenario: b2_resource_governance

推荐先从 `b2_resource_governance` 开始。这个场景已经包含：

- 资源清单不完整
- 审批程序存在张力
- 角色之间对核查、说明、记录和规则边界有不同反应

## 7. 20 to 30 minute playtest flow

建议流程：

1. 看场景介绍
2. 查看当前状态
3. 看线索、报告、规范
4. 连续发出 6 到 10 条治理命令
5. 对比传闻、台账、审计、当事人说法
6. 测试 save/load
7. 试一次私下沟通、说明会或公开说明
8. 试一次 availability / consent / avoidance 情况
9. 试一次 assistant / inbox / self
10. 试一次 presence / nearby / focus / speech mode
11. 试一次高压命令
12. 用 `interactions` / `availability` / `inbox` / `self` / `presence` / `snapshot` / `context` 收尾

## 8. What the player should try

- 试试有边界的宽容处理
- 试试无边界的“先算了”
- 试试明确期限
- 试试授权查看记录
- 试试私下沟通、委托询问、说明会、公开说明
- 试试“书面说明 / R101 在场 / 公开说明 / 暂缓跟进”这些替代接触方式
- 试试让 R101 先总结、转写、提醒或整理你的意图
- 试试 `focus A2` 后直接对附近人物说话
- 试试 `r101 off` 和 `r101 on` 的区别
- 试试 `speech whisper` 和 `speech announcement` 的区别
- 试试玩家亲自介入，例如亲自去问、亲自查看记录
- 试试高风险玩家自行动作是否会被安全重定向
- 试试匿名举报
- 试试高压命令
- 试试最后再要求核查总结

## 9. What the player should observe

- built-in commands 不应推进世界
- governance commands 应推进世界
- 线索会积累
- 记录渠道和传闻渠道会被区别对待
- 不同互动渠道应产生不同但安全的沟通摘要
- 某些互动会被提示更适合书面说明、中介在场、公开场合或后续跟进
- 玩家输入会先经过 presence context，而不是默认先进 R101
- `focus` 模拟未来 UI 点击人物
- `speech mode` 会改变可听范围与是否容易被旁听
- R101 可以接收和整理意图，但不会代替世界直接执行结果
- 玩家 self-action 也只是世界中的一种尝试，仍受风险、程序、可见性和安全边界约束
- 高压命令不会直接变成伤害结果
- Projection API 输出应始终是玩家可读文本

## 10. Known limitations

- CLI 仍然很简洁
- 没有图形界面
- 没有完整会议机制
- 还没有完整 scene / map / spatial renderer
- 互动内容仍然是模板化、安全有界的摘要
- actor availability / consent 仍然是 lightweight rule-based estimate
- 没有任务完成生命周期

## 11. Safety boundaries

- 不直接显示 backend IDs
- 不直接显示 true_state
- 不直接显示 hidden norm internals
- 不直接显示 raw scores
- 传闻、匿名线索、私下说法、推断不能单独确认事实
- 高压命令不会直接变成处罚或伤害结果
- 高风险/违法/危险的玩家自行动作会被安全重定向，不提供操作指导
- 复杂物理改造不会由当前 UI 直接执行，只会转成项目/委托/风险意图

## 12. How to save/load

- `save test1`
- `saves`
- `load test1`

save/load 只用于内部状态持久化，玩家看到的仍然必须通过 Projection API。

## 13. How to report issues

如果试玩时发现以下问题，请记录：

- 哪个输出太模糊
- 哪个输出太像 backend
- 哪个命令没有按预期推进
- save/load 后哪里不一致
- 哪条信息看起来像被“直接裁决”为真相
