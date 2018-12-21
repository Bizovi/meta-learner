import ujson
from flask import Flask
from newspaper import Article
from flask import request
from flask import Response
import pymysql


app = Flask(__name__)

HOST = "mysql"
USER = "app"
PASSWORD = "asdasd"
DB = "app"


@app.route("/article", methods=['POST'])
def hello():
    url = request.get_json()['url']
    parsedData = extractArticle(url)
    response = ujson.dumps(parsedData, ensure_ascii=False)

    resp = Response(response, status=200, mimetype='application/json')

    saveArticle(url, parsedData['title'], parsedData['text'])

    return resp

def extractArticle(url):
    article = Article(url)
    article.download()

    article.parse()

    # print(article.text.encode("utf-8"))
    # print(article.title.encode("utf-8"))
    # print(article.authors)
    # print(article.publish_date)
    # print(article.top_image)
    # print(article.movies)

    data = {}
    data['title'] = article.title.encode("utf-8")
    data['text'] = article.text.encode("utf-8")

    return data

def saveArticle(url, title, text):
    host = "mysql"
    user = "app"
    password = "asdasd"
    db = "app"

    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                               DictCursor)
    cur = con.cursor()

    cur.execute("INSERT INTO articles (category_id, title, body, url, source, reading_time, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW())", (
       0, title, text, url, '', 0
    ))
    con.commit()


@app.route("/article/get", methods=['GET'])
def get_articles():
    con = pymysql.connect(
        host=HOST, user=USER, password=PASSWORD,
        db=DB, cursorclass=pymysql.cursors.DictCursor)
    query = "SELECT id, title, url, created_at, reading_time FROM articles"

    cur = con.cursor()
    cur.execute(query)
    articles = cur.fetchall()
    return ujson.dumps(articles)


def filter_articles():
    pass


def add_tags():
    pass


def create_category():
    pass


def create_goal():
    pass


def count_words():
    pass


def calculate_time():
    pass


def add_article_to_goal():
    pass



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
