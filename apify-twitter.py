# from apify_client import ApifyClient

# # # Initialize the ApifyClient with your API token
# client = ApifyClient("apify_api_WImzM6OYEuoeK4KZiFw8J5C9HfCvyR0PGdX3")
# # Prepare the Actor input
# run_input = { 
#             "queries": ["i still dy Sha, praise Jah"],
#              "language": "en",
#              "newer_than": "2023-12-01",
#              "older_than": "2023-12-31"
#              }

# # Run the Actor and wait for it to finish
# run = client.actor("shanes/tweet-flash").call(run_input=run_input)

# # Fetch and print Actor results from the run's dataset (if there are any)
# for item in client.dataset(run["defaultDatasetId"]).iterate_items():
#     print(item)

from flask import Flask, request, jsonify
from apify_client import ApifyClient
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from flask_cors import CORS 

nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'


# Initialize the ApifyClient with your API token
# client = ApifyClient("apify_api_WImzM6OYEuoeK4KZiFw8J5C9HfCvyR0PGdX3")
# client = ApifyClient("apify_api_Whhhx1LkAAhiPtZdIPJu2nXq4YxB4m1I2iRA")
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

@app.route('/search', methods=['POST'])
def fetch_twitter_data():
    data = request.get_json()
    keywords = data.get('keywords', [])
    print("Received Keywords:", keywords)

    # Tokenize and remove stopwords
    queries = [word for word in word_tokenize(" ".join(keywords)) if word.lower() not in stop_words]
    print(queries)

    results = get_twitter_data(queries)
    # print(results)

    sentiment_results = []
    for result in results:
        sentiment = perform_sentiment_analysis(result.get('text', ''))
        sentiment_results.append({'text': result.get('text', ''), 'sentiment': sentiment})

    # Save results to CSV (you can customize this part based on your requirements)

    return jsonify(sentiment_results)

if __name__ == '__main__':
    app.run(debug=True)
