"""
Funções de conexão e operações com SQLite
Responsável por toda interação com o banco de dados
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from .models import SCHEMA_CHAMADOS

DB_PATH = "estacionamento.db"


def conectar_db() -> sqlite3.Connection:
    """Estabelece conexão com o banco SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Retorna resultados como dicionários
    return conn


def inicializar_db():
    """Cria as tabelas se não existirem"""
    conn = conectar_db()
    try:
        conn.execute(SCHEMA_CHAMADOS)
        conn.commit()
        print("✓ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"✗ Erro ao inicializar banco: {e}")
    finally:
        conn.close()


def inserir_chamado(dados: Dict) -> Optional[int]:
    """
    Insere um novo chamado no banco
    Retorna o ID do chamado inserido ou None em caso de erro
    """
    conn = conectar_db()
    try:
        cursor = conn.execute(
            """
            INSERT INTO Chamados_Veiculos 
            (prisma_id, placa, modelo, prioridade, status, local_solicitacao, horario_solicitacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dados['prisma_id'],
                dados['placa'],
                dados['modelo'],
                dados['prioridade'],
                dados['status'],
                dados['local_solicitacao'],
                dados['horario_solicitacao']
            )
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir chamado: {e}")
        return None
    finally:
        conn.close()


def buscar_chamados_pendentes() -> List[Dict]:
    """Busca todos os chamados com status 'Pendente'"""
    conn = conectar_db()
    try:
        cursor = conn.execute(
            """
            SELECT * FROM Chamados_Veiculos 
            WHERE status = 'Pendente'
            ORDER BY prioridade DESC, horario_solicitacao ASC
            """
        )
        chamados = [dict(row) for row in cursor.fetchall()]
        return chamados
    except Exception as e:
        print(f"Erro ao buscar chamados: {e}")
        return []
    finally:
        conn.close()


def buscar_todos_chamados() -> List[Dict]:
    """Busca todos os chamados (para debugging)"""
    conn = conectar_db()
    try:
        cursor = conn.execute("SELECT * FROM Chamados_Veiculos")
        chamados = [dict(row) for row in cursor.fetchall()]
        return chamados
    except Exception as e:
        print(f"Erro ao buscar todos chamados: {e}")
        return []
    finally:
        conn.close()


def atualizar_status_e_manobrista(id_chamado: int, nome_manobrista: str) -> bool:
    """
    Atualiza o status do chamado para 'Em Atendimento'
    Registra o manobrista e horário de atendimento
    """
    conn = conectar_db()
    try:
        conn.execute(
            """
            UPDATE Chamados_Veiculos 
            SET status = 'Em Atendimento', 
                manobrista_nome = ?, 
                horario_atendimento = ?
            WHERE id = ?
            """,
            (nome_manobrista, datetime.now().isoformat(), id_chamado)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar chamado: {e}")
        return False
    finally:
        conn.close()