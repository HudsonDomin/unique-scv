"""
Script de inicialização do servidor
Executa a aplicação FastAPI com suporte a WebSocket
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Recarrega automaticamente ao detectar mudanças
        ws_ping_interval=20,
        ws_ping_timeout=20
    )