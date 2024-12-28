from flask import Flask, render_template, jsonify
from selenium_script import scrape_trending_topics

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-scraper', methods=['GET'])
def run_scraper():
    try:
        print("Received request to run scaper")

        results = scrape_trending_topics()

        results['_id'] = str(results['_id'])

        print("Returning the following results")
        print(results)

        return jsonify(results)
    except Exception as e:
        print("Exception occurred")
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
