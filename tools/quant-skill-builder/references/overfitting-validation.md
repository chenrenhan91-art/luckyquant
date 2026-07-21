# 过拟合检验工作流

## 白话版（零基础必读）

**过拟合是什么？** 你的策略在历史数据上表现很好，只是因为「记住了答案」，未来会失效。

**怎么防？** 三步：
1. **留考试题**：用一部分从没参与调参的数据做最终验证（样本外 OOS）
2. **反复考**：不只做一次验证，而是滚动多次（Walk-Forward）
3. **算概率**：用 DSR/PBO 判断「好看的成绩是不是运气」

**新手简化版门禁**（构建器「新手模式」默认）：
- 回测至少 2 年数据
- Walk-Forward 5 折，至少 60% 的折 OOS 盈利
- DSR > 0.95，PBO < 0.50
- 全部通过 → 才能进模拟盘

---

AI 在实现用户量化系统时，必须将此清单作为强制门禁，不可跳过。

## Phase 1: 数据完整性

- [ ] 确认无未来函数（lookahead bias）
- [ ] 确认无 survivorship bias（退市/摘牌处理）
- [ ] 时序 CV 使用 Purging（清除重叠标签）+ Embargo（测试集前禁运期）
- [ ] 交易成本：佣金 + 滑点 + 冲击成本（按市场微观结构设定）
- [ ] A股 T+1、涨跌停、停牌规则已建模

## Phase 2: 样本外验证

### Walk-Forward Optimization (WFO)

```
训练窗口 → 测试窗口 → 滚动
推荐: train=252d, test=63d, purge=21d, n_splits≥5
```

### Combinatorial Purged CV (CPCV)

替代单路径 WFO，枚举 C(S, S/2) 种 train/test 分割，输出 OOS 分布而非单点估计。

## Phase 3: 统计显著性

| 指标 | 公式来源 | 通过阈值 |
|------|----------|----------|
| Probabilistic Sharpe Ratio (PSR) | Bailey & Lopez de Prado | PSR > 0.95 |
| Deflated Sharpe Ratio (DSR) | 多重检验校正 | DSR > 0.95 |
| Probability of Backtest Overfitting (PBO) | CSCV | PBO < 0.50 |
| Min Track Record Length (MinTRL) | 所需最小样本量 | 实际数据 ≥ MinTRL |
| Information Coefficient (IC) | Alphalens | IC mean > 0.02, IC IR > 0.5 |

## Phase 4: 稳健性压力测试

- [ ] 参数敏感性：±20% 参数扰动，Sharpe 衰减 < 30%
- [ ] 子样本：牛市/熊市/震荡市分段表现
- [ ] 蒙特卡洛置换检验：p-value < 0.05
- [ ] 不同随机种子 / 不同起始日期

## Phase 5: Verdict

```
PASS  → 可进入模拟盘
WARN  → 缩小仓位，继续 OOS 观察
FAIL  → 拒绝上线，回到策略设计
```

### OOS 衰减比（成熟用户必检）

- OOS Sharpe / IS Sharpe > **0.7**：优秀
- **0.5 - 0.7**：可交易，缩小仓位
- **0.3 - 0.5**：边缘有效
- **< 0.3**：大概率过拟合，拒绝

参考: [QuanterLab WFO Cookbook](https://quanterlab.com/articles/cookbook-backtest-to-walkforward)

参考实现: `oos-lab`, `ml4t-diagnostic`, `backtest-audit`
