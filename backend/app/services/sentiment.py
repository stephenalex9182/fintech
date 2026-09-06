from transformers import pipeline
import logging

# Initialize lazy-loaded pipeline to avoid massive memory usage on boot
_sentiment_pipeline = None

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        try:
            # Using a relatively lightweight financial sentiment model
            _sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
        except Exception as e:
            logging.error(f"Failed to load sentiment model: {e}")
            return None
    return _sentiment_pipeline

def analyze_sentiment(texts: list[str]) -> list[dict]:
    """Analyze sentiment of financial news or texts."""
    pipe = get_sentiment_pipeline()
    if not pipe:
        return [{"error": "Model not loaded"}] * len(texts)
    
    try:
        results = pipe(texts)
        return results
    except Exception as e:
        logging.error(f"Error during sentiment analysis: {e}")
        return [{"error": str(e)}] * len(texts)
