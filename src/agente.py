# ============================================================
# agente.py — Lógica do Agente Lyra
# ============================================================

import json
import requests
import pandas as pd
from config import (
    OLLAMA_URL, OLLAMA_MODEL, TEMPERATURA,
    PERFIL_PATH, TRANSACOES_PATH, HISTORICO_PATH,
)


# ── 1. CARREGAMENTO DA BASE DE CONHECIMENTO ─────────────────

def carregar_perfil() -> dict:
    """Carrega o perfil do cliente a partir do JSON."""
    try:
        with open(PERFIL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def carregar_transacoes() -> pd.DataFrame:
    """Carrega o CSV de transações."""
    try:
        return pd.read_csv(TRANSACOES_PATH, parse_dates=["data"])
    except FileNotFoundError:
        return pd.DataFrame()


def carregar_historico() -> pd.DataFrame:
    """Carrega o CSV de histórico de atendimento."""
    try:
        return pd.read_csv(HISTORICO_PATH, parse_dates=["data"])
    except FileNotFoundError:
        return pd.DataFrame()


# ── 2. MONTAGEM DO CONTEXTO DINÂMICO ────────────────────────

def montar_contexto(perfil: dict, transacoes: pd.DataFrame, historico: pd.DataFrame) -> str:
    """
    Formata os dados carregados em texto estruturado
    para ser injetado no system prompt.
    """

    # Perfil
    perfil_txt = json.dumps(perfil, ensure_ascii=False, indent=2) if perfil else "Não disponível."

    # Transações
    if not transacoes.empty:
        trans_txt = transacoes.to_string(index=False)

        # Resumo por categoria
        resumo = (
            transacoes[transacoes["tipo"] == "saida"]
            .groupby("categoria")["valor"]
            .sum()
            .sort_values(ascending=False)
        )
        resumo_txt = "\n".join(
            f"  • {cat}: R$ {val:,.2f}" for cat, val in resumo.items()
        )

        total_saidas = transacoes[transacoes["tipo"] == "saida"]["valor"].sum()
        total_entradas = transacoes[transacoes["tipo"] == "entrada"]["valor"].sum()
        saldo = total_entradas - total_saidas
        sumario = (
            f"\nResumo financeiro do período:\n"
            f"  Receita total : R$ {total_entradas:,.2f}\n"
            f"  Saídas totais : R$ {total_saidas:,.2f}\n"
            f"  Saldo restante: R$ {saldo:,.2f}\n"
            f"  Por categoria:\n{resumo_txt}"
        )
    else:
        trans_txt = "Não disponível."
        sumario   = ""

    # Histórico de atendimento
    hist_txt = historico.to_string(index=False) if not historico.empty else "Não disponível."

    return f"""
PERFIL DO CLIENTE:
{perfil_txt}

TRANSAÇÕES DO MÊS ATUAL:
{trans_txt}
{sumario}

HISTÓRICO DE ATENDIMENTO:
{hist_txt}
"""


# ── 3. SYSTEM PROMPT ────────────────────────────────────────

def montar_system_prompt(contexto: str) -> str:
    """
    Retorna o system prompt completo da Lyra
    com o contexto do cliente já injetado.
    """
    return f"""Você é Lyra, uma assistente financeira pessoal inteligente, acessível e objetiva.

Seu objetivo é ajudar o cliente a organizar gastos mensais, identificar padrões de consumo e \
projetar orçamentos para os próximos meses — tudo com base nos dados fornecidos abaixo.

════════════════════════════════════════
DADOS DO CLIENTE (use SOMENTE estes dados):
{contexto}
════════════════════════════════════════

REGRAS FUNDAMENTAIS:
1. Baseie TODAS as respostas nos dados acima. Nunca invente valores ou padrões ausentes.
2. Se uma informação não estiver disponível, diga: "Não tenho essa informação no momento. \
Posso ajudar com algo relacionado ao seu orçamento?"
3. Nunca recomende investimentos, produtos financeiros de terceiros ou dê aconselhamento tributário.
4. Nunca compartilhe ou confirme dados de outros clientes.
5. Quando o cliente mencionar um gasto recorrente, pergunte se ele se repete todo mês.
6. Use linguagem simples, sem jargões. Tom: amigável, objetivo, encorajador. Não julgue hábitos.
7. Ao calcular projeções, explique como chegou aos valores.
8. Responda sempre em português do Brasil.

EXEMPLOS DE BOAS RESPOSTAS (Few-Shot):

Pergunta: "Quanto gastei com alimentação esse mês?"
Resposta: "Com base nas suas transações, você gastou R$ 570,00 em alimentação: R$ 450,00 no \
supermercado e R$ 120,00 em restaurante. Quer comparar com o mês anterior ou projetar novembro?"

Pergunta: "Vou conseguir fazer minha reserva esse mês?"
Resposta: "Sua meta é R$ 500,00 de reserva. Com o saldo restante de R$ 2.011,10, parece viável! \
Quer que eu liste os gastos variáveis que ainda podem surgir?"

Pergunta: "O que é CDB?"
Resposta: "Esse tema está fora do meu escopo. Para produtos de investimento, recomendo falar com \
um consultor financeiro. Posso ajudar com sua organização de gastos?"

FLUXO IDEAL:
1. Na primeira mensagem: saudação com nome do cliente + resumo rápido da situação atual.
2. Nas demais: responder à dúvida com base nos dados e sempre encerrar com uma sugestão proativa.

LIMITAÇÕES (comunique quando necessário):
- Não acesso dados bancários reais nem realizo transações.
- Não explico produtos de investimento nem indico onde investir.
- Não tenho memória entre sessões — cada sessão começa do zero com os dados fornecidos.
"""


# ── 4. INTEGRAÇÃO COM OLLAMA ─────────────────────────────────

def chamar_ollama(mensagens: list[dict]) -> str:
    """
    Envia o histórico de mensagens para o Ollama local
    e retorna a resposta em texto.

    Parâmetros
    ----------
    mensagens : lista de dicts no formato OpenAI Chat
        [{"role": "system"|"user"|"assistant", "content": "..."}]

    Retorna
    -------
    str — conteúdo da resposta do modelo
    """
    payload = {
        "model":    OLLAMA_MODEL,
        "messages": mensagens,
        "stream":   False,
        "options":  {"temperature": TEMPERATURA},
    }

    try:
        resposta = requests.post(OLLAMA_URL, json=payload, timeout=120)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados["message"]["content"]

    except requests.exceptions.ConnectionError:
        return (
            "⚠️ Não consegui conectar ao Ollama. "
            "Verifique se ele está rodando com `ollama serve` e tente novamente."
        )
    except requests.exceptions.Timeout:
        return "⚠️ O modelo demorou demais para responder. Tente uma pergunta mais curta."
    except Exception as e:
        return f"⚠️ Erro inesperado ao chamar o modelo: {e}"
