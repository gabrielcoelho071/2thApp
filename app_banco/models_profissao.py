from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float, Numeric
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, declarative_base

engine = create_engine('sqlite:///banco_profissao.db')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False, index=True)
    salario = Column(String(10), nullable=False, index=True)
    emprego = Column(String(40), nullable=False, index=True)

    def __repr__(self):
        return '<Usuario: {} {}>'.format(self.id_usuario, self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_usuario(self):
        dados_usuario = {
            "id_usuario": self.id_usuario,
            "nome": self.nome,
            "salario": self.salario,
            "emprego": self.emprego,
        }
        return dados_usuario

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()