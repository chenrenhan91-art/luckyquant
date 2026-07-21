---
name: {{SKILL_NAME}}
description: >-
  {{SKILL_DESCRIPTION}}
disable-model-invocation: true
---

# {{PROJECT_NAME}} 量化交易系统

> 由 Quant Skill Builder 生成 | 市场: {{MARKETS}} | 风险偏好: {{RISK_LABEL}} ({{RISK_SCORE}}/5)

## 系统概要

{{SYSTEM_SUMMARY}}

## 开发约束（AI 必须遵守）

1. **阶段门禁**: 回测 PASS → 模拟盘 → 小仓位实盘，不可跳阶段
2. **过拟合检验**: 实现前读取 [overfitting-validation.md](references/overfitting-validation.md)，DSR/PBO/WFO 未通过禁止上线
3. **无未来函数**: 所有信号基于 t 时刻及之前数据，严格 no-lookahead
4. **交易成本**: 必须建模 {{COMMISSION_MODEL}}
5. **语言**: 代码注释与文档以中文为主

## 市场配置

| 维度 | 设定 |
|------|------|
| 目标市场 | {{MARKETS}} |
| 交易频率 | {{FREQUENCY}} |
| 持仓周期 | {{HOLDING_PERIOD}} |
| 最大回撤容忍 | {{MAX_DRAWDOWN}} |
| 单票/单合约上限 | {{POSITION_LIMIT}} |

## 风险偏好映射 ({{RISK_SCORE}}/5 - {{RISK_LABEL}})

{{RISK_PROFILE_DETAIL}}

## 技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| 核心框架 | {{FRAMEWORK}} | {{FRAMEWORK_REASON}} |
| 数据源 | {{DATA_SOURCES}} | 市场匹配 |
| 指标库 | {{INDICATOR_LIB}} | {{INDICATOR_LIB_REASON}} |
| 过拟合检验 | {{VALIDATION_LIBS}} | 研究级统计验证 |
| 因子分析 | {{FACTOR_LIB}} | 策略类型匹配 |

## 策略规格

### 策略类型
{{STRATEGY_TYPES}}

### 入场规则
{{ENTRY_RULES}}

### 出场规则
{{EXIT_RULES}}

### 仓位管理
{{POSITION_SIZING}}

### 风控规则
{{RISK_CONTROLS}}

## 过拟合检验流水线

```
数据准备 → Purged CV 分割 → 回测 → WFO/CPCV → DSR/PSR/PBO → Verdict
```

必检项见 [overfitting-validation.md](references/overfitting-validation.md)。

阈值:
- DSR > 0.95
- PBO < 0.50
- WFO OOS Sharpe 命中率 > 60%

## 项目结构

```
{{PROJECT_NAME}}/
├── config/
│   ├── markets.yaml          # 市场与交易规则
│   ├── risk.yaml             # 风控参数
│   └── backtest.yaml         # 回测配置
├── data/
│   ├── fetchers/             # 数据获取
│   └── processors/           # 清洗/复权/对齐
├── strategies/
│   └── {{STRATEGY_MODULE}}.py
├── indicators/
│   └── custom.py             # 自定义指标
├── backtest/
│   ├── engine.py             # 回测引擎封装
│   └── reports/              # 报告输出
├── validation/
│   ├── walk_forward.py       # WFO
│   ├── cpcv.py               # CPCV 分割
│   ├── deflated_sharpe.py    # DSR/PSR
│   └── audit.py              # PASS/WARN/FAIL
├── paper/                    # 模拟盘
├── live/                     # 实盘（门禁后）
├── tests/
├── requirements.txt
└── README.md
```

## AI 开发工作流

### Step 1: 环境搭建
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Step 2: 数据管道
实现 `data/fetchers/` 对接 {{DATA_SOURCES}}，处理 {{MARKET_SPECIFIC_RULES}}。

### Step 3: 策略实现
在 `strategies/{{STRATEGY_MODULE}}.py` 实现上述入场/出场/仓位规则。

### Step 4: 回测
运行回测，输出 Sharpe、MaxDD、Calmar、Win Rate、Turnover。

### Step 5: 过拟合审计
运行 `validation/audit.py`，未 PASS 则迭代策略。

### Step 6: 模拟盘
对接 {{PAPER_TRADING_API}}，小资金验证滑点与延迟。

### Step 7: 实盘
仅 audit PASS + 模拟盘稳定 {{PAPER_MIN_DAYS}} 天后启用。

## 自然语言需求（用户原始描述）

{{NL_DESCRIPTION}}

## AI 需反问用户的开放项

{{CLARIFICATION_QUESTIONS}}

## 零基础学习支持

AI 与用户沟通时：
1. 优先使用 [glossary.md](references/glossary.md) 中的白话术语
2. 按 [beginner-learning-path.md](references/beginner-learning-path.md) 当前阶段推进，不可跳步
3. 策略逻辑参考 [strategy-templates.md](references/strategy-templates.md) 中选定模板

{{BEGINNER_NOTES}}

## 参考资源

- [策略模板库](references/strategy-templates.md)
- [术语白话词典](references/glossary.md)
- [零基础学习路径](references/beginner-learning-path.md)
- [GitHub 量化生态](references/github-landscape.md)
- [过拟合检验清单](references/overfitting-validation.md)
- [指标目录](references/indicator-catalog.md)
