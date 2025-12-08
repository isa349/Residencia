// Función para formatear números como moneda
function formatCurrency(value) {
  return new Intl.NumberFormat("es-MX", {
    style: "currency",
    currency: "MXN",
  }).format(value)
}

// Función para formatear fechas
function formatDate(dateString) {
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }
  return new Date(dateString).toLocaleDateString("es-MX", options)
}

// Confirmar eliminación
function confirmarEliminacion(mensaje) {
  return confirm(mensaje || "¿Está seguro de que desea eliminar este elemento?")
}

// Cargar datos de producto para editar
async function editarProducto(id) {
  try {
    const response = await fetch(`/api/producto/${id}`)
    const producto = await response.json()

    // Llenar el formulario de edición con los datos
    document.getElementById("edit_producto_id").value = producto.id
    document.getElementById("edit_nombre").value = producto.nombre
    document.getElementById("edit_descripcion").value = producto.descripcion || ""
    document.getElementById("edit_categoria_id").value = producto.categoria_id
    document.getElementById("edit_proveedor_id").value = producto.proveedor_id
    document.getElementById("edit_stock_minimo").value = producto.stock_minimo
    document.getElementById("edit_stock_maximo").value = producto.stock_maximo || ""
    document.getElementById("edit_costo_unitario").value = producto.costo_unitario
    document.getElementById("edit_precio_venta").value = producto.precio_venta

    // Mostrar el modal
    const modal = new window.bootstrap.Modal(document.getElementById("modalEditarProducto"))
    modal.show()
  } catch (error) {
    console.error("Error al cargar producto:", error)
    alert("Error al cargar los datos del producto")
  }
}

// Validar stock antes de registrar salida
function validarStock(productoId, cantidadInput) {
  const cantidad = Number.parseFloat(cantidadInput.value)

  fetch(`/api/producto/${productoId}`)
    .then((response) => response.json())
    .then((producto) => {
      if (cantidad > producto.stock_actual) {
        alert(`Stock insuficiente. Disponible: ${producto.stock_actual}`)
        cantidadInput.value = producto.stock_actual
      }
    })
    .catch((error) => {
      console.error("Error al validar stock:", error)
    })
}

// Inicializar tooltips de Bootstrap
document.addEventListener("DOMContentLoaded", () => {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map((tooltipTriggerEl) => new window.bootstrap.Tooltip(tooltipTriggerEl))
})

// Auto-cerrar alertas después de 5 segundos
document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)")
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new window.bootstrap.Alert(alert)
      bsAlert.close()
    }, 5000)
  })
})

// Búsqueda en tablas
function filtrarTabla(inputId, tablaId) {
  const input = document.getElementById(inputId)
  const filter = input.value.toUpperCase()
  const table = document.getElementById(tablaId)
  const tr = table.getElementsByTagName("tr")

  for (let i = 1; i < tr.length; i++) {
    const txtValue = tr[i].textContent || tr[i].innerText
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      tr[i].style.display = ""
    } else {
      tr[i].style.display = "none"
    }
  }
}

// Calcular total en formularios
function calcularTotal(cantidadId, precioId, totalId) {
  const cantidad = Number.parseFloat(document.getElementById(cantidadId).value) || 0
  const precio = Number.parseFloat(document.getElementById(precioId).value) || 0
  const total = cantidad * precio

  document.getElementById(totalId).textContent = formatCurrency(total)
}

// Prevenir envío de formulario con Enter (excepto en textareas)
document.addEventListener("DOMContentLoaded", () => {
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && e.target.tagName !== "TEXTAREA") {
        e.preventDefault()
        return false
      }
    })
  })
})

/* ---------------------------------------------------------------------------
   NUEVO: Filtro por fecha y scroll en "Últimos Movimientos"
--------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const fechaFiltro = document.getElementById("fechaFiltro")
  const tabla = document.getElementById("tablaMovimientos")

  if (fechaFiltro && tabla) {
    const picker = flatpickr(fechaFiltro, {
      dateFormat: "Y-m-d",
      defaultDate: new Date(),
      onChange: (selectedDates, dateStr) => filtrarPorFecha(dateStr),
    })

    function filtrarPorFecha(fecha) {
      const filas = tabla.querySelectorAll("tbody tr")
      let visibles = 0
      filas.forEach((fila) => {
        const fechaMovimiento = fila.dataset.fecha
        if (fechaMovimiento === fecha) {
          if (visibles < 3) {
            fila.style.display = ""
          } else {
            fila.style.display = ""
          }
          visibles++
        } else {
          fila.style.display = "none"
        }
      })
    }

    // Mostrar solo los de hoy al cargar
    const hoy = new Date().toISOString().split("T")[0]
    filtrarPorFecha(hoy)
  }
})