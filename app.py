from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import timedelta
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
app.secret_key = 'madereria_san_jose_2025_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

# ===================== DB =====================
def get_db_connection():
    try:
        return psycopg2.connect(
            host=os.environ.get("PGHOST"),
            database=os.environ.get("PGDATABASE"),
            user=os.environ.get("PGUSER"),
            password=os.environ.get("PGPASSWORD"),
            port=os.environ.get("PGPORT")
        )
    except Exception as e:
        print("❌ Error DB:", e)
        return None

# ===================== DECORADOR =====================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ===================== HOME =====================
@app.route('/')
def home():
    return redirect(url_for('login'))

# ===================== LOGIN =====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        if not conn:
            flash("Error de conexión", "danger")
            return render_template('login.html')

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['rol'] = user['rol']
            session['nombre'] = user['nombre']
            return redirect(url_for('dashboard'))

        flash("Credenciales inválidas", "danger")

    return render_template('login.html')

# ===================== DASHBOARD =====================
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    if not conn:
        return render_template('dashboard.html', total=0, productos=[])

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT COUNT(*) as total FROM productos")
    total = cur.fetchone()['total']

    cur.execute("SELECT * FROM productos ORDER BY id DESC LIMIT 10")
    productos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('dashboard.html', total=total, productos=productos)

# ===================== USUARIOS =====================
@app.route('/usuarios')
@login_required
def usuarios():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM usuarios")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('usuarios.html', usuarios=data)

# ===================== PRODUCTOS =====================
@app.route('/productos')
@login_required
def productos():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM productos")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('productos.html', productos=data)

# ===================== LOGOUT =====================
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

# ===================== ERROR 404 =====================
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

# ===================== RUN =====================
if __name__ == "__main__":
    app.run()