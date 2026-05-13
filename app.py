import streamlit as st
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# --- 1. TREINAMENTO ---
frases = [
    "qual meu limite", "limite disponível", "aumentar meu limite", "ver limite",
    "fatura", "valor da fatura", "vencimento da conta", "boleto", "pagar fatura",
    "segurança", "esqueci a senha", "mudar senha", "trocar senha", "perdi a senha",
    "cancelar cartão", "quero cancelar", "encerrar conta", "cancelamento"
]
categorias = [
    "Limite", "Limite", "Limite", "Limite",
    "Fatura", "Fatura", "Fatura", "Fatura", "Fatura",
    "Segurança", "Segurança", "Segurança", "Segurança", "Segurança",
    "cancelamento", "cancelamento", "cancelamento", "cancelamento"
]

vetorizador = CountVectorizer()
X = vetorizador.fit_transform(frases)
modelo = MultinomialNB()
modelo.fit(X, categorias)

respostas_base = {
    "Segurança": "🔒 Para sua segurança, você pode redefinir sua senha diretamente no menu 'Segurança' do nosso aplicativo móvel.",
    "cancelamento": "😔 Poxa, ficamos tristes com isso. Para cancelar seu cartão, por favor ligue para nossa central no 0800-123-456."
}

# --- 2. FUNÇÕES DE BANCO DE DADOS ---

def validar_login(conta, senha):
    try:
        conn = sqlite3.connect('cartao.db')
        # Busca o usuário que tenha essa conta E essa senha
        query = "SELECT nome FROM usuarios WHERE conta = ? AND senha_acesso = ?"
        df = pd.read_sql_query(query, conn, params=(conta, senha))
        conn.close()
        return df.iloc[0] if not df.empty else None
    except Exception as e:
        return None

def buscar_dados_financeiros(conta, colunas):
    try:
        conn = sqlite3.connect('cartao.db')
        query_cols = ", ".join(colunas) if isinstance(colunas, list) else colunas
        df = pd.read_sql_query(f"SELECT {query_cols} FROM usuarios WHERE conta = ?", conn, params=(conta,))
        conn.close()
        return df.iloc[0] if not df.empty else None
    except Exception as e:
        return None

# --- 3. INTERFACE VISUAL ---

st.set_page_config(page_title="Seu Banco Digital", page_icon="🏦", layout="centered")

if "logado" not in st.session_state:
    st.session_state.logado = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# CSS dinâmico para esconder header e ajustar layout
classe_status = "st-deslogado" if not st.session_state.logado else "st-logado"
st.markdown(f"""
    <style>
    [data-testid="stHeader"], header {{ display: none !important; }}
    .stApp {{ background-color: #0E1117; }}
    .login-container {{ width: 100%; max-width: 500px; text-align: center; padding: 20px; margin: auto; }}
    .login-container h1 {{ font-size: 3rem !important; }}
    </style>
    <div class="{classe_status}"></div>
""", unsafe_allow_html=True)

# --- FLUXO DE LOGIN ---
if not st.session_state.logado:
    _, col_central, _ = st.columns([0.1, 0.8, 0.1])
    with col_central:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; justify-content: center;"><img src="https://cdn-icons-png.flaticon.com/512/2830/2830284.png" width="120"></div>', unsafe_allow_html=True)
        st.title("Acesse sua conta")
        
        # O max_chars=6 permite: 4 números + 1 traço + 1 número = 6 caracteres
        conta_input = st.text_input("Número da Conta:", placeholder="Ex: 1234-5", max_chars=6)
        senha_input = st.text_input("Senha de 4 dígitos:", type="password", max_chars=4)
        
        if st.button("Entrar", use_container_width=True):
            # Validação extra: verifica se tem o traço na posição certa
            if len(conta_input) == 6 and conta_input[4] == "-":
                usuario = validar_login(conta_input, senha_input)
                if usuario is not None:
                    st.session_state.logado = True
                    st.session_state.conta_usuario = conta_input
                    st.session_state.nome_usuario = usuario['nome']
                    st.rerun()
                else:
                    st.error("Conta ou senha incorretos.")
            else:
                st.warning("Formato inválido! Use o padrão 0000-0 (6 caracteres com o traço).")
        st.markdown('</div>', unsafe_allow_html=True)

# --- FLUXO DO CHAT ---
else:
    col_vazia, col_botao = st.columns([0.85, 0.15])
    with col_botao:
        if st.button("Sair 🚪"):
            st.session_state.logado = False
            st.session_state.messages = []
            st.rerun()

    st.title("🏦 Banco Lay - Atendimento")
    st.caption(f"Seja bem vindo(a), {st.session_state.nome_usuario}!!| Conta logada: {st.session_state.conta_usuario}")
    st.divider()

    # Mostrar histórico (Apenas UM loop para não duplicar)
    for message in st.session_state.messages:
        icone = "🏦" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=icone):
            st.markdown(message["content"])

    # Entrada do chat
    if prompt := st.chat_input("Como posso ajudar?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # Lógica de Inteligência Artificial
        pergunta_vet = vetorizador.transform([prompt.lower()])
        categoria = modelo.predict(pergunta_vet)[0]
        prob = max(modelo.predict_proba(pergunta_vet)[0])

        if prob < 0.35:
            resposta = "Desculpe, não entendi. Pode reformular sua dúvida?"
        else:
            if categoria == "Limite":
                res = buscar_dados_financeiros(st.session_state.conta_usuario, ["limite"])
                resposta = f"💰 Seu limite disponível é **R$ {res['limite']:.2f}**."
            elif categoria == "Fatura":
                res = buscar_dados_financeiros(st.session_state.conta_usuario, ["valor_fatura", "vencimento_fatura"])
                resposta = f"📄 Sua fatura atual é de **R$ {res['valor_fatura']:.2f}** com vencimento em **{res['vencimento_fatura']}**."
            else:
                resposta = respostas_base.get(categoria, "Como posso ajudar?")

        with st.chat_message("assistant", avatar="🏦"):
            st.markdown(resposta)
        st.session_state.messages.append({"role": "assistant", "content": resposta})