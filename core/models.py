# Importa a biblioteca SQLAlchemy, que é usada para interagir com bancos de dados.
import sqlalchemy

# Importa classes específicas do módulo ORM (Object-Relational Mapping) do SQLAlchemy.
# Isso serve para mapear classes Python para tabelas de banco de dados e vice-versa.
# Estou usando para criar a estrutura do banco de dados e gerenciar relações entre tabelas.
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

# Cria uma conexão com um banco de dados SQLite, especificando o caminho do arquivo.
# Isso permite que a aplicação se conecte ao banco de dados para realizar operações.
engine = sqlalchemy.create_engine("sqlite:///database/db.sqlite3")

# Define uma classe base para todos os modelos do banco de dados.
# Isso serve para fornecer uma base comum para todas as tabelas do banco de dados.
# Estou usando para garantir que todas as tabelas tenham uma estrutura comum.
class Base(DeclarativeBase):
    __abstract__ = True  # Indica que esta classe é abstrata e não deve ser usada diretamente para criar tabelas.

    # Define uma coluna de ID que será a chave primária em todas as tabelas derivadas desta classe.
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    # Representação da instância como string.
    # Isso serve para fornecer uma representação legível da instância da classe.
    # Estou usando para facilitar a depuração e o registro das instâncias, porque isso permite ver rapidamente 
    # informações importantes sobre o objeto durante a depuração ou ao registrar logs.
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

# Define uma tabela chamada "categoria" no banco de dados.
# Isso serve para armazenar informações sobre categorias.
# Estou usando para organizar os modelos em categorias.
class Categoria(Base):
    __tablename__ = "categoria"  # Nome da tabela no banco de dados.
    
    # Colunas da tabela com seus tipos e restrições.
    nome = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    video_link = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    
    # Define um relacionamento com a tabela "modelos".
    # Isso serve para indicar que uma categoria pode ter vários modelos associados.
    # Estou usando para mapear a relação entre categorias e modelos.
    modelos = relationship("Modelos", back_populates="categoria")

    # Representação da instância como string.
    # Isso serve para fornecer uma representação legível da instância da classe.
    # Estou usando para facilitar a depuração e o registro das instâncias, porque isso permite ver rapidamente 
    # informações importantes sobre o objeto durante a depuração ou ao registrar logs.
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.nome}>"

# Define uma tabela chamada "modelos" no banco de dados.
# Isso serve para armazenar informações sobre modelos.
# Estou usando para representar cada modelo com detalhes específicos.
class Modelos(Base):
    __tablename__ = "modelos"  # Nome da tabela no banco de dados.

    # Colunas da tabela com seus tipos e restrições.
    nome = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    ipaddress = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    video_link = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    
    # Chave estrangeira referenciando a tabela "categoria".
    # Isso serve para criar um vínculo entre modelos e categorias.
    # Estou usando para conectar cada modelo a uma categoria específica.
    categoria_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("categoria.id")
    )
    
    # Define um relacionamento com a tabela "categoria".
    # Isso serve para indicar que um modelo pertence a uma categoria.
    # Estou usando para mapear a relação inversa entre modelos e categorias.
    categoria = relationship("Categoria", back_populates="modelos")

    # Representação da instância como string.
    # Isso serve para fornecer uma representação legível da instância da classe.
    # Estou usando para facilitar a depuração e o registro das instâncias, porque isso permite ver rapidamente 
    # informações importantes sobre o objeto durante a depuração ou ao registrar logs.
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.nome}>"

# Define uma tabela chamada "config" no banco de dados.
# Isso serve para armazenar configurações do sistema.
# Estou usando para salvar pares de chave-valor para configurações.
class Config(Base):
    __tablename__ = "config"  # Nome da tabela no banco de dados.
    
    # Colunas da tabela com seus tipos e restrições.
    key = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    value = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    # Representação da instância como string.
    # Isso serve para fornecer uma representação legível da instância da classe.
    # Estou usando para facilitar a depuração e o registro das instâncias, porque isso permite ver rapidamente 
    # informações importantes sobre o objeto durante a depuração ou ao registrar logs.
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.key}>"

# Define uma tabela chamada "user" no banco de dados.
# Isso serve para armazenar informações de usuários.
# Estou usando para gerenciar os dados de login e perfil dos usuários.
class User(Base):
    __tablename__ = "user"  # Nome da tabela no banco de dados.

    # Colunas da tabela com seus tipos e restrições.
    username = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_superuser = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_staff = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_moderator = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_verified = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_blocked = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    last_login = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    deleted_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    last_login = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    # Representação da instância como string.
    # Isso serve para fornecer uma representação legível da instância da classe.
    # Estou usando para facilitar a depuração e o registro das instâncias, porque isso permite ver rapidamente 
    # informações importantes sobre o objeto durante a depuração ou ao registrar logs.
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.username}>"

    # Representações alternativas da instância como string.
    # Isso serve para fornecer diferentes formas de representar a instância.
    # Estou usando para garantir compatibilidade com diferentes contextos de uso.
    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

# Função para obter uma sessão do banco de dados.
# Isso serve para criar uma sessão de conexão com o banco de dados.
# Estou usando para interagir com o banco de dados através de uma sessão.
def get_session():
    return Session(engine)

# Se este arquivo for executado diretamente, ele criará todas as tabelas no banco de dados.
if __name__ == "__main__":
    # Cria todas as tabelas definidas no banco de dados.
    # Isso serve para garantir que todas as tabelas necessárias existam no banco de dados.
    Base.metadata.create_all(engine)
    
    # Obtém uma sessão do banco de dados.
    # Isso serve para iniciar uma sessão para realizar operações no banco de dados.
    session = get_session()
    
    # Consulta todas as instâncias da tabela "categoria".
    # Isso serve para buscar todas as categorias do banco de dados.
    cat = session.query(Categoria).all()
    
    # Imprime a lista de atributos e métodos das instâncias de "categoria".
    # Isso serve para inspecionar as propriedades das categorias obtidas.
    print(dir(cat))
