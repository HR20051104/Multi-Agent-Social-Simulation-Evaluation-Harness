# Dynamic Influence–Signal Architecture v0.3
# 动态影响-信号三层架构说明

> 本文档用于修订《AI 社区沙盘 / crisis 社区治理游戏》的底层架构。  
> v0.3 在 v0.2 基础上补充世界时钟与持续运行系统，并保留此前三个关键修正：  
> 1. 行动可以直接作用于人和组织，不必先通过世界对象痕迹。  
> 2. 玩家作为区长不需要被系统刻画“对他人的信任度”，玩家判断由玩家自己完成。  
> 3. 三层框架虽然敲定，但每一层内部都应是高维的，否则难以表达边缘人物进入核心圈、关系跃迁、派系重组等现象。

---

## 1. 架构升级原因

早期 Rule Mode 文本原型以 `TaskEngine / EventEngine / EvidenceEngine` 为主要骨架：

```text
玩家命令
→ 生成任务/事件
→ 检查资源
→ 更新角色状态
→ 生成后台事件
→ 通过线索系统暴露
```

这套架构可以验证基本玩法，但容易把世界写成“任务列表 + 事件列表”，而不是一个真正会自己演化的社会系统。

真实社会影响不是单点的：

```text
压迫 A
→ 不只是 A 压力上升
→ B 会观察
→ 其他楼长会调整预期
→ 报告会变得更保守
→ 信息传播路径会改变
→ 居民可能听到变形版本
→ 派系关系可能重组
```

因此，底层应从“任务/事件驱动”升级为：

> **动态影响-信号三层架构。**

---

## 2. 最高设计原则

### 2.1 优雅大一统原则

不要为每一种社会现象单独写一个特殊系统：

```text
贪污系统
承诺系统
密谋系统
谣言系统
起义系统
眼线系统
恐惧系统
信任系统
```

而应统一表达为：

```text
社会网络中的关系变化
世界对象中的现实状态变化
证据-信号层中的传播、记忆、阻断、泄露和误读
```

也就是说：

> **社会现象不是独立模块，而是同一个动态网络-信号机制在不同条件下的表现。**

---

## 3. 三层核心架构

整个世界分为三层：

```text
1. Social Network Layer      社会网络层
2. World Object Layer        世界对象层
3. Evidence-Signal Layer     证据-信号层
```

但这三层不是单向流水线。  
行动不一定必须经过“世界对象 → 痕迹 → 信号”才能影响社会网络。

更准确的结构是：

```text
行动 / 事件 / 命令 / 环境变化
        ↓
可以同时作用于：
- 社会网络层：直接影响人和组织
- 世界对象层：改变资源、任务、建筑、制度、地点
- 证据-信号层：产生命令、承诺、报告、谣言、线索、记忆
        ↓
三层之间继续相互反馈
```

---

## 4. 修正后的核心闭环

v0.1 中曾写成：

```text
社会网络状态
→ 人/组织采取行动
→ 世界对象发生变化
→ 留下痕迹或产生信号
→ 信号被发现、传播、阻断、泄露或误读
→ 反过来改变社会网络
```

这条链路仍然存在，但它只是其中一种闭环，主要对应“行为通过现实痕迹被发现后影响社会关系”。

v0.2 采用更一般的表达：

```text
社会网络状态
→ 主体采取行动
→ 行动同时产生：
   1. 对人的直接影响
   2. 对世界对象的现实改变
   3. 对证据-信号层的信息改变
→ 影响在社会网络中传播、叠加、延迟、衰减
→ 世界对象留下 trace 或改变约束
→ 信号被传播、阻断、误读、记忆、泄露
→ 三层共同改变后续行动倾向
```

### 4.1 直接作用于人的例子

玩家说：

```text
公开训斥 A
```

这不需要先经过世界对象。  
它会直接进入社会网络层：

```text
A 压力上升
A 对区长的服从可能上升
A 对区长的真实亲近下降
旁观者对区长治理风格形成新预期
其他楼长发言更谨慎
```

同时也可能产生信号：

```text
公开训斥这一行为被旁观者记住
居民之间出现传闻
楼长群体形成“坏消息最好少说”的预期
```

如果现场有会议记录、公告、录音、目击者，则它也会连接到世界对象或 trace。

### 4.2 通过世界对象影响人的例子

玩家批准经费给 B 修仓库：

```text
World Object Layer:
预算池减少
task_T1 获得资源
仓库项目推进

Social Network Layer:
B 对区长服从和合作意愿上升
A 可能产生资源不公感
物业对审批流程形成预期

Evidence-Signal Layer:
拨款记录
会议通知
项目进度报告
其他楼长听到的传闻
```

### 4.3 通过信号影响人的例子

玩家承诺未来修 2 栋垃圾点：

```text
Evidence-Signal Layer:
生成 promise signal

Social Network Layer:
2栋楼长短期信任上升
2栋居民预期上升

World Object Layer:
暂时不一定发生变化

后续：
若兑现，则正向记忆沉积
若失信，则 promise 变质为 broken_expectation signal
```

---

# 5. Social Network Layer 社会网络层

## 5.1 定义

社会网络层只包含：

```text
人
组织
群体
派系
临时联盟
外部势力
```

不要把房屋、垃圾点、火箭、仓库、账本等物体作为社会网络节点。  
否则网络会变得难解释。

## 5.2 玩家节点的特殊性

玩家/区长可以作为社会网络中的“影响源”和“权力中心”存在，但系统不需要刻画：

```text
chief.trust_to_A
chief.trust_to_B
chief.preference
chief.inner_belief
```

因为区长就是玩家。  
玩家对谁信任、怀疑、偏爱、讨厌，应由玩家自己判断，不应由系统替玩家决定。

系统可以刻画的是：

```text
A 对区长的信任
A 对区长的恐惧
A 对区长的服从
A 对区长的隐瞒倾向
A 对区长命令的执行概率
A 认为区长是否可靠
```

也就是说：

> **系统刻画他人如何看待玩家，而不是玩家内心如何看待他人。**

### 5.2.1 玩家认知与玩家判断的区别

系统可以维护：

```text
玩家已知线索
玩家收到的报告
玩家看到的地图现象
玩家确认/怀疑的事实列表
```

但不能替玩家得出主观判断：

```text
玩家信任 A = 70
玩家讨厌 B = 30
```

玩家自己的判断应通过 UI、报告、线索面板提供信息，由玩家自己在脑中完成。

---

## 5.3 节点类型

第一版可包含：

```text
chief                  区长/玩家，特殊节点
building_leader        楼长
deputy_leader          副楼长
property_manager       物业经理
security_chief         保安队长
resident_group         居民群体
construction_team      施工队
merchant_group         商户群体
informal_faction       非正式派系
external_authority     外部监管/救援组织
```

## 5.4 社会边类型

人与组织之间可以有多种边：

```text
trust                  信任
authority              权力/命令
obedience              服从
fear                   恐惧
loyalty                忠诚
hostility              敌意
interest_alignment     利益一致
dependency             依赖
information_flow       信息流
secrecy                隐秘协作
conspiracy             密谋
empathy                同情/共情
competition            竞争
status_distance        地位距离
access                 接近核心圈的通道
reputation             声誉影响
```

这些边不是固定的，会被事件、信号、历史记忆持续改变。

---

## 5.5 社会网络是高维的

社会网络不是一张简单二维关系图。  
每个节点与边都可以有高维状态。

### 5.5.1 节点高维属性

一个人物/组织节点可以包含：

```text
身份维度：职位、所属楼栋、组织身份、派系身份
心理维度：压力、恐惧、希望、愤怒、安全感
行为维度：执行力、拖延倾向、隐瞒倾向、合作倾向
信息维度：知道什么、不知道什么、误解什么、相信什么
资源维度：掌握多少资源、能调动谁、欠谁人情
声誉维度：被谁尊重、被谁怀疑、被谁看不起
权力维度：能命令谁、能绕过谁、能接近谁
位置维度：处在核心圈、边缘圈、地下网络、外部网络
```

### 5.5.2 边的高维属性

人与人之间的边也不只是一个数值：

```text
strength               强度
direction              方向
visibility             是否公开
channel_type           正式/非正式/地下/亲密/制度
latency                传播延迟
bandwidth              信息带宽
distortion             失真率
trust                  信任度
fear                   恐惧成分
dependency             依赖成分
secrecy                保密程度
volatility             易变性
```

### 5.5.3 为什么需要高维

如果社会网络只是二维或少数几个变量，很难表达：

```text
边缘人物突然进入核心圈
副楼长被任命后地位跃迁
普通居民因为掌握关键证据而变重要
施工队因为掌握资源成为关键节点
某个低级保安因为控制入口而获得权力
某个居民群因为谣言传播能力强而影响全局
```

这些现象本质上是高维网络中的“中心性跃迁”。

---

# 6. World Object Layer 世界对象层

## 6.1 定义

世界对象层包含现实世界中的对象、资源、制度、任务、空间和状态。

它们不是“社会关系节点”，而是：

```text
现实约束
资源载体
任务目标
行动场景
证据载体
地图表现
制度状态
```

## 6.2 对象类型

```text
building               建筑
facility               设施
resource_pool          资源池
task                   任务
policy                 政策
position               职位
document               文档/账本
location               地点
equipment              设备
construction_site      施工地
storage                仓库
surveillance_device    监控设备
notice_board           公告栏
```

## 6.3 世界对象不参与什么

世界对象不应具有：

```text
信任
恐惧
忠诚
敌意
密谋
心理压力
主观预期
```

例如：

```text
仓库不会信任区长
垃圾点不会反抗
账本不会害怕审计
```

但它们可以：

```text
被管理
被破坏
被审计
被占用
被改造
留下痕迹
成为争议焦点
影响居民生活
改变资源流动
```

## 6.4 世界对象也是高维的

世界对象虽然不参与社会心理，但其状态也不是单维的。

例如一个仓库可以有：

```text
容量
库存
管理者
访问权限
安全等级
账目一致性
被审计频率
物理位置
可见度
历史异常记录
与任务的关联
与证据 trace 的关联
```

一个职位可以有：

```text
权限范围
继任关系
副职列表
实际权威
名义权威
可绕过程度
责任归属
可问责性
信息通道
资源审批权
```

一个任务可以有：

```text
目标
执行者
资源池
审批状态
真实进度
上报进度
风险
压力
依赖对象
公众可见度
失败后责任归属
```

因此，世界对象层不是简单物品表，而是现实约束空间。

---

# 7. Evidence-Signal Layer 证据-信号层

## 7.1 定义

证据-信号层是社会网络层和世界对象层之间的连接介质。

它负责表达：

```text
命令
承诺
报告
谣言
警告
请求
威胁
隐瞒
审计结果
客观痕迹
线索
记忆
误解
泄露
```

一句话：

> **证据-信号层负责让行动、现实变化和社会认知互相转化。**

注意：  
信号不只是从世界对象痕迹中产生。  
信号也可以直接来自人的发言、命令、会议、表态、沉默、威胁、承诺、背叛。

## 7.2 三种主要信号来源

### A. 人直接产生的信号

```text
命令
承诺
警告
威胁
公开表扬
公开训斥
会议发言
私下密谋
沉默
拒绝表态
```

### B. 世界对象产生的信号

```text
账本异常
库存减少
施工延误
建筑破损
道路拥堵
监控录像
公告记录
资源短缺
```

### C. 二次传播产生的信号

```text
谣言
误读
泄密
转述
伪报
宣传
匿名举报
审计摘要
楼长报告
```

---

# 8. 信号模型

## 8.1 Signal 定义

信号是可以在社会网络中传播、被记忆、被阻断、被误读、被泄露的信息单位。

信号不一定是真实的。  
信号可以是事实、谎言、承诺、命令、传闻、暗示、威胁、报告或误解。

## 8.2 Signal 字段建议

```python
Signal:
    id: str
    day_created: int
    signal_type: str
    source_node_id: str | None
    intended_receivers: list[str]
    current_holders: list[str]
    content_summary: str
    truth_status: str              # true / false / mixed / unknown
    confidence: float              # 对接收者而言的置信度
    intensity: float               # 影响强度
    secrecy_level: float           # 保密程度
    spread_rate: float             # 传播速度
    decay_rate: float              # 衰减速度
    distortion_rate: float         # 传播变形率
    memory_strength: float         # 被记住的强度
    blocked_by: list[str]
    linked_world_objects: list[str]
    linked_traces: list[str]
    tags: list[str]
```

## 8.3 Signal 类型

```text
order                  命令
promise                承诺
request                请求
warning                警告
threat                 威胁
report                 报告
rumor                  谣言
clue                   线索
audit_result           审计结果
complaint              投诉
propaganda             宣传
concealment            隐瞒
confession             坦白
accusation             指控
coordination           协调
conspiracy             密谋信号
leak                   泄露
memory                 记忆沉积
silence                沉默
public_gesture         公开姿态
```

---

# 9. 统一解释：承诺、预期、密谋、谣言、泄露

## 9.1 承诺

承诺不是独立系统，而是一类带未来指向的信号。

```text
promise signal:
source = 区长
target = 2栋居民 / 2栋楼长
content = 未来修垃圾点
deadline = 7 天内
memory_strength = 高
```

如果兑现：

```text
promise → fulfilled_signal
相关节点对区长可靠性评价上升
制度可信度上升
```

如果未兑现：

```text
promise → delayed_promise → broken_expectation → distrust_signal
相关节点对区长可靠性评价下降
future_promise_confidence 下降
rumor_spread 上升
```

注意：  
这里刻画的是别人如何评价区长承诺，不刻画玩家自己如何评价别人。

## 9.2 预期

预期是历史信号在节点中沉积形成的预测权重。

例如，玩家多次“下任务但不给经费”，楼长网络会形成预期：

```text
区长会甩锅
区长的 deadline 不可靠
接任务前必须索要书面审批
坏消息最好别直接报告
```

预期不需要单独建表，可以通过：

```text
信号记忆
历史承诺兑现率
报告被惩罚记录
资源审批可靠性
```

共同生成。

## 9.3 密谋

密谋是局部封闭的隐藏信号回路。

```text
signal_type = conspiracy
source_nodes = [A, B]
allowed_receivers = [A, B]
blocked_receivers = [chief, audit_team]
secrecy_level = 高
leak_probability = 中低
```

密谋会改变社会网络：

```text
A-B secrecy 边增强
A/B 到区长的信息边失真
对外 report 信号被包装或伪造
```

## 9.4 谣言

谣言是低置信度、高传播率、高变形率的信号。

```text
truth_status = unknown / mixed
confidence = 低到中
spread_rate = 高
distortion_rate = 高
```

谣言可以来自：

```text
低强度 trace
未验证 clue
被压制的真实事件
居民情绪高压
信息真空
敌对派系操控
```

## 9.5 隐瞒与压制

隐瞒不是删除事件，而是对信号施加传播控制：

```text
propagation_control:
    target_signal
    method = conceal / suppress / distort / delay
    controller = A
    leakage_rate
    stress_cost
    discovery_risk
```

隐瞒会导致：

```text
明面信号减少
知情者压力上升
虚假稳定增加
泄露风险上升
被发现后的信任损失更大
```

## 9.6 泄露

泄露是被阻断信号的非预期传播。

泄露来源：

```text
知情者压力过高
信任边太强，忍不住告诉亲近节点
审计发现 trace
巡查发现迹象
匿名举报
敌对派系揭露
事故使隐藏信号实体化
```

---

# 10. 影响传播模型

## 10.1 Disturbance 定义

扰动是对社会网络、世界对象或信号层施加的影响源。

扰动可以来自：

```text
玩家命令
NPC 行动
后台事件
自然灾害
季节变化
资源短缺
外部救援
政策变化
事故
谣言爆发
公开表态
沉默
```

## 10.2 扰动不是直接结果

玩家说：

```text
强压 A 完成任务
```

系统不应只执行：

```text
A.stress += 20
```

而应生成扰动：

```python
Disturbance:
    type = coercive_pressure
    source = chief
    entry_points = [A, task_T1]
    intensity = 0.8
    propagation_channels = [authority, fear, information_flow, empathy]
    decay = 0.4
    duration = 3 days
```

然后它沿社会网络传播，同时可能作用于任务对象和信号层。

## 10.3 多扰动叠加

同一节点可以同时受到多个扰动：

```text
A 被强压任务
B 被额外批经费
居民听到谣言
天气导致施工暂停
审计即将开始
```

节点状态应由多源影响叠加：

```text
当前状态 = 原状态 + 直接扰动 + 传播扰动 + 历史记忆 + 环境压力 + 自身特质过滤
```

## 10.4 时间延迟

扰动传播不应瞬间完成。  
不同边有不同传播速度：

```text
权力命令：快
谣言传播：中快
信任变化：中慢
资源流动：依物流速度
恐惧扩散：快但可能转入地下
制度变化：慢
地位跃迁：通常慢，但可被关键事件瞬间加速
```

这支持“随时介入”和“并发影响”。

---

# 11. 随时介入与并发

玩家可以在任意时间点下达多个命令：

```text
t=1：让 A 修仓库
t=2：让 B 审计账目
t=3：给 C 任命副楼长
t=4：要求物业压缩预算
```

这些行为不是排队变成单线程，而是同时向系统投下多个扰动。

```text
每个扰动有：
- 入口节点
- 影响类型
- 传播速度
- 衰减率
- 持续时间
- 可见度
- 与其他扰动的叠加方式
```

因此，一个节点可能在某天同时受到：

```text
任务压力
同伴传闻
资源不足
区长承诺
审计威胁
天气压力
```

---

# 12. 高维层内结构与“边缘进入核心”

## 12.1 为什么高维是必要的

如果每个 layer 都是低维表格，就很难表达：

```text
一个普通居民因为掌握关键证据突然变重要
一个副楼长因为被授权审计进入核心圈
一个保安因为控制出入口变成关键人物
一个商户因为掌握物资渠道成为权力节点
一个外部志愿者因为救援资源进入核心决策
```

这些不是简单的“职位 +1”。  
它们是多个维度同时变化：

```text
信息中心性上升
资源控制力上升
接近区长的路径缩短
被其他节点关注
被拉拢或打压概率上升
可发出高影响信号
```

## 12.2 核心圈不是固定名单

“核心圈”应是网络状态的结果，而不是写死的角色名单。

可以通过高维中心性计算：

```text
authority_centrality       权力中心性
information_centrality     信息中心性
resource_centrality        资源中心性
trust_centrality           信任中心性
fear_centrality            恐惧中心性
access_to_chief            接近区长程度
issue_relevance            当前议题相关性
```

边缘人物可能因为某个议题突然变成核心：

```text
仓库失窃案中，仓库管理员的信息中心性上升
供暖危机中，维修工资源中心性上升
谣言危机中，居民群主传播中心性上升
救援到来时，外部联络员权力中心性上升
```

## 12.3 地位跃迁

地位跃迁可由以下机制触发：

```text
任命
授权
掌握关键证据
控制关键资源
成为关键任务负责人
成为主要信号源
成为谣言中心
救援或危机中的不可替代性
旧核心圈失信或崩溃
```

地位跃迁后，系统应自动改变：

```text
别人向其传播信号的概率
其发言被重视的程度
其被拉拢/打压的概率
其对任务和资源的影响力
其成为派系中心的概率
```

---

# 13. 网络重组机制

## 13.1 边权变化

信号和扰动会改变社会边：

```text
信任增强/下降
恐惧增强
信息流变窄
密谋边生成
敌意边生成
依赖边增强
权力边失效
接近核心路径改变
```

## 13.2 新组织生成

当某些社会关系形成闭环时，可以生成新组织：

```text
楼长互助群
反对派小组
居民自治会
地下交易圈
亲区长派系
黑市网络
```

生成条件例子：

```text
多个节点对区长 trust 低
彼此 empathy 高
私下 information_flow 高
共同压力源存在
secrecy 边增强
```

## 13.3 网络拆分

高压、资源不公、隐瞒失败、承诺破裂可能导致：

```text
原有居民群分裂
楼长群体分裂
物业与楼长断裂
保安倒向居民或区长
```

## 13.4 网络合并

共同危机、成功合作、公开透明、资源公平可能导致：

```text
不同楼栋合作
楼长与物业互信增强
居民组织与官方协作
派系消解
```

---

# 14. 与旧模块的关系

新架构不是废弃旧模块，而是重新定位旧模块。

## 14.1 TaskEngine

旧定位：

```text
任务系统是核心
```

新定位：

```text
任务是 World Object Layer 中的一类对象。
任务执行会生成扰动、trace、signal。
```

任务状态变化：

```text
资源不足
进度滞后
被强制推进
完成
失败
虚报
事故
```

都应通过证据-信号层进入社会网络。

## 14.2 EventEngine

旧定位：

```text
后台事件生成器
```

新定位：

```text
事件是社会网络与世界对象交互后产生的结果。
事件可以直接影响社会网络，也可以生成 trace 和 signal。
```

事件不应是随机刷怪，而应来自网络条件：

```text
高压力 + 低信任 + 高资源诱惑 + 弱审计
→ 挪用/虚报倾向上升
```

## 14.3 EvidenceEngine

旧定位：

```text
从隐藏事件生成 clue
```

新定位：

```text
管理 trace → signal → clue → memory 的转换。
负责发现、置信度、误读、泄露、传播。
```

## 14.4 ReportEngine

旧定位：

```text
生成每日文字报告
```

新定位：

```text
把高维社会网络和世界对象状态投影成玩家可理解的信息界面。
```

ReportEngine 不应暴露真相，只应暴露玩家当前认知。

---

# 15. 玩家认知投影

底层网络可以复杂，但玩家不应看到完整网络。

玩家看到的是：

```text
地图表现
会议发言
日报
审计结果
线索面板
人物态度
任务进度
资源账目
异常迹象
```

玩家认知不等于真实世界。

玩家可见信息应来自：

```text
signal 当前是否到达玩家节点
clue 是否被发现
report 是否被伪造
source 可靠性
confidence 置信度
information_distortion 信息失真
```

## 15.1 认知层级

玩家对某个话题的认知可分为：

```text
unknown                完全不知道
weak_suspicion          弱怀疑
suspected               有怀疑
probable                大概率
confirmed               已确认
misled                  被误导
```

注意：  
玩家认知层记录的是“玩家有哪些信息”，不是“玩家该信任谁”。

---

# 16. 第一版实现建议

不要一上来实现完整高维网络。

第一版 v2 原型只实现最小三层：

## 16.1 社会节点

```text
chief
A1 1栋楼长
A2 2栋楼长
A3 3栋楼长
A4 物业经理
A5 保安队长
resident_group_B1
resident_group_B2
resident_group_B3
```

## 16.2 社会边

先支持：

```text
trust
authority
fear
information_flow
secrecy
empathy
access
reputation
```

其中：

```text
chief → others:
    authority 可存在
others → chief:
    trust / fear / obedience / concealment tendency 可存在
chief 对 others 的 trust 不需要系统刻画
```

## 16.3 世界对象

```text
budget_pool
material_pool
labor_pool
task_T*
building_B1/B2/B3
storage
ledger
position_P*
```

## 16.4 信号类型

```text
order
promise
report
rumor
clue
audit_result
concealment
conspiracy
public_gesture
silence
```

## 16.5 扰动类型

```text
funding
coercion
appointment
audit
resource_shortage
task_delay
public_support
broken_promise
public_rebuke
private_warning
```

## 16.6 最小闭环

测试用例：

```text
Day 1:
玩家强压 A2 建仓库，但不给经费

系统：
生成 coercion disturbance
生成 order signal
task_T1 blocked
A2 stress 上升
A2 对 chief trust 下降
A2 fear 上升
A1/A3 通过 information_flow 得到弱信号
楼长群体对 chief 预期恶化
后台生成 private_complaint signal
若 secrecy 边增强，则形成隐藏抱怨回路
若玩家 audit，则可能从 task_T1 / ledger trace 生成 clue
```

第二个测试用例：

```text
Day 1:
玩家任命一个普通居民 R1 为临时物资协调员

系统：
position_P_new 生成
R1 authority_centrality 上升
R1 resource_centrality 上升
R1 access_to_chief 上升
原物业经理可能感到权力被削弱
居民群体可能对 R1 的态度分化
R1 从边缘节点进入当前物资议题核心圈
```

---


---

# 16A. 世界时钟与持续运行系统

## 16A.1 核心原则

游戏世界不应只在玩家下命令时推进。

玩家不操作时，系统也应持续运行：

```text
任务继续执行
信号继续传播
扰动继续衰减或叠加
人物继续交流
资源继续消耗
建筑继续老化
后台事件继续生成
谣言继续扩散
承诺继续等待兑现
密谋继续发展或泄露
```

也就是说：

> **玩家不是按回合推动世界存在，而是在一个持续运行的世界中随时介入。**

## 16A.2 World Clock 世界时钟

底层应存在一个统一的世界时钟：

```python
WorldClock:
    current_tick: int
    current_day: int
    time_of_day: str
    tick_length_minutes: int
    paused: bool
    speed: float
```

建议第一版可简化为：

```text
1 tick = 半天或一天
```

后续 2D 版本可细分为：

```text
早晨
中午
下午
晚上
夜间
```

## 16A.3 Tick 推进内容

每个 tick 自动推进：

```text
1. 任务进度推进
2. 资源消耗与补充
3. 信号传播、衰减、变形
4. 扰动传播、衰减、叠加
5. 角色心理状态更新
6. 社会边权更新
7. 世界对象状态更新
8. 后台事件倾向计算
9. trace / clue / rumor 生成与传播
10. 玩家可见报告更新
```

即使玩家没有输入命令，以上过程也会继续发生。

## 16A.4 随时介入

玩家命令不应被设计成“一个回合只能下一个命令”。

更合理的是：

```text
玩家可以在任意 tick 插入命令
命令生成 signal / disturbance / task / policy
这些对象进入正在运行的世界
与已有扰动叠加
```

例如：

```text
t=10：A 正在修仓库
t=11：玩家任命 B 为副楼长
t=12：谣言开始传播
t=13：玩家安排审计
t=14：A 的虚报风险因为审计扰动而变化
```

## 16A.5 玩家不操作时的世界演化

系统应支持“观察/等待”玩法：

```text
玩家选择不介入
→ 世界继续运行
→ 任务可能自然完成、拖延或失败
→ 后台关系继续变化
→ 一些小事件可能自愈
→ 一些问题可能发酵
→ 一些隐藏信号可能泄露
```

这对游戏体验很重要，因为它避免了世界变成“玩家输入一句，系统回应一句”的聊天式结构。

## 16A.6 与动态影响-信号网络的关系

World Clock 是动态影响-信号网络的时间轴。

```text
扰动需要时间传播
信号需要时间扩散
记忆需要时间沉积
关系需要时间重组
建筑需要时间老化
承诺需要时间兑现或失信
密谋需要时间发展
```

没有时钟，网络就只是静态图；  
有了时钟，网络才会像水面一样产生波纹、延迟、叠加和回声。


# 17. 对 CC 的实现指令摘要

如果将此文档交给 coding agent，应要求其：

```text
1. 不要继续把 TaskEngine/EventEngine 当最高层。
2. 新增 InfluenceSignalNetwork 作为底层核心。
3. 社会网络只包含人/组织节点。
4. 世界对象单独存储，不参与信任/恐惧等社会边。
5. 证据-信号层连接社会网络和世界对象，但行动也可以直接作用于社会网络。
6. 玩家命令转化为 signal + disturbance，而不是直接改最终结果。
7. 不要刻画 chief 对其他人的 trust/preference，玩家自己判断。
8. 任务、事件、报告、线索都应挂到三层架构上。
9. 支持多个扰动并发、传播、衰减、叠加。
10. 支持信号记忆、阻断、泄露、置信度。
11. 每层内部应保留高维属性接口，不要写死成低维表。
12. 支持边缘节点通过授权、证据、资源控制、信号中心性进入核心圈。
13. 玩家只能看到信号到达玩家节点后的认知投影。
```

---

# 18. 当前文档的定位

本文档不是最终完整实现文档，而是：

```text
v2 架构方向说明
旧 Rule Mode 原型的底层修订
后续实现规格的基础
```

它应放在 `v2/` 或 `architecture_v2/` 文件夹下，作为新版本核心架构。

推荐文件名：

```text
dynamic_influence_signal_architecture_v0_3.md
```

---

# 19. 一句话总结

> 游戏世界由人和组织构成高维动态社会网络，由建筑、资源、任务、制度构成高维现实对象层，由命令、承诺、报告、谣言、证据和记忆构成证据-信号层。玩家和 NPC 的每个行为都不是直接结果，而是向系统投下扰动；扰动可以直接作用于人，也可以改变世界对象或产生信号，并通过传播、记忆、阻断、泄露、认知投影和关系重组，逐步改变整个社区。
