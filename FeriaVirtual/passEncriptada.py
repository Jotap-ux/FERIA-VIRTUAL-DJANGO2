import bcrypt

'''
txt = input('Ingrese contraseña :')

pwd = txt.encode('utf-8')

sal = bcrypt.gensalt()

encript = bcrypt.hashpw(pwd, sal)

print(encript)
'''
#contraseña encriptada generada...
pwd = b'$2b$12$.h6W5VLAY8SVUA.NHfF/2.QgYRI//7812q0b5wkWlVxan5WRwBS6G'

txt = bytes(input("Ingrese un texto :"), 'utf-8')

if bcrypt.checkpw(txt, pwd):
    print('La contraseña es correcta!')
else:
    print('La contraseña es incorrecta causa :( ')