# Importação das bibliotecas necessárias
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Criação da aplicação FastAPI
app = FastAPI()

# Configurações do banco de dados PostgreSQL
# Aqui configuramos o URL de conexão para o PostgreSQL
# Substitua 'senha' e 'ufc_db' pelos seus dados
DATABASE_URL = "postgresql://postgres:senha@localhost/ufc_db"

# Cria a engine para se comunicar com o banco de dados
engine = create_engine(DATABASE_URL)

# Cria uma sessão local para conexão com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para mapeamento de classes do banco de dados
Base = declarative_base()

# Modelo da tabela no banco de dados
class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    duracao = Column(Integer)
    modalidade = Column(String)

# Criação da tabela no banco de dados
Base.metadata.create_all(bind=engine)

# Modelos Pydantic para validação de dados de entrada e saída
class CursoCreate(BaseModel):
    nome: str
    descricao: str
    duracao: int
    modalidade: str

class CursoResponse(CursoCreate):
    id: int

# Função para obter a sessão do banco de dados

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para listar todos os cursos
@app.get("/cursos", response_model=List[CursoResponse])
def listar_cursos(db: Session = Depends(get_db)):
    cursos = db.query(Curso).all()  # Recupera todos os cursos do banco de dados
    return cursos

# Endpoint para obter um curso específico pelo ID
@app.get("/cursos/{curso_id}", response_model=CursoResponse)
def obter_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()  # Filtra o curso pelo ID
    if not curso:  # Verifica se o curso existe
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

# Endpoint para adicionar um novo curso
@app.post("/cursos", response_model=CursoResponse)
def criar_curso(curso: CursoCreate, db: Session = Depends(get_db)):
    novo_curso = Curso(**curso.dict())  # Cria um novo curso com os dados fornecidos
    db.add(novo_curso)  # Adiciona o curso à sessão do banco
    db.commit()  # Salva as alterações
    db.refresh(novo_curso)  # Atualiza o curso para obter o ID gerado
    return novo_curso

# Endpoint para atualizar um curso existente pelo ID
@app.put("/cursos/{curso_id}", response_model=CursoResponse)
def atualizar_curso(curso_id: int, curso: CursoCreate, db: Session = Depends(get_db)):
    curso_existente = db.query(Curso).filter(Curso.id == curso_id).first()  # Busca o curso pelo ID
    if not curso_existente:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    for key, value in curso.dict().items():
        setattr(curso_existente, key, value)  # Atualiza os campos do curso
    db.commit()  # Salva as alterações
    db.refresh(curso_existente)  # Atualiza o curso com os novos dados
    return curso_existente

# Endpoint para remover um curso pelo ID
@app.delete("/cursos/{curso_id}")
def deletar_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()  # Busca o curso pelo ID
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    db.delete(curso)  # Remove o curso do banco
    db.commit()  # Salva a exclusão
    return {"message": "Curso removido com sucesso"}
