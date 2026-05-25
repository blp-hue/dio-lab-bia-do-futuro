# ============================================================
# app.py — Interface principal da Lyra (Streamlit)
# ============================================================

import streamlit as st
from agente import (
    carregar_perfil,
    carregar_transacoes,
    carregar_historico,
    montar_contexto,
    montar_system_prompt,
    chamar_ollama,
)
from config import MAX_HISTORICO_MSGS, OLLAMA_MODEL

# ── Configuração da página ───────────────────────────────────

st.set_page_config(
    page_title="Lyra · Assistente Financeira",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ────────────────────────────────────────

st.markdown("""
<style>
/* Fonte e fundo geral */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fundo principal escuro */
.stApp {
    background-color: #0f1117;
    color: #e8f0e9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #141a1f;
    border-right: 1px solid #1e2d24;
}

/* Balão do usuário */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 10px 0;
}
.msg-user .bubble {
    background: linear-gradient(135deg, #1a6b3a, #0f4a28);
    color: #e8f5ea;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    max-width: 72%;
    font-size: 0.95rem;
    line-height: 1.55;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}

/* Balão da Lyra */
.msg-lyra {
    display: flex;
    justify-content: flex-start;
    align-items: flex-end;
    gap: 10px;
    margin: 10px 0;
}
.msg-lyra .avatar {
    width: 34px;
    height: 34px;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    box-shadow: 0 0 10px rgba(34,197,94,0.3);
}
.msg-lyra .bubble {
    background-color: #1a2320;
    border: 1px solid #1e3a28;
    color: #d4edda;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 18px;
    max-width: 72%;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* Área do chat */
.chat-container {
    max-height: 62vh;
    overflow-y: auto;
    padding: 8px 4px;
}

/* Input de mensagem */
.stTextInput input {
    background-color: #1a2320 !important;
    border: 1px solid #1e3a28 !important;
    border-radius: 12px !important;
    color: #e8f5ea !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
}
.stTextInput input:focus {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 2px rgba(34,197,94,0.2) !important;
}

/* Botões */
.stButton > button {
    background: linear-gradient(135deg, #16a34a, #15803d);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    padding: 10px 20px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(34,197,94,0.3);
}

/* Métricas na sidebar */
[data-testid="metric-container"] {
    background-color: #1a2320;
    border: 1px solid #1e3a28;
    border-radius: 10px;
    padding: 12px 16px;
}
[data-testid="metric-container"] label {
    color: #6ee7b7 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e8f5ea !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    font-family: 'DM Mono', monospace !important;
}

/* Divisores */
hr {
    border-color: #1e3a28 !important;
    margin: 16px 0 !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #22c55e !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #1e3a28; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #22c55e; }

/* Tag modelo */
.model-tag {
    display: inline-block;
    background: #0d2818;
    color: #4ade80;
    border: 1px solid #166534;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    padding: 3px 10px;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)


# ── Carregamento dos dados (cached) ──────────────────────────

@st.cache_data(show_spinner=False)
def inicializar_dados():
    perfil     = carregar_perfil()
    transacoes = carregar_transacoes()
    historico  = carregar_historico()
    contexto   = montar_contexto(perfil, transacoes, historico)
    system     = montar_system_prompt(contexto)
    return perfil, transacoes, historico, contexto, system


perfil, transacoes, historico, contexto, system_prompt = inicializar_dados()

nome_cliente = perfil.get("nome", "Cliente").split()[0] if perfil else "Cliente"
renda        = perfil.get("renda_mensal", 0)
orcamento    = perfil.get("orçamento_mensal", 0)
reserva_meta = perfil.get("meta_de_reserva_mensal", 0)

# Calcula saldo disponível com base nas transações
if not transacoes.empty:
    total_saidas  = transacoes[transacoes["tipo"] == "saida"]["valor"].sum()
    total_entrada = transacoes[transacoes["tipo"] == "entrada"]["valor"].sum()
    saldo_disp    = total_entrada - total_saidas
else:
    total_saidas = total_entrada = saldo_disp = 0.0


# ── Estado da sessão ─────────────────────────────────────────

if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []   # lista de {"role": ..., "content": ...}

if "saudacao_feita" not in st.session_state:
    st.session_state.saudacao_feita = False


# ── Layout principal ─────────────────────────────────────────

# ---- Sidebar ------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 16px 0 8px 0;'>
            <div style='font-size:2.4rem;'>💚</div>
            <div style='font-size:1.4rem; font-weight:600; color:#4ade80; letter-spacing:-0.02em;'>Lyra</div>
            <div style='font-size:0.78rem; color:#6b7280; margin-top:2px;'>Assistente Financeira Pessoal</div>
            <div class='model-tag'>⚡ """ + OLLAMA_MODEL + """</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    if perfil:
        st.markdown(f"**👤 {perfil.get('nome', '—')}**")
        st.caption(perfil.get("profissao", ""))

        st.divider()
        st.markdown("##### 📊 Resumo do mês")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Renda", f"R$ {renda:,.0f}")
        with col2:
            st.metric("Gastos", f"R$ {total_saidas:,.0f}")

        col3, col4 = st.columns(2)
        with col3:
            st.metric("Saldo livre", f"R$ {saldo_disp:,.0f}")
        with col4:
            st.metric("Meta reserva", f"R$ {reserva_meta:,.0f}")

        # Barra de progresso do orçamento
        if orcamento > 0:
            pct = min(total_saidas / orcamento, 1.0)
            st.divider()
            st.markdown("##### 🎯 Orçamento mensal")
            st.progress(pct, text=f"R$ {total_saidas:,.0f} / R$ {orcamento:,.0f}")

        # Metas do perfil
        metas = perfil.get("metas", [])
        if metas:
            st.divider()
            st.markdown("##### 🏁 Metas")
            for m in metas:
                st.markdown(
                    f"<div style='font-size:0.82rem; color:#9ca3af; padding:3px 0;'>"
                    f"• {m.get('meta','—')} — <span style='color:#4ade80;'>R$ {m.get('valor_necessario', m.get('valor_necessário',0)):,.0f}</span></div>",
                    unsafe_allow_html=True,
                )
    else:
        st.warning("Nenhum perfil carregado. Verifique `data/perfil_cliente.json`.")

    st.divider()

    if st.button("🗑️ Limpar conversa", use_container_width=True):
        st.session_state.historico_chat = []
        st.session_state.saudacao_feita = False
        st.rerun()


# ---- Área principal ----------------------------------------
st.markdown(
    "<h2 style='color:#4ade80; font-weight:600; letter-spacing:-0.03em; margin-bottom:4px;'>"
    "Olá! Sou a Lyra 👋</h2>"
    "<p style='color:#6b7280; font-size:0.9rem; margin-top:0;'>"
    "Sua assistente de organização financeira pessoal. Como posso ajudar hoje?</p>",
    unsafe_allow_html=True,
)

st.divider()

# ── Saudação automática na primeira abertura ─────────────────
if not st.session_state.saudacao_feita:
    with st.spinner("Lyra está carregando seus dados..."):
        msg_inicial = (
            f"Oi, {nome_cliente}! 😊 Que bom ter você por aqui.\n\n"
            f"Aqui está um resumo rápido do seu mês:\n"
            f"- 💰 Receita: R$ {total_entrada:,.2f}\n"
            f"- 💸 Gastos até agora: R$ {total_saidas:,.2f}\n"
            f"- 🏦 Saldo disponível: R$ {saldo_disp:,.2f}\n"
            f"- 🎯 Meta de reserva: R$ {reserva_meta:,.2f}\n\n"
            f"Você está dentro do orçamento! Como posso ajudar? "
            f"Pode me perguntar sobre seus gastos, pedir uma projeção para o próximo mês "
            f"ou registrar um novo gasto. 🌿"
        )
        st.session_state.historico_chat.append(
            {"role": "assistant", "content": msg_inicial}
        )
        st.session_state.saudacao_feita = True

# ── Renderização das mensagens ────────────────────────────────
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.historico_chat:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='msg-user'><div class='bubble'>{msg['content']}</div></div>",
            unsafe_allow_html=True,
        )
    else:
        conteudo = msg["content"].replace("\n", "<br>")
        st.markdown(
            f"<div class='msg-lyra'>"
            f"<div class='avatar'>🌿</div>"
            f"<div class='bubble'>{conteudo}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ── Input de mensagem ─────────────────────────────────────────
col_input, col_btn = st.columns([6, 1])

with col_input:
    user_input = st.text_input(
        label="mensagem",
        placeholder=f"Digite sua mensagem para a Lyra...",
        label_visibility="collapsed",
        key="input_msg",
    )

with col_btn:
    enviar = st.button("Enviar ➤", use_container_width=True)

# Sugestões rápidas
st.markdown("<div style='margin-top:8px;'>", unsafe_allow_html=True)
sugestoes = [
    "📊 Resumo do mês",
    "📅 Projeção de novembro",
    "💾 Verificar meta de reserva",
    "🛒 Gastos por categoria",
]
cols = st.columns(len(sugestoes))
for i, sug in enumerate(sugestoes):
    with cols[i]:
        if st.button(sug, use_container_width=True, key=f"sug_{i}"):
            user_input = sug.split(" ", 1)[1]   # remove emoji
            enviar = True
st.markdown("</div>", unsafe_allow_html=True)


# ── Lógica de envio ───────────────────────────────────────────
if enviar and user_input and user_input.strip():
    # Adiciona mensagem do usuário
    st.session_state.historico_chat.append(
        {"role": "user", "content": user_input.strip()}
    )

    # Monta payload para o Ollama
    # Janela de contexto: system + últimas N mensagens
    msgs_ollama = [{"role": "system", "content": system_prompt}]
    janela = st.session_state.historico_chat[-MAX_HISTORICO_MSGS:]
    msgs_ollama.extend(janela)

    # Chama o modelo
    with st.spinner("Lyra está pensando..."):
        resposta = chamar_ollama(msgs_ollama)

    # Adiciona resposta ao histórico
    st.session_state.historico_chat.append(
        {"role": "assistant", "content": resposta}
    )

    st.rerun()
