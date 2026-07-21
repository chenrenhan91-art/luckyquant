# GitHub 量化开源生态参考

> 供 Quant Skill Builder 自动推荐技术栈与过拟合检验方案时使用。

## 一、全栈交易框架

| 项目 | Stars | 许可 | 最佳场景 |
|------|-------|------|----------|
| [freqtrade/freqtrade](https://github.com/freqtrade/freqtrade) | ~50k | GPL-3.0 | 加密货币、Telegram/WebUI、FreqAI 自适应 ML |
| [vnpy/vnpy](https://github.com/vnpy/vnpy) | ~43k | MIT | A股/期货/期权实盘、CTP/XTP 等国内接口 |
| [microsoft/qlib](https://github.com/microsoft/qlib) | ~45k | MIT | ML 因子挖掘、组合优化、RD-Agent 自动化研究 |
| [mementum/backtrader](https://github.com/backtrader/backtrader) | ~22k | GPL-3.0 | 经典事件驱动回测、多品种/多周期 |
| [quantopian/zipline](https://github.com/quantopian/zipline) | ~20k | Apache-2.0 | 美股研究、Alphalens/Pyfolio 生态 |
| [polakowo/vectorbt](https://github.com/polakowo/vectorbt) | ~8k | 社区版 | 向量化回测、大规模参数扫描、Numba/Rust 加速 |

## 二、数据接口

| 项目 | Stars | 覆盖 |
|------|-------|------|
| [akfamily/akshare](https://github.com/akfamily/akshare) | ~21k | A股/港股/期货/宏观，纯 Python |
| [waditu/tushare](https://github.com/waditu/tushare) | 高活跃 | A股基本面/行情，Pro 需 token |
| [ranaroussi/yfinance](https://github.com/ranaroussi/yfinance) | ~12k+ | 美股/ETF/部分港股 |
| [ccxt/ccxt](https://github.com/ccxt/ccxt) | ~33k+ | 100+ 加密货币交易所统一 API |

## 三、技术指标

| 项目 | Stars | 说明 |
|------|-------|------|
| [TA-Lib/ta-lib-python](https://github.com/TA-Lib/ta-lib-python) | ~12k | 150+ 指标 + K线形态，C 底层 |
| [freqtrade/pandas-ta](https://github.com/freqtrade/pandas-ta) | 维护中 | 130+ 指标，Pandas 原生 |
| [xgboosted/pandas-ta-classic](https://github.com/xgboosted/pandas-ta-classic) | ~360 | 192 指标 + 62 形态，可选 TA-Lib 加速 |

## 四、因子分析与组合诊断

| 项目 | Stars | 用途 |
|------|-------|------|
| [quantopian/alphalens](https://github.com/quantopian/alphalens) | ~4.3k | Alpha 因子 IC、分位收益、换手 tear sheet |
| [quantopian/pyfolio](https://github.com/quantopian/pyfolio) | ~5k | 组合绩效与风险分析（维护较慢） |
| [ml4t/diagnostic](https://github.com/ml4t/diagnostic) | 新兴 | DSR/CPCV/SHAP 诊断、HTML tearsheet |

## 五、过拟合检验（专业级）

| 项目 | 核心方法 | 适用 |
|------|----------|------|
| [OutOfSampleLab/oos-lab](https://github.com/OutOfSampleLab/oos-lab) | DSR, PBO/CSCV, WalkForward, CPCV | 轻量研究级验证 |
| [ml4t/diagnostic](https://github.com/ml4t/diagnostic) | DSR, CPCV, RAS, FDR, HAC-IC | 完整 ML 量化流水线 |
| [DaruFinance/quant-research-framework](https://github.com/DaruFinance/quant-research-framework) | WFO + DSR/PSR/PBO + Rust 等价校验 | 严格 WFO 引擎 |
| [Aliipou/backtest-audit](https://github.com/Aliipou/backtest-audit) | DSR + PBO + MC + WalkForward → PASS/WARN/FAIL | 策略审计 verdict |
| [tommy-ca/how-to-backtest-correctly](https://github.com/tommy-ca/how-to-backtest-correctly) | Triple-Barrier, Meta-Labeling, CPCV 教程 | Lopez de Prado 方法论 |

### 过拟合检验决策阈值（行业共识）

- **PBO > 0.50**：拒绝策略（IS 最优配置 OOS 大概率失效）
- **DSR < 0.95**：Sharpe 可能由多重检验产生，不可信
- **Walk-Forward**：至少 5 折，OOS Sharpe 命中率 > 60%
- **CPCV**：替代单路径 Walk-Forward，生成数千条 OOS 路径分布
- **Purging + Embargo**：时序 CV 必须，防止标签泄漏

## 六、市场 → 框架推荐矩阵

| 市场 | 首选框架 | 数据源 | 过拟合工具 |
|------|----------|--------|------------|
| A股 | VnPy / Qlib | AKShare, TuShare | oos-lab + ml4t-diagnostic |
| 美股 | Backtrader / Zipline / VectorBT | yfinance, Alpaca | alphalens + oos-lab |
| 港股 | VnPy / AKShare | AKShare | oos-lab |
| 加密 | Freqtrade / ccxt | ccxt, exchange API | Freqtrade hyperopt + oos-lab |
| 期货 | VnPy | CTP / AKShare | quant-research-framework |
| 多因子 | Qlib | Qlib 内置 / AKShare | alphalens + ml4t-diagnostic |
| ML 信号 | Qlib / VectorBT | 自定义 | ml4t-diagnostic CPCV |
| 统计套利 | VectorBT / Backtrader | 配对数据源 | CPCV + regime audit |
| 事件驱动 | 自定义 + Backtrader | 新闻/公告 API | WalkForward + DSR |
| 高频 | VnPy C++ / 自研 | 交易所直连 | 延迟审计，非传统回测 |
