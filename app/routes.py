"""
Definição das rotas da API
Endpoints REST e WebSocket
"""
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from typing import Dict, List
import json
from . import services

# Router para as rotas da API
router = APIRouter()

# Gerenciador de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Envia mensagem para todos os clientes conectados"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()


# ==================== ROTAS DA API REST ====================

@router.post("/api/solicitar")
async def api_solicitar_carro(dados: Dict):
    """Endpoint para solicitar um veículo"""
    try:
        id_chamado = services.solicitar_carro(dados)
        if id_chamado:
            # Notifica todos os clientes via WebSocket
            await manager.broadcast({
                "type": "novo_chamado",
                "chamado": {**dados, "id": id_chamado}
            })
            return {"success": True, "id": id_chamado}
        else:
            raise HTTPException(status_code=500, detail="Erro ao criar chamado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/chamados_pendentes")
async def api_chamados_pendentes():
    """Endpoint para listar chamados pendentes"""
    chamados = services.obter_lista_de_chamados()
    return {"chamados": chamados}


@router.post("/api/atender_chamado")
async def api_atender_chamado(dados: Dict):
    """Endpoint para registrar atendimento de um chamado"""
    try:
        id_chamado = dados.get('id')
        manobrista = dados.get('manobrista')
        
        if not id_chamado or not manobrista:
            raise ValueError("ID do chamado e nome do manobrista são obrigatórios")
        
        sucesso = services.atender_chamado(id_chamado, manobrista)
        
        if sucesso:
            # Notifica todos os clientes via WebSocket
            await manager.broadcast({
                "type": "chamado_atualizado",
                "id": id_chamado
            })
            return {"success": True}
        else:
            raise HTTPException(status_code=500, detail="Erro ao atender chamado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== WEBSOCKET ====================

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para comunicação em tempo real"""
    await manager.connect(websocket)
    try:
        # Envia lista inicial de chamados
        chamados = services.obter_lista_de_chamados()
        await websocket.send_json({
            "type": "chamados_update",
            "chamados": chamados
        })
        
        # Mantém conexão aberta e processa mensagens
        while True:
            data = await websocket.receive_text()
            # Aqui você pode processar comandos do cliente se necessário
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ==================== ROTAS HTML ====================

@router.get("/", response_class=HTMLResponse)
async def pagina_inicial():
    """Renderiza página inicial"""
    return FileResponse("templates/index.html")

@router.get("/guarita_recepcao.html", response_class=HTMLResponse)
async def pagina_guarita():
    """Renderiza página da Guarita/Recepção"""
    return FileResponse("templates/guarita_recepcao.html")

@router.get("/manobristas.html", response_class=HTMLResponse)
async def pagina_manobristas():
    """Renderiza página dos Manobristas"""
    return FileResponse("templates/manobristas.html")