# PARTE 1
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.platypus import Spacer, Image, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import psycopg
import os

app = Flask(__name__)
app.secret_key = 'madereria_san_jose_2025_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

# ---------- Conexión PostgreSQL ----------
# Debes definir en Render / entorno local:
# DATABASE_URL = postgresql://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=require
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    """Devuelve una conexión a la DB. Recuerda cerrar conn/cur después."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL no está definida")
    conn = psycopg.connect(DATABASE_URL)
    return conn

# ------------ Decoradores ------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('login'))
        if session.get('rol') != 'administrador':
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== RUTAS DE AUTENTICACIÓN ====================
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = None
        try:
            conn = get_db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM usuarios WHERE email = %s AND activo = true", (email,))
            user = cur.fetchone()
            cur.close()
        except Exception as e:
            if conn:
                conn.close()
            flash('Error de conexión con la base de datos', 'danger')
            return render_template('login.html')
        finally:
            if conn:
                conn.close()

        if user and check_password_hash(user['password'], password):
            session.permanent = True
            session['user_id'] = user['id']
            session['nombre'] = user['nombre']
            session['rol'] = user['rol']
            flash(f'Bienvenido {user["nombre"]}', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

# ==================== DASHBOARD ====================
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        user_id = session['user_id']
        rol = session['rol']

        if rol == 'empleado':
            cur.execute("""
                SELECT COUNT(*) AS total
                FROM movimientos
                WHERE usuario_id = %s AND DATE(fecha) = CURRENT_DATE
            """, (user_id,))
            movimientos_hoy = cur.fetchone()['total']

            cur.execute("""
                SELECT m.*, p.nombre as producto_nombre, u.nombre as usuario_nombre
                FROM movimientos m
                JOIN productos p ON m.producto_id = p.id
                JOIN usuarios u ON m.usuario_id = u.id
                WHERE m.usuario_id = %s AND DATE(m.fecha) = CURRENT_DATE
                ORDER BY m.fecha DESC
                LIMIT 10
            """, (user_id,))
            ultimos_movimientos = cur.fetchall()

            cur.execute("SELECT COUNT(*) as total FROM productos WHERE activo = true")
            total_productos = cur.fetchone()['total']

            cur.execute("""
                SELECT COUNT(*) as total
                FROM productos
                WHERE stock_actual <= stock_minimo AND activo = true
            """)
            productos_stock_bajo = cur.fetchone()['total']

            cur.execute("""
                SELECT p.*, c.nombre as categoria_nombre
                FROM productos p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                WHERE p.stock_actual <= p.stock_minimo AND p.activo = true
                ORDER BY p.stock_actual ASC
                LIMIT 5
            """)
            productos_bajo_stock = cur.fetchall()

        else:
            cur.execute("SELECT COUNT(*) as total FROM productos WHERE activo = true")
            total_productos = cur.fetchone()['total']

            cur.execute("SELECT COUNT(*) as total FROM productos WHERE stock_actual <= stock_minimo AND activo = true")
            productos_stock_bajo = cur.fetchone()['total']

            cur.execute("SELECT COUNT(*) as total FROM movimientos WHERE DATE(fecha) = CURRENT_DATE")
            movimientos_hoy = cur.fetchone()['total']

            cur.execute("""
                SELECT p.*, c.nombre as categoria_nombre
                FROM productos p
                LEFT JOIN categorias c ON p.categoria_id = c.id
                WHERE p.stock_actual <= p.stock_minimo AND p.activo = true
                ORDER BY p.stock_actual ASC
                LIMIT 5
            """)
            productos_bajo_stock = cur.fetchall()

            cur.execute("""
                SELECT m.*, p.nombre as producto_nombre, u.nombre as usuario_nombre
                FROM movimientos m
                JOIN productos p ON m.producto_id = p.id
                JOIN usuarios u ON m.usuario_id = u.id
                ORDER BY m.fecha DESC
                LIMIT 10
            """)
            ultimos_movimientos = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    return render_template('dashboard.html',
                           total_productos=total_productos,
                           productos_stock_bajo=productos_stock_bajo,
                           movimientos_hoy=movimientos_hoy,
                           productos_bajo_stock=productos_bajo_stock,
                           ultimos_movimientos=ultimos_movimientos)

# PARTE 2
# ==================== PRODUCTOS ====================
@app.route('/productos')
@login_required
def productos():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""
            SELECT p.*, c.nombre as categoria_nombre, pr.nombre as proveedor_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
            WHERE p.activo = true
            ORDER BY p.nombre
        """)
        productos = cur.fetchall()

        cur.execute("SELECT * FROM categorias WHERE activo = true ORDER BY nombre")
        categorias = cur.fetchall()

        cur.execute("SELECT * FROM proveedores WHERE activo = true ORDER BY nombre")
        proveedores = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return render_template('productos.html', productos=productos, categorias=categorias, proveedores=proveedores)

@app.route('/productos/crear', methods=['POST'])
@admin_required
def crear_producto():
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    categoria_id = request.form['categoria_id']
    proveedor_id = request.form['proveedor_id']
    stock_minimo = request.form['stock_minimo']
    stock_maximo = request.form['stock_maximo']
    costo_unitario = request.form['costo_unitario']
    precio_venta = request.form['precio_venta']

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id,
                                 stock_minimo, stock_maximo, costo_unitario, precio_venta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (codigo, nombre, descripcion, categoria_id or None, proveedor_id or None,
              stock_minimo or 0, stock_maximo or None, costo_unitario or 0, precio_venta or 0))
        conn.commit()
        flash('Producto creado exitosamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al crear producto: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('productos'))

@app.route('/productos/editar/<int:id>', methods=['POST'])
def editar_producto(id):
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    descripcion = request.form.get('descripcion')
    categoria_id = request.form['categoria_id']
    proveedor_id = request.form['proveedor_id']
    stock_minimo = request.form['stock_minimo']
    stock_maximo = request.form.get('stock_maximo')
    costo_unitario = request.form['costo_unitario']
    precio_venta = request.form['precio_venta']

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE productos SET
                codigo = %s,
                nombre = %s,
                descripcion = %s,
                categoria_id = %s,
                proveedor_id = %s,
                stock_minimo = %s,
                stock_maximo = %s,
                costo_unitario = %s,
                precio_venta = %s
            WHERE id = %s
        """, (codigo, nombre, descripcion, categoria_id or None, proveedor_id or None,
              stock_minimo or 0, stock_maximo or None, costo_unitario or 0, precio_venta or 0, id))
        conn.commit()
        flash("Producto actualizado correctamente", "success")
    except Exception as e:
        conn.rollback()
        flash(f'Error al actualizar producto: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("productos"))

@app.route('/productos/eliminar/<int:id>')
@admin_required
def eliminar_producto(id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE productos SET activo = false WHERE id = %s", (id,))
        conn.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al eliminar producto: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('productos'))

# ==================== CATEGORÍAS ====================
@app.route('/categorias')
@admin_required
def categorias():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("SELECT * FROM categorias WHERE activo = true ORDER BY nombre")
        categorias = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    return render_template('categorias.html', categorias=categorias)

@app.route('/categorias/crear', methods=['POST'])
@admin_required
def crear_categoria():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        conn.commit()
        flash('Categoría creada exitosamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al crear categoría: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('categorias'))

@app.route('/categorias/editar/<int:id>', methods=['POST'])
@admin_required
def editar_categoria(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE categorias SET nombre = %s, descripcion = %s WHERE id = %s", (nombre, descripcion, id))
        conn.commit()
        flash('Categoría actualizada exitosamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al actualizar categoría: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('categorias'))

@app.route('/categorias/eliminar/<int:id>')
@admin_required
def eliminar_categoria(id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE categorias SET activo = false WHERE id = %s", (id,))
        conn.commit()
        flash('Categoría eliminada exitosamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al eliminar categoría: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('categorias'))

# ==================== PROVEEDORES ====================
@app.route('/proveedores')
@admin_required
def proveedores():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("SELECT * FROM proveedores WHERE activo = true ORDER BY nombre")
        proveedores = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    return render_template('proveedores.html', proveedores=proveedores)


# ==================== PROVEEDORES (continuación) ====================
@app.route('/proveedores/crear', methods=['POST'])
@admin_required
def crear_proveedor():
    nombre = request.form['nombre']
    contacto = request.form['contacto']
    telefono = request.form['telefono']
    email = request.form['email']

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO proveedores (nombre, contacto, telefono, email)
            VALUES (%s, %s, %s, %s)
        """, (nombre, contacto, telefono, email))
        conn.commit()
        flash('Proveedor creado exitosamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al crear proveedor: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('proveedores'))

@app.route('/proveedores/editar/<int:id>', methods=['POST'])
@admin_required
def editar_proveedor(id):
    nombre = request.form['nombre']
    contacto = request.form['contacto']
    telefono = request.form['telefono']
    email = request.form['email']

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE proveedores SET nombre=%s, contacto=%s, telefono=%s, email=%s
            WHERE id=%s
        """, (nombre, contacto, telefono, email, id))
        conn.commit()
        flash('Proveedor actualizado exitosamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al actualizar proveedor: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('proveedores'))

@app.route('/proveedores/eliminar/<int:id>')
@admin_required
def eliminar_proveedor(id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE proveedores SET activo = false WHERE id = %s", (id,))
        conn.commit()
        flash('Proveedor eliminado exitosamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al eliminar proveedor: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('proveedores'))

# ==================== ENTRADAS ====================
@app.route('/entradas')
@login_required
def entradas():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cur.execute("""
            SELECT e.*, p.nombre as producto_nombre, pr.nombre as proveedor_nombre, u.nombre as usuario_nombre
            FROM entradas e
            JOIN productos p ON e.producto_id = p.id
            JOIN proveedores pr ON e.proveedor_id = pr.id
            JOIN usuarios u ON e.usuario_id = u.id
            ORDER BY e.fecha DESC
        """)
        entradas = cur.fetchall()

        cur.execute("SELECT id, nombre FROM productos WHERE activo = true ORDER BY nombre")
        productos = cur.fetchall()

        cur.execute("SELECT id, nombre FROM proveedores WHERE activo = true ORDER BY nombre")
        proveedores = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    return render_template('entradas.html', entradas=entradas, productos=productos, proveedores=proveedores)

@app.route('/entradas/crear', methods=['POST'])
@login_required
def crear_entrada():
    producto_id = request.form['producto_id']
    proveedor_id = request.form['proveedor_id']
    cantidad = int(request.form['cantidad'])
    usuario_id = session['user_id']

    conn = get_db()
    cur = conn.cursor()
    try:
        # Registrar entrada
        cur.execute("""
            INSERT INTO entradas (producto_id, proveedor_id, cantidad, usuario_id)
            VALUES (%s, %s, %s, %s)
        """, (producto_id, proveedor_id, cantidad, usuario_id))

        # Actualizar stock
        cur.execute("""
            UPDATE productos SET stock_actual = stock_actual + %s
            WHERE id = %s
        """, (cantidad, producto_id))

        # Registrar movimiento
        cur.execute("""
            INSERT INTO movimientos (producto_id, usuario_id, tipo, cantidad)
            VALUES (%s, %s, 'entrada', %s)
        """, (producto_id, usuario_id, cantidad))

        conn.commit()
        flash('Entrada registrada correctamente', 'success')

    except Exception as e:
        conn.rollback()
        flash(f'Error al registrar entrada: {str(e)}', 'danger')

    finally:
        cur.close()
        conn.close()

    return redirect(url_for('entradas'))

# ==================== SALIDAS ====================
@app.route('/salidas')
@login_required
def salidas():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        cur.execute("""
            SELECT s.*, p.nombre as producto_nombre, u.nombre as usuario_nombre
            FROM salidas s
            JOIN productos p ON s.producto_id = p.id
            JOIN usuarios u ON s.usuario_id = u.id
            ORDER BY s.fecha DESC
        """)
        salidas = cur.fetchall()

        cur.execute("SELECT id, nombre FROM productos WHERE activo = true ORDER BY nombre")
        productos = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    return render_template('salidas.html', salidas=salidas, productos=productos)

@app.route('/salidas/crear', methods=['POST'])
@login_required
def crear_salida():
    producto_id = request.form['producto_id']
    cantidad = int(request.form['cantidad'])
    usuario_id = session['user_id']

    conn = get_db()
    cur = conn.cursor()
    try:
        # Verificar stock
        cur.execute("SELECT stock_actual FROM productos WHERE id = %s", (producto_id,))
        stock_actual = cur.fetchone()[0]

        if stock_actual < cantidad:
            flash('Stock insuficiente', 'danger')
            return redirect(url_for('salidas'))

        # Registrar salida
        cur.execute("""
            INSERT INTO salidas (producto_id, cantidad, usuario_id)
            VALUES (%s, %s, %s)
        """, (producto_id, cantidad, usuario_id))

        # Actualizar stock
        cur.execute("""
            UPDATE productos SET stock_actual = stock_actual - %s
            WHERE id = %s
        """, (cantidad, producto_id))

        # Registrar movimiento
        cur.execute("""
            INSERT INTO movimientos (producto_id, usuario_id, tipo, cantidad)
            VALUES (%s, %s, 'salida', %s)
        """, (producto_id, usuario_id, cantidad))

        conn.commit()
        flash('Salida registrada correctamente', 'success')

    except Exception as e:
        conn.rollback()
        flash(f'Error al registrar salida: {str(e)}', 'danger')

    finally:
        cur.close()
        conn.close()

    return redirect(url_for('salidas'))

# ==================== MOVIMIENTOS ====================
@app.route('/movimientos')
@login_required
def movimientos():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("""
            SELECT m.*, p.nombre AS producto_nombre, u.nombre AS usuario_nombre
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            JOIN usuarios u ON m.usuario_id = u.id
            ORDER BY m.fecha DESC
        """)
        movimientos = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return render_template('movimientos.html', movimientos=movimientos)

# ==================== USUARIOS ====================
@app.route('/usuarios')
@admin_required
def usuarios():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute("SELECT * FROM usuarios WHERE activo = true ORDER BY nombre")
        usuarios = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['POST'])
@admin_required
def crear_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    rol = request.form['rol']

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO usuarios (nombre, email, password, rol)
            VALUES (%s, %s, %s, %s)
        """, (nombre, email, password, rol))
        conn.commit()
        flash('Usuario creado correctamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al crear usuario: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('usuarios'))

@app.route('/usuarios/eliminar/<int:id>')
@admin_required
def eliminar_usuario(id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE usuarios SET activo = false WHERE id = %s", (id,))
        conn.commit()
        flash('Usuario desactivado correctamente', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error al desactivar usuario: {str(e)}', 'danger')
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('usuarios'))

# ==================== API BUSCAR PRODUCTOS (AJAX) ====================
@app.route('/api/buscar-productos')
@login_required
def api_buscar_productos():
    termino = request.args.get('q', '')

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT id, nombre, codigo, stock_actual
        FROM productos
        WHERE activo = true AND (nombre ILIKE %s OR codigo ILIKE %s)
        LIMIT 10
    """, (f"%{termino}%", f"%{termino}%"))

    productos = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(productos)

# ==================== INICIO DE LA APP ====================
if __name__ == '__main__':
    app.run(debug=True)
