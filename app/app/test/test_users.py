def test_index(client):
    response = client.get('/User/')
    assert response.status_code == 200
    assert b"Usuarios" in response.data  # Asumiendo que hay un texto "Users" en la página

def test_add_user(client):
    response = client.post('/User/add', data={
        'nameUser': 'new_user',
        'passwordUser': 'new_password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Usuarios" in response.data  # Asumiendo que el nombre del usuario se muestra en la página

def test_edit_user(client, user):
    response = client.post(f'/User/edit/{user.idUser}', data={
        'nameUser': 'updated_user',
        'passwordUser': 'updated_password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"updated_user" in response.data  # Asumiendo que el nombre del usuario actualizado se muestra en la página

def test_delete_user(client, user):
    response = client.get(f'/User/delete/{user.idUser}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Usuarios" in response.data  # Asumiendo que hay un mensaje de confirmación de eliminación


def test_add_user_guarda_hash(client, app):
    from app.models.users import User
    client.post('/User/add', data={'nameUser': 'ana', 'passwordUser': 'clave-segura'})
    guardado = User.query.filter_by(nameUser='ana').first()
    assert guardado.passwordUser != 'clave-segura'
    assert guardado.check_password('clave-segura')

def test_edit_sin_clave_no_la_cambia(client, user):
    client.post(f'/User/edit/{user.idUser}', data={'nameUser': 'test_user', 'passwordUser': ''})
    assert user.check_password('test_password')

def test_listado_no_muestra_claves(client, user):
    html = client.get('/User/').data
    assert user.passwordUser.encode() not in html
