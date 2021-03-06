import ujson
from flask import Flask
from newspaper import Article
from flask import request
from flask import Response
from flask_cors import CORS
import pymysql

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

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

    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors. DictCursor)
    cur = con.cursor()

    cur.execute("INSERT INTO articles (category_id, title, body, url, source, reading_time, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW())", (
       0, title, text, url, '', 0
    ))
    con.commit()

@app.route("/goals", methods=['POST'])
def addGoalsRoute():
    name = request.get_json()['name']
    timespan = request.get_json()['timespan']
    bookmarks = request.get_json()['bookmarks']

    host = "mysql"
    user = "app"
    password = "asdasd"
    db = "app"

    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO goals (name, timespan) VALUES (%s, %s)",
        (
            name, timespan
        ))
    con.commit()

    goal_id = cur.lastrowid


    print(bookmarks)

    for article_id in bookmarks:
        cur = con.cursor()

        cur.execute(
            "INSERT INTO goal_articles (goal_id, article_id, `read`) VALUES (%s, %s, 0)",
            (
                goal_id, article_id
            ))
        con.commit()

    return "true"


@app.route("/article/get", methods=['GET'])
def list_articles():
    con = pymysql.connect(
        host=HOST, user=USER, password=PASSWORD,
        db=DB, cursorclass=pymysql.cursors.DictCursor)
    query = "SELECT id, title, url, created_at, reading_time FROM articles ORDER BY id DESC"

    cur = con.cursor()
    cur.execute(query)
    articles = cur.fetchall()

    response = ujson.dumps(articles, ensure_ascii=False)
    resp = Response(response, status=200, mimetype='application/json')

    return resp


@app.route("/goals/get", methods=['GET'])
def list_goals():
    con = pymysql.connect(
        host=HOST, user=USER, password=PASSWORD,
        db=DB, cursorclass=pymysql.cursors.DictCursor)
    query = "SELECT * FROM goals ORDER BY id DESC"

    cur = con.cursor()
    cur.execute(query)
    articles = cur.fetchall()

    response = ujson.dumps(articles, ensure_ascii=False)
    resp = Response(response, status=200, mimetype='application/json')

    return resp

@app.route("/goals/get/<id>", methods=['GET'])
def get_goal(id):
    con = pymysql.connect(
        host=HOST, user=USER, password=PASSWORD,
        db=DB, cursorclass=pymysql.cursors.DictCursor)
    query = "SELECT * FROM goals WHERE id = %s"

    cur = con.cursor()
    cur.execute(query, (id))
    bookmark = cur.fetchone()
    bookmark['bookmarks'] = get_goal_articles(id)
    response = ujson.dumps(bookmark, ensure_ascii=False)
    resp = Response(response, status=200, mimetype='application/json')

    return resp


def get_goal_articles(goal_id):
    con = pymysql.connect(
        host=HOST, user=USER, password=PASSWORD,
        db=DB, cursorclass=pymysql.cursors.DictCursor)
    query = "SELECT a.*, ga.read FROM articles a LEFT JOIN goal_articles ga ON ga.article_id = a.id WHERE ga.goal_id = %s"

    cur = con.cursor()
    cur.execute(query, (goal_id))
    articles = cur.fetchall()

    return articles

def filter_articles():
    pass


def add_tags():
    pass



def create_goal():
    pass


def count_words():
    pass


def calculate_time():
    pass


def add_article_to_goal():
    pass

@app.route("/categories", methods=['GET'])
def listCategories():
    response = ujson.dumps(getCategories(), ensure_ascii=False)

    resp = Response(response, status=200, mimetype='application/json')

    return resp

@app.route("/addCategory", methods=['POST'])
def addCategory():
    category = request.get_json()['category']

    saveCategory(category)
    response = ujson.dumps([], ensure_ascii=False)
    resp = Response(response, status=200, mimetype='application/json')

    return resp

def getCategories():
    host = "mysql"
    user = "app"
    password = "asdasd"
    db = "app"

    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()

    cur.execute("SELECT * FROM categories")

    categories = cur.fetchall()
    return categories

def saveCategory(category):
    host = "mysql"
    user = "app"
    password = "asdasd"
    db = "app"

    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()

    cur.execute(
        "INSERT INTO categories (parent_id, name) VALUES (%s, %s)",
        (
            0, category
        ))
    con.commit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
