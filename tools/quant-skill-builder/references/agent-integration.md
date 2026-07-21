# Agent 集成指南（Cursor / Codex / Claude Code）

> 用户通过 Quant Skill Builder 获得 SKILL.md 后，将 Skill 喂给 IDE Agent。用户只需提供 API 密钥与券商/交易所接口，Agent 负责实现策略与对接。

## 用户使用流程

1. 在构建器完成配置，下载 `SKILL.md` + `references/` + `strategy-spec.yaml`
2. 将 Skill 放入 IDE：
   - Cursor: `~/.cursor/skills/<name>/` 或 `.agents/skills/<name>/`
   - Codex / Claude Code: 项目根 `.agents/skills/` 或 CLAUDE.md 引用
3. 在对话中 @ Skill 或粘贴「AI 启动 Prompt」
4. 用户提供 `.env` 中的 API 密钥（Agent 不写入 Skill 文件）
5. Agent 按 Skill 实现代码 → 回测 → 检验 → 对接用户 API → 模拟盘 → 实盘

## Agent 必须读取的文件（按序）

1. `strategy-spec.yaml` - **唯一策略真相源**（与 SKILL.md 冲突时以 YAML 为准）
2. `SKILL.md` - Agent 主契约与读取顺序
3. `references/agent-integration.md` - 本文件
4. `references/overfitting-validation.md` - 检验门禁
5. `config/risk.yaml` + `config/connection.yaml` + `config/markets.yaml` + `config/backtest.yaml`

## Agent 职责边界

| Agent 做 | 用户做 |
|----------|--------|
| 实现策略逻辑、回测、检验 | 提供 API Key / 券商账号 |
| 编写 broker adapter 骨架 | 确认券商接口文档 |
| 模拟盘联调 | 最终实盘授权 |
| 解释每步含义（零基础） | 确认 spec 无误（成熟用户） |

## 环境变量模板（写入 config/.env.example，不提交密钥）

```bash
# 数据
TUSHARE_TOKEN=
AKSHARE_ENABLED=true

# 交易（按 connection.broker 选用）
VNPY_CTP_USER=
VNPY_CTP_PASSWORD=
BINANCE_API_KEY=
BINANCE_API_SECRET=
ALPACA_API_KEY=
ALPACA_SECRET_KEY=

# 运行模式: backtest | paper | live
TRADING_MODE=paper
```

## IDE 特定说明

### Cursor
- Skill 需 `disable-model-invocation: true`
- 用户通过 `@skill-name` 显式加载

### Codex / OpenAI
- 将 SKILL.md 内容放入 project instructions 或 `.agents/skills/`

### Claude Code
- 放入 `.claude/skills/` 或通过 CLAUDE.md 链接

## 交付检查清单（Agent 完成时）

- [ ] `strategy-spec.yaml` 与代码实现一致（entry/exit/risk/exposure/execution）
- [ ] `config/*.yaml` 与 spec 各块一致
- [ ] 回测报告 + `validation/audit.py` 输出 PASS/WARN/FAIL
- [ ] paper 模式可下单（mock 或 sandbox）
- [ ] README 说明用户如何填 `.env` 并启动
- [ ] `.gitignore` 已排除 `.env` 与密钥
