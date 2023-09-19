from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def cat_img():
    domain_name = "https://cataas.com/"
    url = domain_name + "cat/says/%D0%9F%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D1%8C%D1%82%D0%B5%20%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%20%D0%BF%D0%BE%D0%B6%D0%B0%D0%BB%D1%83%D0%B9%D1%81%D1%82%D0%B0?json=true"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify({"data": domain_name + response.json()['url']})
    else:
        return jsonify({"data": "Неудалось получить изображение кота. Попробуй позже"})

if __name__ == '__main__':
    app.run(port=5000)


    