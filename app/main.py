"""
Ponto de entrada da aplicação FastAPI
Inicializa o servidor e registra as rotas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import inicializar_db
from .routes import router

# Cria a aplicação FastAPI
app = FastAPI(
    title="Sistema de Estacionamento Hotel",
    description="API para gerenciamento de chamados de veículos",
    version="1.0.0"
)

# Configuração CORS (permite requisições de qualquer origem)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta pasta de arquivos estáticos
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

# Registra as rotas
app.include_router(router)

# Evento de inicialização
@app.on_event("startup")
async def startup_event():
    """Executado ao iniciar o servidor"""
    print("=" * 50)
    print("🚗 Sistema de Estacionamento Hotel")
    print("=" * 50)
    inicializar_db()
    print("✓ Servidor iniciado com sucesso!")
    print("📡 Acesse: http://localhost:8000")
    print("=" * 50)

# Rota de health check
@app.get("/health")
async def health_check():
    """Verifica se a API está funcionando"""
    return {"status": "ok", "message": "API funcionando corretamente"}