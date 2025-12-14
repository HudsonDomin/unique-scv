import React, { useState, useEffect } from 'react';
import { Car, Clock, User, MapPin, AlertCircle, CheckCircle } from 'lucide-react';

// Simulação de WebSocket para demonstração
class MockWebSocket {
  constructor() {
    this.handlers = {};
    this.connected = false;
    setTimeout(() => {
      this.connected = true;
      if (this.handlers.open) this.handlers.open();
    }, 500);
  }
  
  addEventListener(event, handler) {
    this.handlers[event] = handler;
  }
  
  send(data) {
    console.log('Enviando:', data);
  }
  
  simulateMessage(data) {
    if (this.handlers.message) {
      this.handlers.message({ data: JSON.stringify(data) });
    }
  }
}

const HotelValetSystem = () => {
  const [view, setView] = useState('menu');
  const [chamados, setChamados] = useState([]);
  const [ws, setWs] = useState(null);
  const [connected, setConnected] = useState(false);

  // Dados do formulário de solicitação
  const [formData, setFormData] = useState({
    prisma_id: '',
    placa: '',
    modelo: '',
    prioridade: false,
    local_solicitacao: 'Guarita'
  });

  // Nome do manobrista
  const [manobristaNome, setManobristaNome] = useState('');

  // Inicializar WebSocket
  useEffect(() => {
    const mockWs = new MockWebSocket();
    
    mockWs.addEventListener('open', () => {
      setConnected(true);
      console.log('WebSocket conectado');
    });

    mockWs.addEventListener('message', (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'chamados_update') {
        setChamados(data.chamados);
      } else if (data.type === 'novo_chamado') {
        setChamados(prev => [...prev, data.chamado]);
      } else if (data.type === 'chamado_atualizado') {
        setChamados(prev => prev.map(c => 
          c.id === data.chamado.id ? data.chamado : c
        ));
      }
    });

    setWs(mockWs);

    // Simular alguns chamados iniciais
    setTimeout(() => {
      mockWs.simulateMessage({
        type: 'chamados_update',
        chamados: [
          {
            id: 1,
            prisma_id: '123',
            placa: 'ABC-1234',
            modelo: 'Toyota Corolla',
            prioridade: 1,
            status: 'Pendente',
            local_solicitacao: 'Recepção',
            horario_solicitacao: new Date(Date.now() - 300000).toISOString(),
            manobrista_nome: null,
            horario_atendimento: null
          },
          {
            id: 2,
            prisma_id: '456',
            placa: 'XYZ-5678',
            modelo: 'Honda Civic',
            prioridade: 0,
            status: 'Pendente',
            local_solicitacao: 'Guarita',
            horario_solicitacao: new Date(Date.now() - 600000).toISOString(),
            manobrista_nome: null,
            horario_atendimento: null
          }
        ]
      });
    }, 1000);

    return () => {
      if (mockWs) mockWs.close?.();
    };
  }, []);

  // Função para solicitar carro
  const solicitarCarro = () => {
    if (!formData.prisma_id || !formData.placa || !formData.modelo) {
      alert('Por favor, preencha todos os campos');
      return;
    }
    
    const novoChamado = {
      ...formData,
      id: Date.now(),
      status: 'Pendente',
      horario_solicitacao: new Date().toISOString(),
      manobrista_nome: null,
      horario_atendimento: null
    };

    // Enviar via WebSocket
    if (ws && connected) {
      ws.send(JSON.stringify({
        action: 'solicitar_carro',
        data: novoChamado
      }));
      
      // Simular resposta
      setTimeout(() => {
        ws.simulateMessage({
          type: 'novo_chamado',
          chamado: novoChamado
        });
      }, 500);
    }

    // Limpar formulário
    setFormData({
      prisma_id: '',
      placa: '',
      modelo: '',
      prioridade: false,
      local_solicitacao: 'Guarita'
    });

    alert('Chamado registrado com sucesso!');
  };

  // Função para atender chamado
  const atenderChamado = (id) => {
    if (!manobristaNome.trim()) {
      alert('Por favor, insira seu nome antes de atender o chamado');
      return;
    }

    const chamadoAtualizado = chamados.find(c => c.id === id);
    if (chamadoAtualizado) {
      chamadoAtualizado.status = 'Em Atendimento';
      chamadoAtualizado.manobrista_nome = manobristaNome;
      chamadoAtualizado.horario_atendimento = new Date().toISOString();

      if (ws && connected) {
        ws.send(JSON.stringify({
          action: 'atender_chamado',
          id: id,
          manobrista: manobristaNome
        }));

        // Simular resposta
        setTimeout(() => {
          ws.simulateMessage({
            type: 'chamado_atualizado',
            chamado: chamadoAtualizado
          });
        }, 500);
      }
    }
  };

  // Ordenar chamados: prioridade primeiro, depois mais antigos
  const chamadosOrdenados = [...chamados]
    .filter(c => c.status === 'Pendente')
    .sort((a, b) => {
      if (a.prioridade !== b.prioridade) {
        return b.prioridade - a.prioridade;
      }
      return new Date(a.horario_solicitacao) - new Date(b.horario_solicitacao);
    });

  const formatarHorario = (iso) => {
    const data = new Date(iso);
    return data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  };

  const calcularTempoEspera = (iso) => {
    const diff = Date.now() - new Date(iso).getTime();
    const minutos = Math.floor(diff / 60000);
    return `${minutos} min`;
  };

  // Tela de Menu
  if (view === 'menu') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 p-4">
        <div className="max-w-2xl mx-auto pt-12">
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="text-center mb-8">
              <Car className="w-16 h-16 mx-auto mb-4 text-blue-600" />
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                Sistema de Estacionamento
              </h1>
              <p className="text-gray-600">Hotel Paradise</p>
            </div>

            <div className="space-y-4">
              <button
                onClick={() => setView('guarita')}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-xl transition-colors flex items-center justify-center gap-3"
              >
                <MapPin className="w-5 h-5" />
                Guarita / Recepção
              </button>

              <button
                onClick={() => setView('manobristas')}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-4 px-6 rounded-xl transition-colors flex items-center justify-center gap-3"
              >
                <User className="w-5 h-5" />
                Painel Manobristas
              </button>
            </div>

            <div className="mt-6 flex items-center justify-center gap-2 text-sm">
              <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-gray-600">
                {connected ? 'Conectado' : 'Desconectado'}
              </span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Tela Guarita/Recepção
  if (view === 'guarita') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 p-4">
        <div className="max-w-2xl mx-auto">
          <button
            onClick={() => setView('menu')}
            className="mb-4 text-blue-600 hover:text-blue-700 font-medium"
          >
            ← Voltar ao Menu
          </button>

          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-3">
              <MapPin className="w-7 h-7 text-blue-600" />
              Solicitar Veículo
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  ID do Prisma
                </label>
                <input
                  type="text"
                  value={formData.prisma_id}
                  onChange={(e) => setFormData({...formData, prisma_id: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Ex: 123"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Placa do Veículo
                </label>
                <input
                  type="text"
                  value={formData.placa}
                  onChange={(e) => setFormData({...formData, placa: e.target.value.toUpperCase()})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Ex: ABC-1234"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Modelo do Veículo
                </label>
                <input
                  type="text"
                  value={formData.modelo}
                  onChange={(e) => setFormData({...formData, modelo: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Ex: Toyota Corolla"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Local de Solicitação
                </label>
                <select
                  value={formData.local_solicitacao}
                  onChange={(e) => setFormData({...formData, local_solicitacao: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="Guarita">Guarita</option>
                  <option value="Recepção">Recepção</option>
                </select>
              </div>

              <div className="flex items-center gap-3 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                <input
                  type="checkbox"
                  id="prioridade"
                  checked={formData.prioridade}
                  onChange={(e) => setFormData({...formData, prioridade: e.target.checked})}
                  className="w-5 h-5 text-yellow-600 rounded focus:ring-2 focus:ring-yellow-500"
                />
                <label htmlFor="prioridade" className="text-sm font-medium text-gray-700 cursor-pointer">
                  <AlertCircle className="inline w-4 h-4 mr-1 text-yellow-600" />
                  Atendimento Prioritário
                </label>
              </div>

              <button
                onClick={solicitarCarro}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-colors"
              >
                Solicitar Veículo
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Tela Manobristas
  if (view === 'manobristas') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100 p-4">
        <div className="max-w-4xl mx-auto">
          <button
            onClick={() => setView('menu')}
            className="mb-4 text-green-600 hover:text-green-700 font-medium"
          >
            ← Voltar ao Menu
          </button>

          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-3">
              <User className="w-7 h-7 text-green-600" />
              Painel de Manobristas
            </h2>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Seu Nome
              </label>
              <input
                type="text"
                value={manobristaNome}
                onChange={(e) => setManobristaNome(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Digite seu nome"
              />
            </div>

            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-700">
                Chamados Pendentes ({chamadosOrdenados.length})
              </h3>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                Atualização em tempo real
              </div>
            </div>

            {chamadosOrdenados.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <CheckCircle className="w-12 h-12 mx-auto mb-3 text-green-400" />
                <p>Nenhum chamado pendente no momento</p>
              </div>
            ) : (
              <div className="space-y-3">
                {chamadosOrdenados.map((chamado) => (
                  <div
                    key={chamado.id}
                    className={`border-2 rounded-xl p-4 ${
                      chamado.prioridade 
                        ? 'border-yellow-400 bg-yellow-50' 
                        : 'border-gray-200 bg-white'
                    }`}
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        {chamado.prioridade ? (
                          <span className="inline-flex items-center gap-1 px-2 py-1 bg-yellow-400 text-yellow-900 text-xs font-bold rounded mb-2">
                            <AlertCircle className="w-3 h-3" />
                            PRIORITÁRIO
                          </span>
                        ) : null}
                        <div className="flex items-center gap-2 text-sm text-gray-600 mb-1">
                          <MapPin className="w-4 h-4" />
                          {chamado.local_solicitacao}
                        </div>
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <Clock className="w-4 h-4" />
                          {formatarHorario(chamado.horario_solicitacao)} • Aguardando {calcularTempoEspera(chamado.horario_solicitacao)}
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-3 mb-3 text-sm">
                      <div>
                        <span className="text-gray-500">Prisma:</span>
                        <p className="font-semibold">{chamado.prisma_id}</p>
                      </div>
                      <div>
                        <span className="text-gray-500">Placa:</span>
                        <p className="font-semibold">{chamado.placa}</p>
                      </div>
                      <div>
                        <span className="text-gray-500">Modelo:</span>
                        <p className="font-semibold">{chamado.modelo}</p>
                      </div>
                    </div>

                    <button
                      onClick={() => atenderChamado(chamado.id)}
                      disabled={!manobristaNome.trim()}
                      className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                    >
                      Atender Chamado
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }
};

export default HotelValetSystem;