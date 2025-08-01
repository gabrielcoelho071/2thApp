# models_livro.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, relationship

# Configuração do banco de dados
engine = create_engine('sqlite:///banco_livro.db', connect_args={"check_same_thread": False})
local_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Livro(Base):
    __tablename__ = 'livros'
    id_livro = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False, index=True)
    autor = Column(String, nullable=False, index=True)
    ISBN = Column(String(13), nullable=False, index=True)
    resumo = Column(String, index=True)
    status_l = Column(Boolean, default=True, nullable=False, index=True)

    def __repr__(self):
        return f'<Livro(Título={self.titulo}, id{self.id_livro})>'

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def serialize(self):
        var_livro = {
            'id_livro': self.id_livro,
            'titulo': self.titulo,
            'autor': self.autor,
            'ISBN': self.ISBN,
            'resumo': self.resumo,
            'status_l': self.status_l
        }
        return var_livro


class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    CPF = Column(String, nullable=False, unique=True)
    endereco = Column(String)
    status_u = Column(Boolean, default=True, nullable=False, index=True)

    def __repr__(self):
        return f'<Usuário(nome={self.nome}, id{self.id_usuario})>'

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def serialize(self):
        var_usuario = {
            'id_usuario': self.id_usuario,
            'nome': self.nome,
            'email': self.email,
            'CPF': self.CPF,
            'endereco': self.endereco,
            'status_u': self.status_u
        }
        return var_usuario


class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    id_emprestimo = Column(Integer, primary_key=True)
    data_emprestimo = Column(String, nullable=False, index=True)
    data_devolucao = Column(String, nullable=False, index=True)
    livro_id = Column(Integer, ForeignKey('livros.id_livro'))
    livros = relationship('Livro')
    usuario_id = Column(Integer, ForeignKey('usuarios.id_usuario'))
    usuarios = relationship('Usuario')
    status_e = Column(Boolean, default=True, nullable=False, index=True)

    def __repr__(self):
        return f'<Empréstimo(livro={self.livro_id}, usuario{self.usuario_id})>'

    def save(self, db_session):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self, db_session):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def serialize(self):
        var_emprestimo = {
            'id_emprestimo': self.id_emprestimo,
            'data_emprestimo': self.data_emprestimo,
            'data_devolucao': self.data_devolucao,
            'livro': self.livro_id,
            'usuario': self.usuario_id,
            'status_e': self.status_e
        }
        return var_emprestimo

# Função para criar as tabelas
def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()