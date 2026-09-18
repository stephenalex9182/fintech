import yfinance as yf
import pandas as pd
from sqlalchemy.orm import Session
from .. import models

def evaluate_market_alerts(db: Session):
    """
    Evaluates all active alert rules and creates notifications if conditions are met.
    """
    rules = db.query(models.AlertRule).filter(models.AlertRule.is_active == True).all()
    if not rules:
        return {"status": "No active rules found"}

    # Group rules by symbol to minimize API calls
    symbols = list(set([r.symbol for r in rules]))
    
    try:
        data = yf.download(symbols, period="1d", group_by='ticker')
        current_prices = {}
        if len(symbols) == 1:
            current_prices[symbols[0]] = data['Close'].iloc[-1]
        else:
            for symbol in symbols:
                if symbol in data and 'Close' in data[symbol]:
                    current_prices[symbol] = data[symbol]['Close'].iloc[-1]
                elif 'Close' in data and isinstance(data.columns, pd.MultiIndex):
                    current_prices[symbol] = data['Close'][symbol].iloc[-1]
                    
        notifications_created = 0
        for rule in rules:
            price = current_prices.get(rule.symbol)
            if price is None or pd.isna(price):
                continue
                
            triggered = False
            message = ""
            
            if rule.condition == "PRICE_BELOW" and price < rule.threshold_price:
                triggered = True
                message = f"Alert: {rule.symbol} has dropped below {rule.threshold_price}. Current price: {price:.2f}"
            elif rule.condition == "PRICE_ABOVE" and price > rule.threshold_price:
                triggered = True
                message = f"Alert: {rule.symbol} has risen above {rule.threshold_price}. Current price: {price:.2f}"
                
            if triggered:
                notification = models.Notification(
                    user_id=rule.user_id,
                    message=message
                )
                db.add(notification)
                # optionally deactivate rule after it triggers
                rule.is_active = False 
                notifications_created += 1
                
        db.commit()
        return {"status": "success", "notifications_created": notifications_created}
    except Exception as e:
        return {"status": "error", "message": str(e)}
