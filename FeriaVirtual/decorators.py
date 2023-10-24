from django.http import HttpResponse
from functools import wraps


#ACÁ GESTIONAMOS QUE SI EXISTE USER_INFO EN LA SESIÓN SE ME PERMITE EL ACCESO A LA VISTA 
#DE LO CONTRARIO SE MUESTRA UN MENSAJE DE ERROR..

#Luego el decorators lo aplicamos en las vistas que deseamos proteger en nuestro caso, son
#las vistas privadas de cada usuario, ya que ahi estan sus datos personales y etc.
def user_info_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_info' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Usted no está logueado, por tanto no puede acceder a esta página", status=401)  # Puedes personalizar el mensaje y el código de estado según tus necesidades
    return _wrapped_view
