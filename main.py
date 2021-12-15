"""Program that creates balance sheet"""

from flask import Flask, g, request
import sqlite3

app = Flask(__name__)


DATABASE = 'mydb.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def create_table_if_not_exists():
    cur = get_db().cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS balance_sheet (amount integer)')


def get_from_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def index():
    return 'Balance Sheet'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/balance")
def review_balance():
    cur = get_db().cursor()
    return str(cur.execute('SELECT * FROM balance_sheet').fetchall())


@app.route("/balance/add_entry")
def database_add_entry():
    create_table_if_not_exists()
    amount = request.args.get('amount')
    db = get_db()
    cur = db.cursor()
    with db:
        cur.execute('INSERT INTO balance_sheet VALUES (?)', (amount,))
    return "Success"


@app.route('/total_balance')
def get_total_sum():
    total = 0
    for entry in get_from_db('SELECT * FROM balance_sheet'):
        total += entry[0]
    return f"""Total balance: {total}"""


if __name__ == "__main__":
    app.run(debug=True, port=5000)