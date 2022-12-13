import os
import sqlalchemy as db
from sqlalchemy import Integer, String, Column, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from gen import generate_password
from cripto import Crypt

APP_PATH = os.path.dirname(__file__)
engine = db.create_engine(f"sqlite:///{os.path.join(APP_PATH, 'pwd-buddy.db')}")
connection = engine.connect()
Base = declarative_base(metadata=MetaData(engine))


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(30), nullable=False)
    password = Column(String(200), nullable=False, unique=True)

    def __repr__(self):
        return "<Account(name='%s', email='%s', password='%s'>" % (self.name, self.email, self.password)


if not engine.dialect.has_table(connection, 'accounts'):
    Account.metadata.create_all()


def create_account_csv(name: str, email: str, password: str) -> list[list[Column]] | bool:
    with Session(engine) as session:
        try:
            account = Account(name=name, email=email, password=password)
            session.add(account)
            session.commit()
            result = session.query(Account).filter(
                Account.name == name and
                Account.email == email).order_by(db.desc(Account.id)).first()
            if result:
                return [[result.id, result.name, result.email, result.password]]
            return False
        except SQLAlchemyError as e:
            return False


def create_account(name: str, email: str) -> list[list[Column]] | bool:
    crypto = Crypt(APP_PATH)
    pwd = generate_password()
    pwd = crypto.encrypt_text(pwd)
    with Session(engine) as session:
        try:
            account = Account(name=name, email=email, password=pwd)
            session.add(account)
            session.commit()
            result = session.query(Account).filter(
                Account.name == name and
                Account.email == email).order_by(db.desc(Account.id)).first()
            if result:
                dec = crypto.decrypt_text(str(result.password))
                return [[result.id, result.name, result.email, dec]]
            return False
        except SQLAlchemyError as e:
            return False


def get_all_accounts() -> list[list[Column]] | bool:
    crypto = Crypt(APP_PATH)
    with Session(engine) as session:
        try:
            results = session.query(Account).all()
            data = []
            for index, result in enumerate(results):
                dec = crypto.decrypt_text(str(result.password))
                data.append([result.id, result.name, result.email, dec])
            return data
        except SQLAlchemyError:
            return False


def get_all_accounts_to_export() -> list[list[Column]] | bool:
    with Session(engine) as session:
        try:
            results = session.query(Account).all()
            data = []
            for index, result in enumerate(results):
                data.append([result.id, result.name, result.email, result.password])
            return data
        except SQLAlchemyError:
            return False


def get_account(name: str) -> list[list[Column]] | bool:
    crypto = Crypt(APP_PATH)
    with Session(engine) as session:
        try:
            results = session.query(Account).filter_by(name=name).all()
            data = []
            for index, result in enumerate(results):
                dec = crypto.decrypt_text(str(result.password))
                data.append([result.id, result.name, result.email, dec])
            return data
        except SQLAlchemyError as e:
            print(e.args)
            return False


def delete_account(name: str, email: str) -> list[list[Column]] | bool:
    with Session(engine) as session:
        try:
            account = get_account(name)
            result = session.query(Account).filter(
                Account.name == name and
                Account.email == email).delete(synchronize_session="fetch")
            if result != 0:
                session.commit()
                return account
            return False
        except SQLAlchemyError:
            return False


def reset_and_import() -> None:
    if not engine.dialect.has_table(connection, 'accounts'):
        Account.metadata.create_all()
        return
    Account.__table__.drop(engine)
    Account.metadata.create_all()
    return
