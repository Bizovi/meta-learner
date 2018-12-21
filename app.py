from flask import Flask
from newspaper import Article
from flask import request
import ujson
from flask import Response


app = Flask(__name__)

@app.route("/article", methods=['POST'])
def hello():
    url = request.get_json()['url']
    parsedData = extractArticle(url)
    response = ujson.dumps(parsedData, ensure_ascii=False)

    resp = Response(response, status=200, mimetype='application/json')

    return resp


    # return json.dumps(extractArticle(url))

def extractArticle(url):
    article = Article(url)
    article.download()

    article.parse()

    print(article.title.encode("utf-8"))
    # print(article.authors)
    # print(article.publish_date)
    print(article.text.encode("utf-8"))
    # print(article.top_image)
    # print(article.movies)
    data = {}
    data['title'] = article.title.encode("utf-8")
    data['text'] = article.text.encode("utf-8")

    return data

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)