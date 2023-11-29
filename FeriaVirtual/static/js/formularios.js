
$(document).ready(function () {
    // Agrega el evento clic al botón que abre el modal
    $("#btnMostrarModal").click(function () {
        // Muestra el modal
        //$("#modal-registro-persona").modal('show');
        // Valida el formulario antes de enviarlo
        if (validarFormulario()) {
            // Muestra el primer modal solo si las validaciones son exitosas
            $("#modal-registro-persona").modal('show');
        } else {
            // Evita el envío del formulario si la validación falla
            event.preventDefault();
        }
    });

    // Agrega el evento clic al botón de aceptar dentro del modal
    $("#btnAceptar").click(function () {
        
        //$("#modal-registro-persona").modal('hide');
        $('#modal-aviso').modal('show');        
        
    });

    // Agrega el evento clic al botón de aceptar dentro del modal
    $("#btnAceptar2").click(function () {
        // Oculta el modal
        //$("#modal-registro-persona").modal('hide');
        
        $("#miFormulario").submit();
        
    });
});
   

// Función para validar el formulario
function validarFormulario() {
    // Usa el método checkValidity() del formulario para activar la validación HTML nativa
    if ($("#miFormulario")[0].checkValidity()) {
        return true; // Devuelve true si la validación es exitosa
    } else {
        // Muestra un mensaje de error si la validación falla
        //alert("Por favor, complete correctamente todos los campos obligatorios.");
        $('#modal-aviso-CAMPOS').modal('show');   
        return false;
    }
}