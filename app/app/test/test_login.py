def test_login_success(anon, user):
    # Enviar una solicitud POST con las credenciales correctas
    response = anon.post('/', data={
        'nameUser': user.nameUser,
        'passwordUser': 'test_password'
    }, follow_redirects=True)
    
    # Verificar que el login fue exitoso y que el usuario fue redirigido al dashboard
    assert response.status_code == 200
    assert b"Login successful!" in response.data
    
def test_login_invalid_credentials(anon):
  # Enviar una solicitud POST con credenciales incorrectas
  response = anon.post('/', data={
      'nameUser': 'wronguser',
      'passwordUser': 'wrongskdfghgpassword'
  }, follow_redirects=True)

  # Verificar que el login fue rechazado
  assert response.status_code == 200
  assert b"Invalid credentials. Please try again." in response.data
  
# test_auth.py
from flask_login import login_user

def test_login_already_authenticated(anon, user):
    # Simular un usuario autenticado
    with anon:
        with anon.session_transaction() as session:
          # Simula que el usuario está autenticado
          session['_user_id'] = str(user.idUser)
        
        # El usuario ya autenticado debería ser redirigido al dashboard
        response = anon.get('/dashboard', follow_redirects=True)
        assert response.status_code == 200
        assert b"This is your dashboard" in response.data  # Asumiendo que hay un texto "Dashboard" en la página

def test_login_clave_incorrecta(anon, user):
    response = anon.post('/', data={'nameUser': user.nameUser, 'passwordUser': 'otra'}, follow_redirects=True)
    assert b"Invalid credentials. Please try again." in response.data

def test_sin_sesion_redirige_al_login(anon):
    for ruta in ('/Book/', '/User/', '/Loan/', '/User/add'):
        response = anon.get(ruta)
        assert response.status_code == 302
        assert response.headers['Location'].startswith('/')

def test_sin_sesion_no_crea_usuarios(anon, app):
    from app.models.users import User
    anon.post('/User/add', data={'nameUser': 'intruso', 'passwordUser': 'x'})
    assert User.query.filter_by(nameUser='intruso').first() is None

def test_comando_crear_usuario(app):
    from app.models.users import User
    resultado = app.test_cli_runner().invoke(args=['crear-usuario', 'admin'], input='clave-admin\nclave-admin\n')
    assert 'Usuario admin creado.' in resultado.output
    assert User.query.filter_by(nameUser='admin').first().check_password('clave-admin')
