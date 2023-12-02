from rut_chile import rut_chile

# Validar RUT
print(rut_chile.is_valid_rut("12345678-9"))  # debería imprimir False
print(rut_chile.is_valid_rut("6265837-1"))   # debería imprimir True
print(rut_chile.is_valid_rut("9126251-4"))

# Obtener dígito verificador
print(rut_chile.get_verification_digit("9868503"))    # debería imprimir "0"
print(rut_chile.get_verification_digit("12667869"))   # debería imprimir "k"
print(rut_chile.get_capitalized_verification_digit("12667869"))  # debería imprimir "K"

# Formatear RUT
print(rut_chile.format_rut_with_dots("12667869k"))          # debería imprimir "12.667.869-k"
print(rut_chile.format_rut_without_dots("12667869k"))       # debería imprimir "12667869-k"
print(rut_chile.format_capitalized_rut_without_dots("12667869k"))  # debería imprimir "12667869-K"
print(rut_chile.format_capitalized_rut_with_dots("12667869k"))     # debería imprimir "12.667.869-K"