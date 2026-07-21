# 交易指标目录

构建器预设指标与 AI 策略描述的对照表。括号内为中文常用名。

> 零基础提示：不必一次学完。先掌握 **均线、RSI、MACD、布林带、ATR** 五个即可开始第一个策略。

## 趋势 (Trend)

| ID | 名称 | 典型参数 | 适用风格 |
|----|------|----------|----------|
| sma | 简单移动平均 | period=20/50/200 | 趋势跟踪 |
| ema | 指数移动平均 | period=12/26 | 趋势/交叉 |
| macd | MACD | fast=12, slow=26, signal=9 | 动量趋势 |
| adx | ADX | period=14 | 趋势强度过滤 |
| supertrend | SuperTrend | period=10, mult=3 | 趋势止损 |
| ichimoku | 一目均衡 | 9/26/52 | 多维度趋势 |
| hma | Hull MA | period=16 | 低滞后趋势 |

## 动量 (Momentum)

| ID | 名称 | 典型参数 | 适用风格 |
|----|------|----------|----------|
| rsi | RSI | period=14, ob=70, os=30 | 均值回归/过滤 |
| stoch | Stochastic | k=14, d=3 | 超买超卖 |
| cci | CCI | period=20 | 极端反转 |
| roc | Rate of Change | period=12 | 动量强度 |
| williams_r | Williams %R | period=14 | 超买超卖 |
| mfi | Money Flow Index | period=14 | 量价动量 |

## 波动率 (Volatility)

| ID | 名称 | 典型参数 | 适用风格 |
|----|------|----------|----------|
| bollinger | 布林带 | period=20, std=2 | 均值回归/突破 |
| atr | ATR | period=14 | 止损/仓位 |
| keltner | Keltner Channel | period=20 | 通道突破 |
| donchian | Donchian Channel | period=20 | 突破策略 |
| hv | 历史波动率 | period=20 | 风险调整 |

## 成交量 (Volume)

| ID | 名称 | 典型参数 | 适用风格 |
|----|------|----------|----------|
| obv | OBV | - | 量价确认 |
| vwap | VWAP | - | 日内基准 |
| cmf | Chaikin Money Flow | period=20 | 资金流向 |
| ad_line | A/D Line | - | 累积派发 |

## 形态 (Pattern)

| ID | 名称 | 说明 |
|----|------|------|
| cdl_doji | 十字星 | TA-Lib 形态 |
| cdl_engulfing | 吞没形态 | 反转信号 |
| cdl_hammer | 锤子线 | 底部反转 |
| squeeze | TTM Squeeze | 波动压缩后突破 |

## 自定义组合示例

- **保守趋势**: EMA(50/200) 交叉 + ADX>25 过滤 + ATR 止损
- **均衡动量**: MACD 交叉 + RSI 过滤 + 布林带宽度
- **激进突破**: Donchian 突破 + 成交量放大 + 无止损宽追踪
