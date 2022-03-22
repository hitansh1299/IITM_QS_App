import json
import sqlite3
from flask import Flask, render_template, url_for, request, redirect
from utils import moods, get_time
from datetime import datetime

app = Flask(__name__, static_folder="static", static_url_path="", template_folder="templates")

userID = None


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    with sqlite3.connect('users.db') as conn:
        global userID
        try:
            print('Please login to the website')
            password = request.form['password']
            email = request.form['email']
            print(email, password)
            user_password = conn.execute('SELECT password FROM Users WHERE email = ?', (email,)).fetchone()[0]
            print(user_password)
            if password == user_password:
                userID = email
                return redirect(url_for('dashboard'))

        except TypeError:
            return redirect('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        redirect(url_for('login'))
    with sqlite3.connect('users.db') as conn:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            conn.cursor().execute('INSERT INTO Users VALUES(?,?,?)', (name, email, password))
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            # TODO Put in an error message to throw
            return redirect(url_for('signup'))
            pass


@app.route('/logs.html', methods=['GET'])
def logs():
    with sqlite3.connect('users.db') as conn:
        logs = conn.cursor().execute("SELECT * FROM Moods WHERE name = ?", (userID,)).fetchall()
        logs = [(x[0], get_time(x[1]), x[2], x[3], x[4], x[1]) for x in logs]
        print(logs)
        return render_template('logs.html', logs=logs)


@app.route('/mood.html', methods=["GET", "POST"])
@app.route('/forms.html', methods=["GET", "POST"])
def input_mood():
    if request.method == 'GET':
        return render_template('mood.html', moods=moods)
    with sqlite3.connect('users.db') as conn:
        general_mood = request.form.get("mood").split('|')[0]
        specific_mood = request.form.get("mood").split('|')[1]
        note = request.form.get("note")
        conn.cursor().execute('INSERT INTO Moods VALUES(?,?,?,?,?)',
                              (userID,
                               str(datetime.now().isoformat()),
                               general_mood,
                               specific_mood,
                               note
                               ))
    return redirect("dashboard.html")


@app.route('/edit_record.html?<timestamp>', methods=['GET', 'POST'])
def edit_record(timestamp):
    with sqlite3.connect('users.db') as conn:
        record = conn.cursor().execute("SELECT * FROM Moods WHERE name = ? and timestamp = ?",
                                       (userID, timestamp)).fetchone()
        if request.method == 'GET':
            return render_template('mood_edit.html', moods=moods, mood_picked=record[3], note=record[4],
                                   timestamp=timestamp)
        elif request.method == 'POST':
            general_mood = request.form.get("mood").split('|')[0]
            specific_mood = request.form.get("mood").split('|')[1]
            note = request.form.get("note")
            conn.cursor().execute('''UPDATE Moods 
                                    SET general=?,
                                    specific=?,
                                    note=?
                                    WHERE name=?
                                    AND timestamp=?''', (general_mood, specific_mood, note, userID, timestamp))
            return redirect(url_for('logs'))


@app.route('/delete_record/<timestamp>')
def delete_record(timestamp: str):
    with sqlite3.connect('users.db') as conn:
        conn.cursor().execute("DELETE FROM Moods WHERE timestamp=? AND name=?", (timestamp, userID))
        return redirect(url_for('logs'))


@app.route('/dashboard.html')
@app.route('/index.html')
def dashboard():
    labels = str(list(dict(moods).keys())).replace("'", '"')
    print(labels)
    with sqlite3.connect('users.db') as conn:
        records = conn.execute("SELECT * FROM Moods WHERE name = ?", (userID,)).fetchall()
        d = {}
        for i in records:
            d[i[2]] = d.get(i[2], 0) + 1
        data = [d.get(x, 0) for x in dict(moods).keys()]
        print(data)

        data2 = []
        d = {i: [] for i in range(1, 13)}
        for record in records:
            d[datetime.fromisoformat(record[1]).month].append(record)
        print(d)
        for i in d.values():
            data2.append(get_color(i))
        print("data2 ", data2)

        return render_template('dashboard.html', labels=labels, data=data, data2=data2)


def get_color(records: list[tuple]):
    print(records)
    if not records:
        return "rgba(255,255,255,0)"
    mx = (-1, -1)
    for i in dict(moods).keys():
            x = len(list(filter(lambda z: z[2] == i, records)))
            mx = (i, x) if x > mx[1] else mx
    print(mx)
    return dict(moods).get(mx[0])[1]


@app.route("/<resource_name>")
def get_resource(resource_name):
    print(resource_name)
    return render_template(resource_name)


def get_monthly_score_happiness_score():
    with sqlite3.connect('users.db') as conn:
        records = conn.execute("SELECT * FROM Moods WHERE Users = ?", (userID,)).fetchall()


if __name__ == '__main__':
    app.run()
