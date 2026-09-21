import pytest
from sqlalchemy.exc import IntegrityError
from app import db
from app.models.authors import Author
from app.models.books import Book
from app.models.rooms import Room
from app.models.computers import Computer
from app.models.cloans import ComputerLoan
from app.models.loans import Loan
from app.models.users import User


@pytest.fixture
def author(app):
    author = Author(nameAuthor="Gabriel Garcia Marquez", nationalityAuthor="Colombiana")
    db.session.add(author)
    db.session.commit()
    return author


@pytest.fixture
def book(app, author):
    book = Book(titleBook="Cien anios de soledad", authorId=author.idAuthor)
    db.session.add(book)
    db.session.commit()
    return book


@pytest.fixture
def computer(app):
    computer = Computer(brandComputer="Dell", modelComputer="Latitude 5400")
    db.session.add(computer)
    db.session.commit()
    return computer


def test_author_creation(app, author):
    assert author.idAuthor is not None
    assert author.nameAuthor == "Gabriel Garcia Marquez"
    assert repr(author) == "<Author Gabriel Garcia Marquez>"


def test_book_creation_and_author_relationship(app, author, book):
    assert book.idBook is not None
    assert book.author == author
    assert author.books.count() == 1
    assert repr(book) == "<Book Cien anios de soledad>"


def test_room_creation(app):
    room = Room(name="Sala de lectura", description="Sala principal")
    db.session.add(room)
    db.session.commit()
    assert room.id is not None
    assert repr(room) == f"<Room {room.id} - Sala de lectura>"


def test_computer_creation_default_status(app, computer):
    assert computer.idComputer is not None
    assert computer.statusComputer == "Active"
    assert repr(computer) == f"<Computer {computer.idComputer} - Dell Latitude 5400>"


def test_computer_loan_creation_and_relationships(app, user, computer):
    cloan = ComputerLoan(computerId=computer.idComputer, userId=user.idUser)
    db.session.add(cloan)
    db.session.commit()

    assert cloan.idLoan is not None
    assert cloan.status == "Active"
    assert cloan.returnDate is None
    assert cloan.computer == computer
    assert cloan.user == user
    assert computer.computerLoans[0] == cloan
    assert user.computerLoansUser.count() == 1
    assert repr(cloan) == f"<ComputerLoan {cloan.idLoan} of Computer {computer.idComputer} to User {user.idUser}>"


def test_loan_creation_defaults_and_relationships(app, user, book):
    loan = Loan(bookId=book.idBook, userId=user.idUser)
    db.session.add(loan)
    db.session.commit()

    assert loan.idLoan is not None
    assert loan.fine == 0.0
    assert loan.status == "Active"
    assert loan.book == book
    assert loan.user == user
    assert book.loans.count() == 1
    assert user.loansUser.count() == 1
    assert repr(loan) == f"<Loan {loan.idLoan} of Book {book.idBook} to User {user.idUser}>"


def test_user_get_id(app, user):
    assert user.get_id() == str(user.idUser)


def test_user_nameUser_unique_constraint(app, user):
    duplicate = User(nameUser=user.nameUser, passwordUser="other_password")
    db.session.add(duplicate)
    with pytest.raises(IntegrityError):
        db.session.commit()


def test_user_generate_qr(app, user):
    qr_base64 = user.generate_qr()
    assert isinstance(qr_base64, str)
    assert len(qr_base64) > 0
