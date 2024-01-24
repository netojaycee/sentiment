from flask import Flask, jsonify, request, send_from_directory
from app.twitter_analysis import get_twitter_data, perform_sentiment_analysis
from nltk import word_tokenize
from app import app

# Assuming your React build folder is named 'build'
REACT_APP_BUILD_FOLDER = 'dist'

@app.route('/')
def serve_react_app():
    return send_from_directory(REACT_APP_BUILD_FOLDER, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(REACT_APP_BUILD_FOLDER, filename)

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

if __name__ == '__main__':
    app.run(debug=True)
