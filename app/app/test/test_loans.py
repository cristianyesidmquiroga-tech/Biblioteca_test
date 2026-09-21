def test_index(client):
    response = client.get('/Loan/')
    assert response.status_code == 200
    assert b"Lista de Pr" in response.data

def test_add_loan(client, user, book):
    response = client.post('/Loan/add', data={
        'bookId': book.idBook,
        'userId': user.idUser
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Lista de Pr" in response.data

def test_edit_loan(client, loan):
    response = client.post(f'/Loan/edit/{loan.idLoan}', data={
        'returnDate': '2024-01-15',
        'fine': '5.0',
        'status': 'Returned'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Lista de Pr" in response.data

def test_delete_loan(client, loan):
    response = client.get(f'/Loan/delete/{loan.idLoan}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Lista de Pr" in response.data
