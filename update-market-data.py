#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT_DIR / "market-data.json"
OUTPUT_SCRIPT_PATH = ROOT_DIR / "market-data.js"


MARKET_DEFINITIONS = [
    {
        "label": "BTC/USDT",
        "loader": lambda: load_binance_ticker("BTCUSDT", decimals=2),
    },
    {
        "label": "AAPL",
        "loader": lambda: load_yahoo_chart("AAPL", decimals=2),
    },
    {
        "label": "沪深300",
        "loader": lambda: load_sina_quote("sh000300", price_index=3, reference_index=2, decimals=2),
    },
    {
        "label": "黄金/USD",
        "loader": lambda: load_yahoo_chart("GC=F", decimals=2),
    },
    {
        "label": "NVDA",
        "loader": lambda: load_yahoo_chart("NVDA", decimals=2),
    },
    {
        "label": "ETH/USDT",
        "loader": lambda: load_binance_ticker("ETHUSDT", decimals=2),
    },
    {
        "label": "IF主力",
        "loader": lambda: load_sina_quote("nf_IF0", price_index=0, reference_index=1, decimals=1),
    },
]


def main() -> int:
    previous_data = load_previous_data()
    fallback_by_label = {item["label"]: item for item in previous_data.get("items", [])}
    items = []

    for definition in MARKET_DEFINITIONS:
        label = definition["label"]
        try:
            quote = definition["loader"]()
            items.append(build_market_item(label, quote))
        except Exception as error:  # noqa: BLE001
            fallback = fallback_by_label.get(label)
            if not fallback:
                print(f"[market-data] Failed to update {label}: {error}", file=sys.stderr)
                return 1
            stale_item = dict(fallback)
            stale_item["stale"] = True
            items.append(stale_item)
            print(
                f"[market-data] {label} update failed, keeping previous value. {error}",
                file=sys.stderr,
            )

    previous_items = previous_data.get("items", [])
    updated_at = previous_data.get("updatedAt")
    if items != previous_items or not updated_at:
        updated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    payload = {
        "updatedAt": updated_at,
        "timezone": "Asia/Shanghai",
        "items": items,
    }

    OUTPUT_PATH.write_text(f"{json.dumps(payload, ensure_ascii=False, indent=2)}\n", encoding="utf-8")
    OUTPUT_SCRIPT_PATH.write_text(
        f"window.__MARKET_TICKER_DATA__ = {json.dumps(payload, ensure_ascii=False, indent=2)};\n",
        encoding="utf-8",
    )
    print(f"[market-data] Wrote {len(items)} ticker items to {OUTPUT_PATH} and {OUTPUT_SCRIPT_PATH}")
    return 0


def load_previous_data() -> dict:
    if not OUTPUT_PATH.exists():
        return {"items": []}
    try:
        return json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"items": []}


def build_market_item(label: str, quote: dict) -> dict:
    change_percent = round(float(quote["change_percent"]), 2)
    return {
        "label": label,
        "price": quote["price"],
        "priceDisplay": format_price(float(quote["price"]), quote["decimals"]),
        "changePercent": change_percent,
        "changeDisplay": format_change(change_percent),
        "trend": get_trend(change_percent),
        "source": quote["source"],
    }


def load_binance_ticker(symbol: str, *, decimals: int) -> dict:
    data = fetch_json(f"https://data-api.binance.vision/api/v3/ticker/24hr?symbol={symbol}")
    return {
        "price": parse_required_float(data["lastPrice"], f"{symbol} lastPrice"),
        "change_percent": parse_required_float(data["priceChangePercent"], f"{symbol} priceChangePercent"),
        "decimals": decimals,
        "source": "binance",
    }


def load_yahoo_chart(symbol: str, *, decimals: int) -> dict:
    encoded_symbol = urllib.parse.quote(symbol, safe="")
    data = fetch_json(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded_symbol}?interval=1d&range=5d",
        headers={"User-Agent": "luckyquant-market-updater/1.0"},
    )
    result = data["chart"]["result"][0]
    meta = result["meta"]
    price = parse_required_float(meta["regularMarketPrice"], f"{symbol} price")
    previous_raw = meta.get("chartPreviousClose", meta.get("previousClose"))
    previous = parse_required_float(previous_raw, f"{symbol} previous close")
    return {
        "price": price,
        "change_percent": ((price - previous) / previous) * 100,
        "decimals": decimals,
        "source": "yahoo",
    }


def load_sina_quote(code: str, *, price_index: int, reference_index: int, decimals: int) -> dict:
    text = fetch_text(
        f"https://hq.sinajs.cn/list={code}",
        headers={"Referer": "https://finance.sina.com.cn"},
        encoding="gbk",
    )
    match = re.search(r'="([^"]*)"', text)
    if not match:
        raise ValueError(f"Unexpected Sina payload for {code}")

    fields = match.group(1).split(",")
    price = parse_required_float(fields[price_index], f"{code} price")
    reference = parse_required_float(fields[reference_index], f"{code} reference")

    return {
        "price": price,
        "change_percent": ((price - reference) / reference) * 100,
        "decimals": decimals,
        "source": "sina",
    }


def fetch_json(url: str, *, headers: dict | None = None) -> dict:
    return json.loads(fetch_text(url, headers=headers))


def fetch_text(url: str, *, headers: dict | None = None, encoding: str = "utf-8", timeout: int = 15) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "luckyquant-market-updater/1.0",
            **(headers or {}),
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode(encoding, errors="ignore")


def parse_required_float(value: str, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Invalid number for {label}") from error
    return number


def format_price(value: float, decimals: int) -> str:
    return f"{value:,.{decimals}f}"


def format_change(value: float) -> str:
    return f"{abs(value):.1f}%"


def get_trend(value: float) -> str:
    if abs(value) < 0.05:
        return "flat"
    return "up" if value > 0 else "down"


if __name__ == "__main__":
    raise SystemExit(main())
