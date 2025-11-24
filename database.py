from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Define o URL do banco de dados. Usaremos SQLite para simplicidade.
# O arquivo 'banco.db' será criado no mesmo diretório.
SQLALCHEMY_DATABASE_URL = "sqlite:///./banco.db"

# Cria o engine (motor de conexão) que o SQLAlchemy usará.
# O 'connect_args' é necessário para SQLite.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria a base declarativa, que as classes de modelo herdarão.
Base = declarative_base()

# Define o modelo da tabela de usuários.
class Usuario(Base):
    __tablename__ = "usuarios"

    # Coluna de ID, chave primária e autoincrementável
    id = Column(Integer, primary_key=True, index=True)
    # Coluna de nome do usuário, tipo string
    nome = Column(String, index=True)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}')>"

# Cria a classe de sessão local. Cada instância de SessionLocal será uma sessão de banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para criar o banco de dados e as tabelas definidas (se ainda não existirem).
def criar_banco():
    # Cria todas as tabelas na base de dados
    Base.metadata.create_all(bind=engine)