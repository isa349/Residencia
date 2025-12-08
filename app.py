from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file   # Funciones principales de Flask
from flask_mysqldb import MySQL                                            # Conexión a MySQL/MariaDB
from werkzeug.security import generate_password_hash, check_password_hash  # Hash y verificación de contraseñas
from functools import wraps                                                # Decoradores (ej: login_required)
from datetime import datetime, timedelta                                   # Manejo de fechas y expiración de sesión
from io import BytesIO                                                     # Crear archivos PDF en memoria

from reportlab.lib.pagesizes import letter, landscape                      # Tamaños de hoja PDF
from reportlab.lib.units import cm                                         # Unidades para PDF
from reportlab.platypus import Spacer, Image, PageBreak, Table, TableStyle, SimpleDocTemplate, Paragraph  # Componentes de PDF
from reportlab.pdfgen import canvas                                        # Generación básica de PDF
from reportlab.lib import colors                                           # Colores para PDF
from reportlab.lib.styles import getSampleStyleSheet                       # Estilos de texto para PDF

import matplotlib                            # Librería base de gráficos
matplotlib.use('Agg')                        # Evita usar interfaz gráfica (importante en servidores)
import matplotlib.pyplot as plt              # Crear gráficos (png para reportes)
from collections import Counter              # Contar elementos (útil para estadísticas)
import os                                    # Manejo de archivos y rutas

app = Flask(__name__)
app.secret_key = 'madereria_san_jose_2025_secret_key'

# ===================== EXPIRACIÓN DE SESIÓN =====================
app.permanent_session_lifetime = timedelta(minutes=30)

# ===================== CONFIGURACIÓN MySQL ======================
app.config['MYSQL_HOST'] = 'localhost'          # <--- corregido
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''               # pon tu contraseña si tienes
app.config['MYSQL_DB'] = 'madereria_almacen'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ===================== DECORADORES =====================
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


# ===================== RUTAS =====================

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE email = %s AND activo = 1", (email,))
            user = cur.fetchone()
            cur.close()
        except Exception as e:
            flash("Error al conectar con la base de datos", "danger")
            print("❌ Error en SELECT:", e)
            return render_template('login.html')

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
    cur = mysql.connection.cursor()
    user_id = session['user_id']
    rol = session['rol']

    if rol == 'empleado':
        # Solo movimientos del día del empleado
        cur.execute("""
            SELECT COUNT(*) as total 
            FROM movimientos 
            WHERE usuario_id = %s AND DATE(fecha) = CURDATE()
        """, [user_id])
        movimientos_hoy = cur.fetchone()['total']

        # Solo sus últimos movimientos
        cur.execute("""
            SELECT m.*, p.nombre as producto_nombre, u.nombre as usuario_nombre
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.usuario_id = %s AND DATE(m.fecha) = CURDATE()
            ORDER BY m.fecha DESC
            LIMIT 10
        """, [user_id])
        ultimos_movimientos = cur.fetchall()

        # Totales de productos (visibles igual)
        cur.execute("SELECT COUNT(*) as total FROM productos WHERE activo = 1")
        total_productos = cur.fetchone()['total']

        cur.execute("""
            SELECT COUNT(*) as total 
            FROM productos 
            WHERE stock_actual <= stock_minimo AND activo = 1
        """)
        productos_stock_bajo = cur.fetchone()['total']

        # Productos con bajo stock
        cur.execute("""
            SELECT p.*, c.nombre as categoria_nombre 
            FROM productos p 
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.stock_actual <= p.stock_minimo AND p.activo = 1
            ORDER BY p.stock_actual ASC
            LIMIT 5
        """)
        productos_bajo_stock = cur.fetchall()

    else:
        # Vista completa para administrador
        cur.execute("SELECT COUNT(*) as total FROM productos WHERE activo = 1")
        total_productos = cur.fetchone()['total']

        cur.execute("SELECT COUNT(*) as total FROM productos WHERE stock_actual <= stock_minimo AND activo = 1")
        productos_stock_bajo = cur.fetchone()['total']

        cur.execute("SELECT COUNT(*) as total FROM movimientos WHERE DATE(fecha) = CURDATE()")
        movimientos_hoy = cur.fetchone()['total']

        cur.execute("""
            SELECT p.*, c.nombre as categoria_nombre 
            FROM productos p 
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE p.stock_actual <= p.stock_minimo AND p.activo = 1
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

    cur.close()
    return render_template('dashboard.html', 
                         total_productos=total_productos,
                         productos_stock_bajo=productos_stock_bajo,
                         movimientos_hoy=movimientos_hoy,
                         productos_bajo_stock=productos_bajo_stock,
                         ultimos_movimientos=ultimos_movimientos)

# ==================== PRODUCTOS ====================

@app.route('/productos')
@login_required
def productos():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.*, c.nombre as categoria_nombre, pr.nombre as proveedor_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
        WHERE p.activo = 1
        ORDER BY p.nombre
    """)
    productos = cur.fetchall()
    
    cur.execute("SELECT * FROM categorias WHERE activo = 1 ORDER BY nombre")
    categorias = cur.fetchall()
    
    cur.execute("SELECT * FROM proveedores WHERE activo = 1 ORDER BY nombre")
    proveedores = cur.fetchall()
    
    cur.close()
    
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
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO productos (codigo, nombre, descripcion, categoria_id, proveedor_id, 
                                 stock_minimo, stock_maximo, costo_unitario, precio_venta)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (codigo, nombre, descripcion, categoria_id, proveedor_id, 
              stock_minimo, stock_maximo, costo_unitario, precio_venta))
        mysql.connection.commit()
        flash('Producto creado exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al crear producto: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('productos'))

@app.route('/productos/editar/<int:id>', methods=['POST'])
def editar_producto(id):
    cur = mysql.connection.cursor()

    codigo = request.form['codigo']
    nombre = request.form['nombre']
    descripcion = request.form.get('descripcion')
    categoria_id = request.form['categoria_id']
    proveedor_id = request.form['proveedor_id']
    stock_minimo = request.form['stock_minimo']
    stock_maximo = request.form.get('stock_maximo')
    costo_unitario = request.form['costo_unitario']
    precio_venta = request.form['precio_venta']

    query = """
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
    """

    values = (
        codigo, nombre, descripcion, categoria_id, proveedor_id,
        stock_minimo, stock_maximo, costo_unitario, precio_venta, id
    )

    cur.execute(query, values)
    mysql.connection.commit()

    flash("Producto actualizado correctamente", "success")
    return redirect(url_for("productos"))

@app.route('/productos/eliminar/<int:id>')
@admin_required
def eliminar_producto(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE productos SET activo = 0 WHERE id = %s", [id])
        mysql.connection.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar producto: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('productos'))

# ==================== CATEGORÍAS ====================

@app.route('/categorias')
@admin_required
def categorias():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM categorias WHERE activo = 1 ORDER BY nombre")
    categorias = cur.fetchall()
    cur.close()
    
    return render_template('categorias.html', categorias=categorias)

@app.route('/categorias/crear', methods=['POST'])
@admin_required
def crear_categoria():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        mysql.connection.commit()
        flash('Categoría creada exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al crear categoría: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('categorias'))

@app.route('/categorias/editar/<int:id>', methods=['POST'])
@admin_required
def editar_categoria(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE categorias SET nombre = %s, descripcion = %s WHERE id = %s", (nombre, descripcion, id))
        mysql.connection.commit()
        flash('Categoría actualizada exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al actualizar categoría: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('categorias'))

@app.route('/categorias/eliminar/<int:id>')
@admin_required
def eliminar_categoria(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE categorias SET activo = 0 WHERE id = %s", [id])
        mysql.connection.commit()
        flash('Categoría eliminada exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar categoría: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('categorias'))

# ==================== PROVEEDORES ====================

@app.route('/proveedores')
@admin_required
def proveedores():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM proveedores WHERE activo = 1 ORDER BY nombre")
    proveedores = cur.fetchall()
    cur.close()
    
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/proveedores/crear', methods=['POST'])
@admin_required
def crear_proveedor():
    nombre = request.form['nombre']
    contacto = request.form['contacto']
    telefono = request.form['telefono']
    email = request.form['email']
    direccion = request.form['direccion']
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO proveedores (nombre, contacto, telefono, email, direccion)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, contacto, telefono, email, direccion))
        mysql.connection.commit()
        flash('Proveedor creado exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al crear proveedor: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('proveedores'))

@app.route('/proveedores/editar/<int:id>', methods=['POST'])
@admin_required
def editar_proveedor(id):
    nombre = request.form['nombre']
    contacto = request.form['contacto']
    telefono = request.form['telefono']
    email = request.form['email']
    direccion = request.form['direccion']
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            UPDATE proveedores 
            SET nombre = %s, contacto = %s, telefono = %s, email = %s, direccion = %s
            WHERE id = %s
        """, (nombre, contacto, telefono, email, direccion, id))
        mysql.connection.commit()
        flash('Proveedor actualizado exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al actualizar proveedor: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('proveedores'))

@app.route('/proveedores/eliminar/<int:id>')
@admin_required
def eliminar_proveedor(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE proveedores SET activo = 0 WHERE id = %s", [id])
        mysql.connection.commit()
        flash('Proveedor eliminado exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al eliminar proveedor: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('proveedores'))

# ==================== MOVIMIENTOS GENERALES ====================
@app.route('/entradas')
@login_required
def entradas():
    cur = mysql.connection.cursor()
    user_id = session['user_id']
    rol = session['rol']

    # Productos activos
    cur.execute("SELECT * FROM productos WHERE activo = 1 ORDER BY nombre")
    productos = cur.fetchall()

    # Proveedores (solo necesarios para admin)
    proveedores = []
    if rol == 'administrador':
        cur.execute("SELECT * FROM proveedores WHERE activo = 1 ORDER BY nombre")
        proveedores = cur.fetchall()

    # Filtrar entradas según el rol
    if rol == 'empleado':
        cur.execute("""
            SELECT m.*, p.nombre AS producto_nombre, pr.nombre AS proveedor_nombre, u.nombre AS usuario_nombre
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            LEFT JOIN proveedores pr ON m.proveedor_id = pr.id
            JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.tipo = 'entrada'
              AND m.usuario_id = %s
              AND DATE(m.fecha) = CURDATE()
            ORDER BY m.fecha DESC
        """, [user_id])
    else:
        cur.execute("""
            SELECT m.*, p.nombre AS producto_nombre, pr.nombre AS proveedor_nombre, u.nombre AS usuario_nombre
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            LEFT JOIN proveedores pr ON m.proveedor_id = pr.id
            JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.tipo = 'entrada'
            ORDER BY m.fecha DESC
            LIMIT 50
        """)

    entradas = cur.fetchall()
    cur.close()

    return render_template(
        'entradas.html',
        productos=productos,
        proveedores=proveedores,
        entradas=entradas
    )

@app.route('/entradas/crear', methods=['POST'])
@login_required
def crear_entrada():
    producto_id = request.form.get('producto_id')
    cantidad = request.form.get('cantidad', 0)
    costo_unitario = request.form.get('costo_unitario', 0)
    proveedor_id = request.form.get('proveedor_id')
    notas = request.form.get('notas', '')
    fecha = datetime.now()

    try:
        cantidad = int(cantidad)
        costo_unitario = float(costo_unitario)
    except ValueError:
        flash("Los valores ingresados no son válidos.", "danger")
        return redirect(url_for('entradas'))

    if cantidad < 1:
        flash("La cantidad debe ser mayor o igual a 1.", "danger")
        return redirect(url_for('entradas'))

    # Si el usuario es empleado, forzamos costo_unitario y proveedor_id en 0 o None
    if session['rol'] == 'empleado':
        costo_unitario = 0
        proveedor_id = None

    cur = mysql.connection.cursor()
    try:
        # Insertar movimiento
        cur.execute("""
            INSERT INTO movimientos (tipo, producto_id, cantidad, costo_unitario,
                                    usuario_id, proveedor_id, fecha, notas)
            VALUES ('entrada', %s, %s, %s, %s, %s, %s, %s)
        """, (producto_id, cantidad, costo_unitario, session['user_id'], proveedor_id, fecha, notas))

        # Actualizar stock
        cur.execute("""
            UPDATE productos
            SET stock_actual = stock_actual + %s
            WHERE id = %s
        """, (cantidad, producto_id))

        mysql.connection.commit()
        flash('Entrada registrada exitosamente.', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al registrar la entrada: {str(e)}', 'danger')
    finally:
        cur.close()

    return redirect(url_for('entradas'))

# ==================== SALIDAS ====================

@app.route('/salidas')
@login_required
def salidas():
    cur = mysql.connection.cursor()
    user_id = session['user_id']
    rol = session['rol']

    cur.execute("SELECT * FROM productos WHERE activo = 1 AND stock_actual > 0 ORDER BY nombre")
    productos = cur.fetchall()

    if rol == 'empleado':
        cur.execute("""
            SELECT m.*, p.nombre as producto_nombre, u.nombre as usuario_nombre
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.tipo = 'salida' AND m.usuario_id = %s AND DATE(m.fecha) = CURDATE()
            ORDER BY m.fecha DESC
        """, [user_id])
    else:
        cur.execute("""
            SELECT m.*, p.nombre as producto_nombre, u.nombre as usuario_nombre
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.tipo = 'salida'
            ORDER BY m.fecha DESC
            LIMIT 50
        """)

    salidas = cur.fetchall()
    cur.close()
    return render_template('salidas.html', productos=productos, salidas=salidas)

@app.route('/salidas/crear', methods=['POST'])
@login_required
def crear_salida():
    producto_id = request.form['producto_id']
    cantidad = float(request.form['cantidad'])
    precio_unitario = request.form.get('precio_unitario', 0)
    notas = request.form.get('notas', '')
    fecha = datetime.now()
    
    cur = mysql.connection.cursor()
    try:
        # Verificar stock disponible
        cur.execute("SELECT stock_actual FROM productos WHERE id = %s", [producto_id])
        producto = cur.fetchone()
        
        if producto['stock_actual'] < cantidad:
            flash('Stock insuficiente para realizar la salida', 'danger')
            return redirect(url_for('salidas'))
        
        # Insertar movimiento
        cur.execute("""
            INSERT INTO movimientos (tipo, producto_id, cantidad, precio_unitario, 
                                   usuario_id, fecha, notas)
            VALUES ('salida', %s, %s, %s, %s, %s, %s)
        """, (producto_id, cantidad, precio_unitario, session['user_id'], fecha, notas))
        
        # Actualizar stock
        cur.execute("""
            UPDATE productos 
            SET stock_actual = stock_actual - %s 
            WHERE id = %s
        """, (cantidad, producto_id))
        
        mysql.connection.commit()
        flash('Salida registrada exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al registrar salida: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('salidas'))

# ==================== MOVIMIENTOS ====================
@app.route('/movimientos', methods=['GET'])
@login_required
def movimientos():
    cur = mysql.connection.cursor()
    user_id = session['user_id']
    rol = session['rol']

    tipo = request.args.get('tipo', '')
    fecha_inicio = request.args.get('fecha_inicio', '')
    fecha_fin = request.args.get('fecha_fin', '')
    exportar = request.args.get('exportar', '')

    base_query = """
        SELECT m.*, p.nombre AS producto_nombre,
               u.nombre AS usuario_nombre
        FROM movimientos m
        JOIN productos p ON m.producto_id = p.id
        JOIN usuarios u ON m.usuario_id = u.id
    """
    filtros = []
    params = []

    # Empleado: solo movimientos del día
    if rol == 'empleado':
        filtros.append("m.usuario_id = %s")
        params.append(user_id)
        filtros.append("DATE(m.fecha) = CURDATE()")

    # Filtrar por tipo
    if tipo:
        filtros.append("m.tipo = %s")
        params.append(tipo)

    # Admin: filtros por fechas
    if rol == 'administrador':
        if fecha_inicio:
            filtros.append("DATE(m.fecha) >= %s")
            params.append(fecha_inicio)
        if fecha_fin:
            filtros.append("DATE(m.fecha) <= %s")
            params.append(fecha_fin)

    if filtros:
        base_query += " WHERE " + " AND ".join(filtros)

    base_query += " ORDER BY m.fecha DESC"
    cur.execute(base_query, params)
    movimientos = cur.fetchall()
    cur.close()

    # =====================================================
    #                  EXPORTAR PDF
    # =====================================================
    if exportar == 'pdf':
        from reportlab.platypus import (
            SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        )
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import Image

        buffer = BytesIO()

        # Documento vertical con márgenes
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=2.5 * cm,
            rightMargin=2.5 * cm,
            topMargin=3 * cm,
            bottomMargin=3 * cm
        )

        styles = getSampleStyleSheet()
        elements = []

        # ===============================
        # ENCABEZADO
        # ===============================
        logo_path = os.path.join(app.root_path, "static/img/logo.png")

        header = Table([
            [
                Image(logo_path, width=60, height=60),
                Paragraph(
                    "<b>Reporte de Movimientos</b><br/>"
                    "Maderería San José<br/>"
                    "<font size=10>Sistema de Control de Almacén</font>",
                    styles["Normal"]
                )
            ]
        ], colWidths=[70, 400])

        header.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (1, 0), (1, 0), 15)
        ]))

        elements.append(header)
        elements.append(Spacer(1, 15))

        # ===============================
        # INFORMACIÓN DE REPORTE
        # ===============================
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

        info = f"""
        <b>Fecha:</b> {fecha_actual}<br/>
        <b>Generado por:</b> {session['nombre']} ({session['rol']})
        """

        elements.append(Paragraph(info, styles["Normal"]))
        elements.append(Spacer(1, 15))

        # ===============================
        # TABLA
        # ===============================

        encabezados = ["Tipo", "Fecha", "Producto", "Cantidad", "Costo/Precio", "Total"]
        datos = [encabezados]

        total_general = 0

        for mov in movimientos:
            tipo_texto = "Entrada" if mov['tipo'] == 'entrada' else "Salida"
            costo_precio = mov.get('costo_unitario') or mov.get('precio_unitario') or 0
            total = mov['cantidad'] * costo_precio
            total_general += total

            datos.append([
                tipo_texto,
                mov['fecha'].strftime('%d/%m/%Y %H:%M'),
                mov['producto_nombre'],
                mov['cantidad'],
                f"${costo_precio:.2f}",
                f"${total:.2f}",
            ])

        tabla = Table(datos, repeatRows=1)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))

        elements.append(tabla)
        elements.append(Spacer(1, 20))

        # ===============================
        # TOTAL GENERAL
        # ===============================
        total_paragraph = Paragraph(
            f"<b>Total General:</b> ${total_general:.2f}",
            styles["Title"]
        )

        elements.append(total_paragraph)
        elements.append(Spacer(1, 30))

        # ===============================
        # FIRMAS
        # ===============================
        firmas = Table([
            ["__________________________", "__________________________"],
            [session["nombre"], "Jefe de Almacén"]
        ], colWidths=[250, 250])

        firmas.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
        ]))

        elements.append(firmas)

        # Construir PDF
        doc.build(elements)

        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name="reporte_movimientos.pdf",
            mimetype="application/pdf"
        )

    # Render normal si no se exporta PDF
    return render_template('movimientos.html', movimientos=movimientos)



# ==================== USUARIOS ====================

@app.route('/usuarios')
@admin_required
def usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios ORDER BY nombre")
    usuarios = cur.fetchall()
    cur.close()
    
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['POST'])
@admin_required
def crear_usuario():
    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    rol = request.form['rol']
    
    password_hash = generate_password_hash(password)
    
    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO usuarios (nombre, email, password, rol)
            VALUES (%s, %s, %s, %s)
        """, (nombre, email, password_hash, rol))
        mysql.connection.commit()
        flash('Usuario creado exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al crear usuario: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('usuarios'))

@app.route('/usuarios/editar/<int:id>', methods=['POST'])
@admin_required
def editar_usuario(id):
    nombre = request.form['nombre']
    email = request.form['email']
    rol = request.form['rol']
    password = request.form.get('password', '')
    
    cur = mysql.connection.cursor()
    try:
        if password:
            password_hash = generate_password_hash(password)
            cur.execute("""
                UPDATE usuarios 
                SET nombre = %s, email = %s, rol = %s, password = %s
                WHERE id = %s
            """, (nombre, email, rol, password_hash, id))
        else:
            cur.execute("""
                UPDATE usuarios 
                SET nombre = %s, email = %s, rol = %s
                WHERE id = %s
            """, (nombre, email, rol, id))
        
        mysql.connection.commit()
        flash('Usuario actualizado exitosamente', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al actualizar usuario: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('usuarios'))

@app.route('/usuarios/toggle/<int:id>')
@admin_required
def toggle_usuario(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE usuarios SET activo = NOT activo WHERE id = %s", [id])
        mysql.connection.commit()
        flash('Estado del usuario actualizado', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error al actualizar usuario: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('usuarios'))

# ==================== API ENDPOINTS ====================

@app.route('/api/producto/<int:id>')
@login_required
def api_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", [id])
    producto = cur.fetchone()
    cur.close()
    
    return jsonify(producto)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)