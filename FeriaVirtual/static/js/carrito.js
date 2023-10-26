// En carrito.js

function agregarAlCarrito() {
    const cantidad = document.getElementById("cantidadProducto").value;
    const producto = document.querySelector('.add-to-cart').getAttribute("data-product");
    const calibre = document.querySelector('.add-to-cart').getAttribute("data-calibre");
    const precio = document.querySelector('.add-to-cart').getAttribute("data-precio");
    //const img = document.querySelector('.add-to-cart').getAttribute("data-img");

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
                calibre,
                precio: parseFloat(precio),
                //img,
                cantidad: parseInt(cantidad),
                total // Agregar el campo 'total'
            });

            // Guardar el carrito actualizado en el almacenamiento local
            localStorage.setItem("carrito", JSON.stringify(carrito));
        } catch (error) {
            console.error("Error al agregar al carrito:", error);
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
        let iva = 0;

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
            // Puedes agregar lógica para calcular envío e IVA aquí si es necesario
        });


// ...


        // Actualiza los valores de subtotal, envío e IVA (en tu HTML)
        document.getElementById("subtotal").textContent = `$${subtotal.toFixed(2)}`;
        document.getElementById("envio").textContent = `$${envio.toFixed(2)}`;
        document.getElementById("iva").textContent = `$${iva.toFixed(2)}`;

        // Calcula el total (en tu HTML)
        const total = subtotal + envio + iva;
        document.getElementById("total").textContent = `$${total.toFixed(2)}`;
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
