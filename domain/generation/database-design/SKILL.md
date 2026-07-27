---
name: database-design
description: "Design a safe, query-aware database schema from business entities, access patterns, consistency needs, and operational constraints. Use whenever the user asks for database design, schema design, table modeling, ERD, indexing, query optimization, data partitioning, multi-tenancy, migration planning, backups, or relational-versus-document tradeoffs—even if they only say \"design the data model.\" Produce a reviewable schema specification before SQL execution; do not silently run migrations or modify a database."
user-invocable: true
agent_created: true
risk_level: mid
category: generation
---

# Database design（数据库设计）

把业务实体、访问模式和运营约束转换为可评审的数据库设计。关注模型、约束、查询、索引、一致性、生命周期和恢复；不执行 SQL、迁移或破坏性数据库操作。

## 使用时机

- 设计关系型、文档型或混合数据模型
- 规划表、字段、主键、外键、约束和实体关系
- 设计索引、查询路径、分区、分片或读写分离
- 评估事务、一致性、多租户、审计、保留和删除策略
- 规划 schema migration、备份恢复和数据生命周期

## 输入与边界

收集实体、字段、关系、读写比例、关键查询、数据量增长、事务边界、并发、租户隔离、合规、备份窗口和已有数据库。缺失信息先标注假设；涉及数据丢失、迁移或线上写入时，必须说明风险并等待确认。

本技能产出 schema 设计、ERD 和迁移计划（→ `retrieve-sql` 查询数据）；不直接执行 SQL 或迁移，不替代系统架构设计（→ `system-design`）。

## 流程

1. **提取实体**：区分核心实体、值对象、关联实体和派生数据。
2. **识别访问模式**：列出关键查询、排序、过滤、聚合、写入和保留需求。
3. **选择模型**：比较关系、文档、键值或混合方案，说明选择与代价。
4. **定义结构**：设计表/集合、字段类型、主键、外键、唯一性、非空和检查约束。
5. **定义关系**：明确基数、级联行为、软删除、版本和审计字段。
6. **设计索引**：按查询模式设计联合、覆盖、部分、全文或空间索引，估算写入代价。
7. **定义一致性**：说明事务边界、隔离级别、并发冲突、幂等和最终一致性补偿。
8. **处理运营**：覆盖租户隔离、分区、分片、归档、备份、恢复、监控和容量阈值。
9. **规划迁移**：给出 expand/contract、回填、校验、灰度、回滚和停机窗口。
10. **标注风险**：区分设计事实、假设、未验证查询计划和破坏性操作风险。

## 精确输出模板

```markdown
# 数据库设计：[领域 / 系统名]
## 1. 目标、范围与假设
## 2. 实体与关系
[ERD；必要时使用 Mermaid erDiagram]
## 3. Schema 规格
| 表/集合 | 字段 | 类型 | 约束 | 说明 |
## 4. 访问模式与索引
| 查询 | 频率 / 延迟 | 索引 | 代价 |
## 5. 事务与一致性
## 6. 租户、审计与生命周期
## 7. 备份、恢复与容量
## 8. 迁移、校验、灰度与回滚
## 9. 风险与待确认问题
```

## 验证清单

- [ ] 每个实体、关系和字段都有业务含义与生命周期
- [ ] 关键查询有对应索引，且说明索引写放大或存储代价
- [ ] 主键、唯一性、外键、非空和检查约束明确
- [ ] 事务边界、隔离级别、幂等和并发冲突策略明确
- [ ] 多租户、敏感字段、审计、删除和保留策略明确
- [ ] 数据量、增长率、备份恢复和容量阈值可计算
- [ ] 迁移采用可回滚步骤，不把未经确认的命令当成已执行
- [ ] 读写风险、假设与未验证的执行计划清楚标记

## 简短示例

用户请求：“设计 SaaS 订单库。”

先区分 tenant、customer、order、order_item 和 payment，按“按租户查订单、按状态分页、按订单号幂等写入”设计约束与索引，再给出 expand/contract 迁移和租户隔离策略。
