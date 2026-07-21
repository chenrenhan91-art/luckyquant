# 用户经验分级与路径设计

> Quant Skill Builder v0.4 — Agent-first 路由逻辑

## 产品目标

用户完成向导 → 获得 **SKILL.md + strategy-spec.yaml** → 喂给 Cursor / Codex / Claude Agent → Agent 理解完整策略 → **用户只需提供 API 密钥**即可对接交易。

## 三级经验定义

| ID | 名称 | 画像 | 核心诉求 |
|----|------|------|----------|
| `zero` | 完全零基础 | 没做过投资或只买过基金 | 固定策略 Skill + Agent 白话教学 |
| `investor` | 有投资经验，无交易体系 | 自己炒过股/币，靠感觉操作 | 高阶模板 + 细粒度 spec + 标准检验 |
| `mature` | 成熟投资经验与交易体系 | 有明确买卖规则和风控 | NL → 结构化 spec，Agent 不改核心逻辑 |

## 统一步骤（含接入配置）

所有路径在「过拟合检验」之后增加 **接入配置** 步骤：

1. 目标 IDE（Cursor / Codex / Claude / 通用）
2. 运行阶段（先回测 / 直接模拟盘 / 准备实盘）
3. 券商/交易所接口（按市场推荐，可「暂未确定」）
4. 行情数据源
5. API 备注（测试网/账号类型等）

**密钥不写入 Skill**，仅生成 `config/.env.example` 与 `config/connection.yaml`。

## 路径差异

### 完全零基础 (`zero`)

- 策略：**仅 3 个固定模板**（双均线、RSI 超卖、定投），每模板含完整 `spec`（entry/exit/position/params）
- 市场：单选，推荐 A股 或 美股
- 风险：滑块上限 3 分
- 过拟合：新手套餐锁定
- 接入：默认「先回测，通过后接 API」
- Agent：读 spec → 回测 → 白话解释 → 告知 .env 需填项

### 有投资经验无体系 (`investor`)

- 策略：**高阶模板库**（12+），含 signal_type、timeframe、universe、costs、rebalance
- 可选：策略类型、指标微调
- 导出：`strategy-spec.yaml` 含全部参数块
- Agent：按 spec 实现 → 检验 PASS → broker adapter 骨架

### 成熟体系 (`mature`)

- 策略：**自然语言表单** → 实时 YAML 预览
- spec 字段：`modules.overview/entry/exit/position/risk_execution` + `pending_clarifications`
- 过拟合：专业全检 + OOS 衰减比 ≥ 0.5
- Agent：结构化为可执行规则 → 用户确认 → 编码，**不可改核心逻辑**

## 导出物

| 文件 | 用途 |
|------|------|
| `SKILL.md` | Agent 主契约（含 Agent 指令块） |
| `strategy-spec.yaml` | 机器可读策略规格（**唯一真相源**） |
| `config/connection.yaml` | 券商/IDE/周期/运行阶段 |
| `config/markets.yaml` | 各市场交易规则 |
| `config/risk.yaml` | 风控参数 |
| `config/backtest.yaml` | 回测默认参数 |
| `AGENT_PROMPT.txt` | 一键启动 Agent 的 Prompt |
| `references/agent-integration.md` | IDE 集成说明 |

## OOS 衰减参考阈值（QuanterLab）

- OOS Sharpe / IS Sharpe > 0.7：优秀
- 0.5 - 0.7：可交易，缩小仓位
- 0.3 - 0.5：边缘有效
- < 0.3：大概率过拟合，拒绝
