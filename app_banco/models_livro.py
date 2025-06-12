# models_livro.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# Configuração do banco de dados
engine = create_engine('sqlite:///banco_livro.db', connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


# Modelo Livro
class Livro(Base):
    __tablename__ = 'livros'

    id_livro = Column(Integer, primary_key=True)
    livro = Column(String(255), nullable=False, index=True)  # Nome do livro
    autor = Column(String(255), nullable=False, index=True)  # Autor do livro
    categoria = Column(String(255), nullable=False, index=True)  # Categoria do livro
    descricao = Column(String(255), nullable=False, index=True)  # Descrição do livro

    def __repr__(self):
        return f'<Livro: {self.id_livro} {self.livro}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        return {
            "id_livro": self.id_livro,
            "livro": self.livro,
            "autor": self.autor,
            "categoria": self.categoria,
            "descricao": self.descricao,
        }


# Função para criar as tabelas
def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()  # Criar as tabelas no banco de dados
    db_session.remove()  # Fechar a sessão
