"""
Definição das estruturas de dados do banco
Define o schema da tabela Chamados_Veiculos
"""

# Schema da tabela Chamados_Veiculos
SCHEMA_CHAMADOS = """
CREATE TABLE IF NOT EXISTS Chamados_Veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prisma_id TEXT NOT NULL,
    placa TEXT NOT NULL,
    modelo TEXT NOT NULL,
    prioridade INTEGER DEFAULT 0,
    status TEXT DEFAULT 'Pendente',
    local_solicitacao TEXT NOT NULL,
    horario_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    manobrista_nome TEXT,
    horario_atendimento TIMESTAMP
)
"""