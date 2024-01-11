from flask import jsonify, request
from app.twitter_analysis import get_twitter_data, perform_sentiment_analysis
from app import app

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/search', methods=['POST'])
def fetch_twitter_data():
    data = request.get_json()
    keywords = data.get('keywords', [])
    print("Received Keywords:", keywords)

    # Tokenize and remove stopwords
    queries = [word for word in word_tokenize(" ".join(keywords)) if word.lower() not in stop_words]
    print(queries)

    results = get_twitter_data(queries)

    sentiment_results = []
    for result in results:
        sentiment = perform_sentiment_analysis(result.get('text', ''))
        sentiment_results.append({'text': result.get('text', ''), 'sentiment': sentiment})

    return jsonify(sentiment_results)
