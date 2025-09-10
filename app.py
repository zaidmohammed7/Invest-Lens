from flask import *
from flask_bcrypt import Bcrypt
import sqlite3
from datetime import timedelta, datetime
import random

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=15)

GREETINGS = [
    {"word": "Hello", "language": "English"},
    {"word": "Hola", "language": "Spanish"},
    {"word": "Bonjour", "language": "French"},
    {"word": "Hallo", "language": "German"},
    {"word": "Ciao", "language": "Italian"},
    {"word": "Namaste", "language": "Hindi"},
    {"word": "Salaam", "language": "Persian"},
    {"word": "Zdravstvuyte", "language": "Russian"},
    {"word": "Nǐ hǎo", "language": "Chinese"},
    {"word": "Konnichiwa", "language": "Japanese"},
    {"word": "Annyeonghaseyo", "language": "Korean"},
    {"word": "Merhaba", "language": "Turkish"},
    {"word": "Sawasdee", "language": "Thai"},
    {"word": "Xin chào", "language": "Vietnamese"},
    {"word": "Olá", "language": "Portuguese"}
]


def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM credentials WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result and bcrypt.check_password_hash(result[0], password):
            session['user_id'] = user_id
            session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        greeting = random.choice(GREETINGS)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT ouser FROM order_history")
        user_list = sorted([row[0] for row in cursor.fetchall()])

        data = None
        selected_date = None
        selected_user = None

        if request.method == 'POST':
            selected_date = request.form.get('inp_date', datetime.now().strftime('%Y-%m-%d'))
            selected_user = request.form.get('inp_user', user_list[0])

            cursor.execute("""
                SELECT * FROM order_history
                WHERE ouser = ? AND odate < ?
            """, (selected_user, selected_date))
            filtered_data = cursor.fetchall()

            formatted_data = []
            for row in filtered_data:
                profit_loss = float(row['oltp']) - float(row['obp'])
                profit_loss_percent = (profit_loss / float(row['obp'])) * 100

                formatted_row = list(row)
                ltp_index = list(row.keys()).index('oltp') + 1  # Index after LTP
                formatted_row.insert(ltp_index, f"+{profit_loss:.2f}" if profit_loss > 0 else f"{profit_loss:.2f}")
                formatted_row.insert(ltp_index + 1,
                                     f"+{profit_loss_percent:.2f}%" if profit_loss_percent > 0 else f"{profit_loss_percent:.2f}%")

                if profit_loss_percent >= 10:
                    formatted_row.append('dark-green-highlight')
                elif profit_loss_percent >= 5:
                    formatted_row.append('green-highlight')
                elif profit_loss_percent <= -10:
                    formatted_row.append('dark-red-highlight')
                elif profit_loss_percent <= -5:
                    formatted_row.append('red-highlight')
                else:
                    formatted_row.append('')
                formatted_data.append(formatted_row)

            data = formatted_data

        conn.close()
        remaining_time = session.get('remaining_time', app.permanent_session_lifetime.total_seconds())

        return render_template(
            'dashboard.html',
            greeting_word=greeting["word"],
            greeting_language=greeting["language"],
            user_id=session['user_id'],
            user_list=user_list,
            selected_date=selected_date,
            selected_user=selected_user,
            data=data,
            session_timeout_ms=remaining_time * 1000
        )
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('last_activity', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route("/")
def connect():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
