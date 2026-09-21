from app import db
from app.models.authors import Author
from app.models.books import Book
from app.models.rooms import Room
from app.models.computers import Computer
from app.models.cloans import ComputerLoan
from app.models.loans import Loan


def test_author(app):
    author = Author(nameAuthor="Gabriel Garcia Marquez", nationalityAuthor="Colombiana")
    db.session.add(author)
    db.session.commit()
    assert author.idAuthor is not None


def test_book(app):
    author = Author(nameAuthor="Gabriel Garcia Marquez", nationalityAuthor="Colombiana")
    db.session.add(author)
    db.session.commit()

    book = Book(titleBook="Cien anios de soledad", authorId=author.idAuthor)
    db.session.add(book)
    db.session.commit()
    assert book.idBook is not None
    assert book.author == author


def test_room(app):
    room = Room(name="Sala de lectura", description="Sala principal")
    db.session.add(room)
    db.session.commit()
    assert room.id is not None


def test_computer(app):
    computer = Computer(brandComputer="Dell", modelComputer="Latitude 5400")
    db.session.add(computer)
    db.session.commit()
    assert computer.idComputer is not None
    assert computer.statusComputer == "Active"


def test_computer_loan(app, user):
    computer = Computer(brandComputer="Dell", modelComputer="Latitude 5400")
    db.session.add(computer)
    db.session.commit()

    cloan = ComputerLoan(computerId=computer.idComputer, userId=user.idUser)
    db.session.add(cloan)
    db.session.commit()
    assert cloan.idLoan is not None
    assert cloan.status == "Active"


def test_loan(app, user):
    author = Author(nameAuthor="Gabriel Garcia Marquez", nationalityAuthor="Colombiana")
    db.session.add(author)
    db.session.commit()

    book = Book(titleBook="Cien anios de soledad", authorId=author.idAuthor)
    db.session.add(book)
    db.session.commit()

    loan = Loan(bookId=book.idBook, userId=user.idUser)
    db.session.add(loan)
    db.session.commit()
    assert loan.idLoan is not None
    assert loan.fine == 0.0
    assert loan.status == "Active"


def test_user(app, user):
    assert user.idUser is not None
    assert user.get_id() == str(user.idUser)
