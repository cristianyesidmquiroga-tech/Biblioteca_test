def test_index(client):
    response = client.get('/cloans/')
    assert response.status_code == 200
    assert b"Lista de Pr" in response.data

def test_add_cloan(client, user, computer):
    response = client.post('/cloans/add', data={
        'computerId': computer.idComputer,
        'userId': user.idUser
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Lista de Pr" in response.data

def test_edit_cloan(client, cloan, user, computer):
    response = client.post(f'/cloans/update/{cloan.idLoan}', data={
        'computerId': computer.idComputer,
        'userId': user.idUser,
        'loanDate': '2024-01-01 00:00:00',
        'returnDate': '2024-01-15 00:00:00',
        'status': 'Returned'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Lista de Pr" in response.data

def test_delete_cloan(client, cloan):
    response = client.post(f'/cloans/delete/{cloan.idLoan}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Lista de Pr" in response.data
