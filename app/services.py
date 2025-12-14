"""
Lógica de Negócios
Implementa as regras de prioridade e ordenação
"""
from typing import Dict, List, Optional
from datetime import datetime
from . import database


def solicitar_carro(dados_chamado: Dict) -> Optional[int]:
    """
    Processa uma solicitação de carro
    Valida os dados e registra no banco
    """
    # Validação dos campos obrigatórios
    campos_obrigatorios = ['prisma_id', 'placa', 'modelo', 'local_solicitacao']
    for campo in campos_obrigatorios:
        if not dados_chamado.get(campo):
            raise ValueError(f"Campo obrigatório ausente: {campo}")
    
    # Define valores padrão
    dados_chamado['status'] = 'Pendente'
    dados_chamado['horario_solicitacao'] = datetime.now().isoformat()
    dados_chamado['prioridade'] = 1 if dados_chamado.get('prioridade') else 0
    
    # Insere no banco
    id_chamado = database.inserir_chamado(dados_chamado)
    return id_chamado


def atender_chamado(id_chamado: int, nome_manobrista: str) -> bool:
    """
    Registra o atendimento de um chamado
    Atualiza status e informações do manobrista
    """
    if not nome_manobrista or not nome_manobrista.strip():
        raise ValueError("Nome do manobrista é obrigatório")
    
    sucesso = database.atualizar_status_e_manobrista(id_chamado, nome_manobrista)
    return sucesso


def obter_lista_de_chamados() -> List[Dict]:
    """
    Retorna lista de chamados pendentes ordenados
    Prioridade: chamados prioritários primeiro, depois os mais antigos
    """
    chamados = database.buscar_chamados_pendentes()
    
    # Ordenação já é feita no SQL, mas podemos adicionar lógica extra aqui
    # Por exemplo: adicionar tempo de espera calculado
    for chamado in chamados:
        horario = datetime.fromisoformat(chamado['horario_solicitacao'])
        tempo_espera = (datetime.now() - horario).total_seconds() / 60
        chamado['tempo_espera_minutos'] = int(tempo_espera)
    
    return chamados