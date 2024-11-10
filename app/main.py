from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import base
from .routers import auth, users, professores, alunos, produtos, comandas, rankings, agendamentos

app = FastAPI(title="Sistema de Gestão de Arena Esportiva")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar tabelas
base.Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(professores.router)
app.include_router(alunos.router)
app.include_router(produtos.router)
app.include_router(comandas.router)
app.include_router(rankings.router)
app.include_router(agendamentos.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Sistema de Gestão de Arena Esportiva"}