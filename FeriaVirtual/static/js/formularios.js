
$(document).ready(function () {
    // Agrega el evento clic al botón que abre el modal
    $("#btnMostrarModal").click(function () {
        
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
   

// Función para validar el formulario CLIENTE
function validarFormulario() {
    // Usa el método checkValidity() del formulario para activar la validación HTML nativa
    if ($("#miFormulario")[0].checkValidity()) {

        // Adicionalmente, valida que las contraseñas coincidan
        if ($("#id_contrasena").val() !== $("#id_confirmar_contrasena").val()) {

            $('#modal-aviso-CONTRASENA').modal('show');
            return false;            
        }
        return true; // Devuelve true si la validación es exitosa

    } else {
        
        $('#modal-aviso-CAMPOS').modal('show');   
        return false;
    }
}