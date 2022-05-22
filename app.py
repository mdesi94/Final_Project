from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql


app = Flask(__name__)

app.secret_key = 'hello'
db = 'blog.db'
conn = sql.connect('blog.db')

POSTS_TABLE = """
CREATE TABLE IF NOT EXISTS posts (
  post_id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  post_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  content TEXT NOT NULL
)
"""

AUTHORS_TABLE = """
CREATE TABLE IF NOT EXISTS authors (
  author_id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_name TEXT NOT NULL
)
"""

POSTS_AUTHORS_TABLE = """
CREATE TABLE IF NOT EXISTS posts_authors (
  author_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL
)
"""

# connect to db and create tables
con = sql.connect('blog.db')
cur = conn.cursor()

cur.execute(POSTS_TABLE)
cur.execute(AUTHORS_TABLE)
cur.execute(POSTS_AUTHORS_TABLE)

con.commit()
con.close()


@app.route('/')
def home():
    con = sql.connect("blog.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    view_posts = cur.execute('''SELECT * FROM posts
                                 ORDER BY posts.post_date DESC''').fetchall()
    return render_template('home.html', posts=view_posts)


@app.route('/login', methods=['POST', 'GET'])
def login():
    con = sql.connect("blog.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    check_username = 'admin'
    check_password = 'pass1234'

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == check_username and password == check_password:
            session.clear()
            return redirect(url_for('dash'))
        elif username != check_username or password != check_password:
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard')
def dash():
    con = sql.connect("blog.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    view_posts = cur.execute('''SELECT * FROM posts
                                 ORDER BY posts.post_date DESC''').fetchall()

    return render_template('dashboard.html', posts=view_posts)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = 'admin'

        con = sql.connect("blog.db")
        cur = con.cursor()
        cur.execute("insert into posts(title,content, author) values (?,?,?)", (title,content,author))
        con.commit()
        return redirect(url_for('dash'))
    return render_template('newpost.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    con = sql.connect("blog.db")
    cur = con.cursor()
    cur.execute("DELETE from posts WHERE post_id = ?", (post_id,))
    con.commit()
    return redirect(url_for('dash'))


@app.route('/edit/<int:post_id>', methods=['POST', 'GET'])
def edit(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        con = sql.connect("blog.db")
        cur = con.cursor()
        cur.execute("update posts set title=?,content=? where post_id=?", (title, content, post_id))
        con.commit()
        return redirect(url_for('dash'))
    con = sql.connect("blog.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from posts where post_id=?", (post_id,))
    data = cur.fetchone()
    return render_template('editpost.html', datas=data)


if __name__ == '__main__':
    app.run(debug=True)

