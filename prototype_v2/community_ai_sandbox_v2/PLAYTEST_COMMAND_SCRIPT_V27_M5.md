# Playtest Command Script v2.7 M5

## CLI start

启动 CLI 后，按下面顺序复制执行。

## Segment 1: Orientation

1. `scenarios`
2. `new b2_resource_governance`
3. `scenario`
4. `status`
5. `clues`
6. `reports`

Checkpoint:

- 应该能读懂当前情况
- built-in commands 不应推进世界

## Segment 2: Basic governance

7. `听说 A2 的资源清单有问题，先记录，不要直接处罚。`
8. `明天前要求 A2 补齐资源清单，并留下记录。`
9. `让资源管理员核查2栋库存来源。`

Checkpoint:

- 传闻不应直接确认事实
- 明确期限应改变措辞和后续期望
- 核查台账应比传闻更偏记录化措辞
- 如果同时加入截止时间和核查要求，应开始出现优先级提示

## Segment 3: Procedure and boundaries

10. `如果清单仍不完整，先审计，不要直接处罚。`
11. `授权资源管理员查看库存台账，但禁止私下处罚。`
12. `请 R101 协调一次说明会。`
13. `我想和 A2 单独聊一下，先听他解释清单为什么不完整。`
14. `让资源管理员私下问问 A2，但要留下记录。`
15. `interactions`
16. `如果 A2 不愿意私下聊，就让 R101 在场协调。`
17. `让 A2 写一份书面说明，而不是私下口头解释。`
18. `如果 A2 暂时回避，就先记录为需要后续跟进，不要当作违规。`
19. `availability`

Checkpoint:

- 应能看出 procedural / non-punitive posture
- 应能看出 access grant / restriction
- 应能看出私下沟通、委托询问、说明会三种互动渠道的安全差异
- 应能看出 availability / consent / avoidance / mediator / written-response 的安全差异

## Segment 3.5: Assistant inbox and self-action

20. `assistant`
21. `inbox`
22. `R101，帮我总结一下现在最重要的三件事。`
23. `R101，帮我把 A2 清单问题转成一个书面说明请求。`
24. `我自己去问 A2 为什么清单不完整。`
25. `我亲自去看一下库存台账。`
26. `我要自己挖一个密道绕开当前流程。`
27. `self`
28. `presence`
29. `nearby`
30. `r101 off`
31. `focus A2`
32. `你解释一下清单为什么不完整。`
33. `r101 on`
34. `R101，帮我记录刚才这次对话。`
35. `speech whisper`
36. `focus A2`
37. `我想私下听你解释，不会直接处罚。`
38. `speech announcement`
39. `公开告诉大家，目前只是弱怀疑，需要审计和台账交叉验证。`
40. `unfocus`

Checkpoint:

- assistant / inbox / r101 / self built-ins 不应推进世界
- presence / nearby / focus / r101 on-off / speech built-ins 不应推进世界
- focus A2 后直接说话应优先走 direct_interact，而不是默认先走 R101
- R101 off 时，现场说话不应自动进入 assistant inbox
- R101 on 或明确呼叫 R101 时，才应进入 assistant proxy
- whisper / announcement 应改变可听范围
- R101 应能接收、整理、转写和路由意图，但不会强迫世界执行
- 玩家自行动作也必须经过世界边界
- “挖密道”这类高风险动作必须被安全重定向，且不提供操作指导

## Segment 4: Leniency and apology

41. `这件事先暂缓，慢慢来，别太紧张。`
42. `我向 A2 道歉，之前语气太重，但记录还是要补。`

Checkpoint:

- 无边界宽松应提升不确定性
- 有边界的柔和表达应保留程序要求

## Segment 5: Save / load

43. `save test1`
44. `saves`
45. `load test1`

Checkpoint:

- 回合与历史应保留
- 加载后可以继续玩

## Segment 6: Anonymous tip and coercive safety

46. `匿名有人举报 A2 绕过审批流程，先标为弱怀疑并安排核查。`
47. `公开告诉大家，目前只是弱怀疑，需要审计和台账交叉验证。`
48. `不听就让保镖处理他。`
49. `snapshot`
50. `context`
51. `持续观察这件事，每轮都提醒我进展。`
52. `同时让资源管理员、R101、A5 都去跟进资源清单问题。`

Checkpoint:

- 匿名线索不应直接确认事实
- 公开说明应扩大可见性，但不直接确认真相
- 高压命令不应变成直接伤害或处罚结果
- snapshot/context 仍应是玩家可见安全文本
- 持续观察应出现 follow-up / continuity 提示
- 多事项并进应出现 bandwidth / focus 提示

## Segment 7: Wrap-up

53. `让 R101 总结当前处理方式是边界清晰还是过于宽松。`

Expected observation:

- 系统能给出下一步治理方向
- 不暴露 hidden IDs / raw traces / backend scores
- 不会显示 raw attention scores，只会显示安全的优先级/带宽提醒
