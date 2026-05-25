# ============================================================
# config.py — Configurações do Agente Lyra
# ============================================================
# Para rodar localmente com Ollama:
#   1. Instale o Ollama: https://ollama.com/download
#   2. Execute: ollama pull llama3
#   3. O servidor sobe automaticamente em http://localhost:11434
# ============================================================

# --- Ollama ---
OLLAMA_URL   = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3"          # troque por "mistral", "phi3", etc. se preferir

# --- Arquivos de dados (relativos à pasta src/) ---
PERFIL_PATH    = "data/perfil_cliente.json"
TRANSACOES_PATH = "data/transacoes.csv"
HISTORICO_PATH  = "data/historico_atendimento.csv"

# --- Comportamento do agente ---
MAX_HISTORICO_MSGS = 20          # janela de contexto (pares usuário/agente)
TEMPERATURA        = 0.4         # baixa = mais determinístico e factual
