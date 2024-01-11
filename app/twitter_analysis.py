from apify_client import ApifyClient
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('stopwords')
nltk.download('punkt')

client = ApifyClient("apify_api_kN50CilImKqjOCVK5FR6vGi5nR0Yzq3Mf0r0")

# Use NLTK stopwords
stop_words = set(stopwords.words('english'))

def get_twitter_data(queries):
    run_input = {
        "queries": queries,
        "language": "en",
        "newer_than": "2017-12-01",
        "older_than": "2017-12-20"
    }

    run = client.actor("shanes/tweet-flash").call(run_input=run_input)

    results = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        results.append(item)
        
    return results
    

def perform_sentiment_analysis(text):
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    return "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"
