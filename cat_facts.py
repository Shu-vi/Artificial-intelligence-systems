from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def cat_facts():
    url = 'https://catfact.ninja/fact'
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify({"data": response.json()['fact']})
    else:
        return jsonify({"data": "Неудалось получить факт о коте. Попробуйте позже"})

if __name__ == '__main__':
    app.run(port=5001)