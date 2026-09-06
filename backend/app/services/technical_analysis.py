import pandas as pd
import ta

def calculate_technical_indicators(data: list) -> dict:
    """
    Calculate RSI and Moving Averages for given historical price data list.
    data format: [{"close": 100.0, "high": 105.0, "low": 95.0, "volume": 1000}, ...]
    """
    if not data or len(data) < 14:
        return {"error": "Not enough data to calculate indicators (min 14 points required)."}
        
    df = pd.DataFrame(data)
    
    if 'close' not in df.columns:
        return {"error": "Missing 'close' column"}
        
    try:
        # RSI
        rsi_indicator = ta.momentum.RSIIndicator(close=df["close"], window=14)
        df["rsi"] = rsi_indicator.rsi()
        
        # Moving Averages
        sma_20 = ta.trend.SMAIndicator(close=df["close"], window=20)
        sma_50 = ta.trend.SMAIndicator(close=df["close"], window=50)
        
        df["sma_20"] = sma_20.sma_indicator()
        df["sma_50"] = sma_50.sma_indicator()
        
        latest = df.iloc[-1]
        
        return {
            "rsi_14": float(latest["rsi"]) if not pd.isna(latest["rsi"]) else None,
            "sma_20": float(latest["sma_20"]) if not pd.isna(latest["sma_20"]) else None,
            "sma_50": float(latest["sma_50"]) if not pd.isna(latest["sma_50"]) else None,
            "trend": "Bullish" if (not pd.isna(latest["sma_20"]) and not pd.isna(latest["sma_50"]) and latest["sma_20"] > latest["sma_50"]) else "Bearish"
        }
    except Exception as e:
        return {"error": str(e)}
