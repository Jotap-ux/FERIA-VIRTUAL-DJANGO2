//FORMULARIO REGISGRO CLIENTE (NATURAL)
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

    //-------------------------------------------------------------
    //FORMULARIO REGISTRO DE VEHICULO
    $("#btnMostrarModalVEHICULO").click(function () {
        if (validarFormularioVEHICULO()) {
            // Muestra el primer modal solo si las validaciones son exitosas
            $('#modal-registro-vehiculo').modal('show'); 
        } else {
            // Evita el envío del formulario si la validación falla
            event.preventDefault();
        }
        //$("#modal-registro-persona").modal('hide');
              
        
    });

    $("#btnAceptar-agregadoVEHICULO").click(function () {
        // Oculta el modal
        //$("#modal-registro-persona").modal('hide');
        
        $("#miFormularioREGISTRO_TRANSPORTE").submit();
        
    });

});
   

// Función para validar el formulario CLIENTE + Contraseña
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

// Función para validar el formulario INGRESO DE VEHICULO
function validarFormularioVEHICULO() {

    var patenteRegex = /^([A-Za-z]{4}\d{2}|\d{2}[A-Za-z]{4})$/;
    var patenteInput = $("#id_patente").val();

    if (!patenteRegex.test(patenteInput)) {
        
        $('#modal-error-patente').modal('show');
        return false;
    }

    if ($("#miFormularioREGISTRO_TRANSPORTE")[0].checkValidity()) {

        return true; 

    } else {
        
        $('#modal-aviso-DATOS-VEHICULO').modal('show');   
        return false;
    }
}

