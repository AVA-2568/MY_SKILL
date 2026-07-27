---
name: system-design
description: Design a production-ready system architecture from product goals, workload, reliability, security, and operational constraints. Use whenever the user asks for system design, architecture, distributed systems, service decomposition, capacity planning, scalability, high availability, SLOs, data flow, migration strategy, or tradeoff analysis—even if they only say "design the backend" or "how should this system be structured." Produce an explicit architecture specification before implementation; do not silently jump to code.
user-invocable: true
agent_created: true
risk_level: mid
category: generation
---

# System design（系统架构设计）

把产品目标和约束转换为可评审、可演进、可落地的系统架构规格。关注组件边界、数据流、容量、可靠性、安全和运维；不直接实现业务代码。

## 使用时机

- 设计新系统、平台、服务或分布式架构
- 拆分单体、规划微服务、事件驱动或异步任务
- 评估吞吐、延迟、容量、SLO、可用性和扩展路径
- 需要在多种架构方案之间做权衡
- 规划迁移、灰度发布、回滚和灾备

## 输入与边界

收集目标、范围、用户规模、流量峰值、数据规模、延迟目标、可用性目标、合规约束、预算、团队和已有系统。缺失值先列为假设并给出敏感性分析；只有会改变架构结论时才追问。

本技能产出架构设计，不负责实现代码（→ `generate-api` 或其他生成技能）；不替代业务决策（→ `decide-product`）；不执行部署或迁移命令。

## 流程

1. **界定范围**：列出目标、非目标、用户旅程和关键用例。
2. **量化约束**：估算 QPS、并发、存储增长、带宽、峰值系数和成本边界。
3. **定义 SLO**：明确可用性、延迟、错误率、RTO、RPO 和监控窗口。
4. **拆分组件**：确定服务边界、接口、数据所有权和依赖关系。
5. **绘制数据流**：说明同步/异步路径、队列、缓存、重试、超时和幂等。
6. **选择存储**：说明数据库、索引、分片、备份、保留和一致性模型。
7. **设计可靠性**：分析限流、熔断、降级、故障转移、灾备和恢复。
8. **设计安全**：覆盖身份、权限、密钥、数据分级、审计和攻击面。
9. **设计可观测性**：定义日志、指标、追踪、告警和容量信号。
10. **比较权衡**：至少给出一个替代方案、选择理由和已接受的代价。
11. **规划演进**：给出阶段化实施、迁移、灰度和回滚路径。

## 精确输出模板

```markdown
# 系统架构设计：[系统名]
## 1. 目标、非目标与假设
## 2. 约束与容量模型
| 指标 | 基线 | 峰值 | 依据 / 不确定性 |
## 3. SLO 与可靠性目标
## 4. 架构总览
[组件、边界、数据流；必要时使用 Mermaid]
## 5. 组件与接口
| 组件 | 责任 | 所有数据 | 依赖 | 扩展方式 |
## 6. 数据、缓存与异步处理
## 7. 安全与合规
## 8. 可观测性与故障模式
## 9. 方案权衡与成本
## 10. 实施、迁移、灰度与回滚
## 11. 待确认问题
```

## 验证清单

- [ ] 每个关键用例都有完整数据流和失败路径
- [ ] 容量估算写明假设、单位和峰值，而非只写“高并发”
- [ ] SLO、RTO、RPO 与架构机制相互匹配
- [ ] 每个状态变更都有一致性、幂等和重试策略
- [ ] 依赖故障有超时、限流、降级或隔离方案
- [ ] 安全边界、权限模型、敏感数据和审计路径明确
- [ ] 至少比较一个替代方案，并记录接受的代价
- [ ] 事实、假设、推断和待确认项分开标记

## 简短示例

用户请求：“设计一个百万日活的图片上传服务。”

先输出容量假设、上传与异步处理数据流、对象存储与元数据分离、病毒扫描和 CDN 边界，再比较同步处理与队列化处理，最后给出分阶段上线和失败回滚方案。
