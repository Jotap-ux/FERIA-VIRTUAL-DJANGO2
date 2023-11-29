// En carrito.js

function agregarAlCarrito() {
    const cantidad = document.getElementById("cantidadProducto").value;
    const producto = document.querySelector('.add-to-cart').getAttribute("data-product");
    const calibre = document.querySelector('.add-to-cart').getAttribute("data-calibre");
    const calibreId = document.querySelector('.add-to-cart').getAttribute("data-calibre_id");
    const precio = document.querySelector('.add-to-cart').getAttribute("data-precio");
    const rut_productor = document.querySelector('.add-to-cart').getAttribute("data-rut_productor");
    const id_producto = document.querySelector('.add-to-cart').getAttribute("data-id_producto");

    // Verifica si la cantidad es un número válido
    if (!isNaN(cantidad) && cantidad > 0) {
        try {
            // Calcular el total
            const total = parseFloat(precio) * parseInt(cantidad);

            // Obtener el carrito actual desde el almacenamiento local
            const carrito = JSON.parse(localStorage.getItem("carrito")) || [];

            // Agregar el producto al carrito con el campo 'total'
            carrito.push({
                producto,
                id_producto,
                calibre,
                calibreId,
                precio: parseFloat(precio),
                rut_productor,
                cantidad: parseInt(cantidad),
                total // Agregar el campo 'total'
            });

            // Guardar el carrito actualizado en el almacenamiento local
            localStorage.setItem("carrito", JSON.stringify(carrito));
            
        } catch (error) {
            console.error("Error al agregar al carrito:", error);
            //alert('El producto se agregó al carrito!! :) ');
        }
    } else {
        // Manejar el caso en que la cantidad no sea válida
        console.error("Cantidad no válida");
    }
}


function mostrarCarrito() {
    try {
        const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
        const tableBody = document.getElementById("carrito-table-body"); // Cambia el ID según tu HTML

        // Limpia el contenido anterior de la tabla
        tableBody.innerHTML = "";

        let subtotal = 0;
        let envio = 0;
        let comision = 0; // Declarada aquí
        let iva = 0;
        let total = 0; // Declarada aquí

        // ...

        // Recorre los productos en el carrito y crea las filas de la tabla
        carrito.forEach(item => {
            //const productoImg = item.img; // Obtiene la URL de la imagen del producto como texto
            const productoNombre = item.producto;
            const productoCalibre = item.calibre;
            const productoPrecio = item.precio;
            const productoCantidad = item.cantidad;
            const productoTotal = productoPrecio * productoCantidad;

            // Crea una nueva fila de la tabla
            const row = document.createElement("tr");

            // Crea celdas para los datos del producto
            //const cellImagen = document.createElement("td");
            //const imagen = document.createElement("img");
            //imagen.src = productoImg;
            //imagen.alt = productoNombre;
            //imagen.style.width = "50px"; // Ajusta el ancho de la imagen según tus necesidades
            //cellImagen.appendChild(imagen);
            //cellImagen.classList.add("align-middle");

            const cellNombre = document.createElement("td");
            cellNombre.textContent = `${productoNombre}`;
            cellNombre.classList.add("align-middle");

            const cellCalibre = document.createElement("td");
            cellCalibre.textContent = productoCalibre;
            cellCalibre.classList.add("align-middle");

            const cellPrecio = document.createElement("td");
            cellPrecio.textContent = `$${productoPrecio}`;
            cellPrecio.classList.add("align-middle");

            const cellCantidad = document.createElement("td");
            cellCantidad.classList.add("align-middle");
            const cantidadInput = document.createElement("input");
            cantidadInput.type = "text";
            cantidadInput.value = productoCantidad;
            cantidadInput.classList.add("form-control", "form-control-sm", "bg-secondary", "border-0", "text-center");
            cellCantidad.appendChild(cantidadInput);

            const cellTotal = document.createElement("td");
            cellTotal.textContent = `$${productoTotal}`;
            cellTotal.classList.add("align-middle");

            const cellEliminar = document.createElement("td");
            const eliminarButton = document.createElement("button");
            eliminarButton.classList.add("btn", "btn-sm", "btn-danger");
            eliminarButton.innerHTML = '<i class="fa fa-times"></i>';
            cellEliminar.appendChild(eliminarButton);
            cellEliminar.classList.add("align-middle");           

            //eliminarButton.addEventListener("click", function () {
              //  eliminarDelCarrito(index);
            //});

            // Agrega las celdas a la fila
            //row.appendChild(cellImagen);
            row.appendChild(cellNombre);
            row.appendChild(cellCalibre);
            row.appendChild(cellPrecio);
            row.appendChild(cellCantidad);
            row.appendChild(cellTotal);
            row.appendChild(cellEliminar);

            // Agrega la fila a la tabla
            tableBody.appendChild(row);

            // Calcula subtotal, envío e IVA
            subtotal += productoTotal;    

        });

        // Calcula envío
        envio = 0;

        // Calcula comisión (Maipo Grande)
        comision = subtotal * 0.02; // 2% del subtotal

        // Calcula el IVA
        iva = subtotal * 0.19; // 19% del subtotal

        // Calcula el total
        total = subtotal + envio + comision + iva;


        // Actualiza los valores en el HTML
        document.getElementById("subtotal").textContent = `$${subtotal.toLocaleString('es-CL', { maximumFractionDigits: 0 })}`;
        document.getElementById("envio").textContent = `$${envio.toFixed(0)}`;
        document.getElementById("iva").textContent = `$${iva.toLocaleString('es-CL', { maximumFractionDigits: 0 })}`;
        document.getElementById("total").textContent = `$${total.toFixed(0)}`;
        document.getElementById("comision").textContent = `$${comision.toFixed(0)}`;       
        document.getElementById("total").textContent = `$${total.toLocaleString('es-CL', { maximumFractionDigits: 0 })}`;



    } catch (error) {
        console.error("Error al mostrar el carrito:", error);
    }
}

// Llama a la función para mostrar el carrito
mostrarCarrito();


function contarProductosEnCarrito() {
    try {
        // Obtén los datos del carrito desde el localStorage
        const carrito = JSON.parse(localStorage.getItem("carrito")) || [];

        let totalProductos = 0;

        // Recorre los productos en el carrito y suma las cantidades
        carrito.forEach(item => {
            totalProductos += item.cantidad;
        });

        return totalProductos;
    } catch (error) {
        console.error("Error al contar los productos en el carrito:", error);
        return 0; // En caso de error, se asume que no hay productos en el carrito.
    }
}

// Llama a la función para contar los productos en el carrito
const cantidadProductosEnCarrito = contarProductosEnCarrito();

// Actualiza el contenido del span
document.getElementById("carrito-cantidad").textContent = cantidadProductosEnCarrito;

console.log("Cantidad de productos en el carrito:", cantidadProductosEnCarrito);



/////////////////////////////////////////////////////////////////////////////////////////////////

// Llama a la función para obtener los datos de la tabla
//const datosDeTabla = obtenerDatosDeTabla();
//console.log(datosDeTabla);

// Obtiene los datos del carrito desde localStorage
//Aquí, el código intenta obtener datos del carrito almacenados en el almacenamiento local del navegador 
//bajo la clave 'carrito'. Esto supone que previamente has guardado los datos del carrito en el almacenamiento local.
// Agrega un controlador de eventos para el clic en el botón

// Hacemos referencia al botón "Realizar pedido"
const realizarPedidoButton = document.getElementById('realizar_pedido');

realizarPedidoButton.addEventListener('click', function (event) {
    // Evita la acción predeterminada del botón, que es enviar el formulario.
    event.preventDefault();

    // Obtén el carrito del almacenamiento local
    let carrito = JSON.parse(localStorage.getItem('carrito'));

    // Verifica si el carrito es un array válido
    if (Array.isArray(carrito)) {
        // Realiza la solicitud POST al servidor como lo estabas haciendo
        const csrfToken = getCookie('csrftoken');
        fetch('/carrito/', {
            method: 'POST',
            body: JSON.stringify(carrito),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            }
        })
        .then(response => response.json())
        .then(data => {
            // Maneja la respuesta del servidor si es necesario

            
        })
        .catch(error => { //el mensaje se captura como error, pero la info si se guarda en la BD :)
            console.error('Error:', error);
            alert('Su pedido se ha creado con èxito, por favor espere el termino de la subasta :)');

            // Borra el contenido del localStorage
            localStorage.removeItem('carrito');
            
            // También puedes redirigir al usuario después de borrar el localStorage si es necesario
            window.location.href = '/confirme_direccion'; // Cambia la URL de redirección según tus necesidades
        });
    } else {
        console.error("El carrito no es un array válido en localStorage.");
        alert('El carrito está vacío o no es válido. Agrega productos antes de realizar un pedido.');
    }
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Busca el nombre del token CSRF
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//PARA VALIDAR LA CANTIDAD QUE ESTAMOS AGREGANDO AL CARRITO DE COMPRAS
function validarCantidad() {
    var cantidadProducto = parseInt(document.getElementById("cantidadProducto").value);
    var stock = parseInt(document.getElementById("stock").value);

    if (isNaN(cantidadProducto) || cantidadProducto <= 0) {
        alert("Ingrese una cantidad válida.");
    } else if (cantidadProducto > stock) {
        alert("No puede ingresar una cantidad superior al stock disponible.");
    } else {
        // Si la cantidad es válida, puedes llamar a la función agregarAlCarrito() aquí.
        agregarAlCarrito();
        // Activamos el modal
        $('#modal-carrito').modal('show');
    }
}
