# 🏦 Banco Lay - Chatbot Bancário Inteligente

Sistema de atendimento bancário inteligente desenvolvido com Python, Streamlit, SQLite e Machine Learning, simulando a experiência de um banco digital moderno com autenticação de usuários e chatbot integrado.

---

# 📌 Sobre o Projeto

O Banco Lay é uma aplicação web interativa criada para simular um sistema de atendimento automatizado de bancos digitais.
A plataforma utiliza Inteligência Artificial para interpretar perguntas dos usuários e responder consultas financeiras em tempo real.

O projeto combina:

* Interface moderna com Streamlit
* Banco de dados SQLite
* Processamento de linguagem natural
* Machine Learning com Scikit-learn
* Sistema de autenticação
* Atendimento conversacional via chat

---

# 🚀 Funcionalidades

## 🔐 Autenticação de Usuário

* Login com conta e senha
* Validação de formato da conta (`0000-0`)
* Controle de sessão com `st.session_state`

## 🤖 Chatbot Inteligente

O assistente virtual consegue identificar intenções do usuário como:

* Consulta de limite
* Informações de fatura
* Segurança da conta
* Cancelamento de cartão

## 💳 Integração Financeira

* Consulta de limite disponível
* Consulta de valor da fatura
* Consulta de vencimento

## 🎨 Interface Moderna

* Layout personalizado
* Tema dark
* Chat interativo
* Avatares personalizados
* Tela de login centralizada

---

# 🧠 Tecnologias Utilizadas

* Python 3
* Streamlit
* SQLite3
* Pandas
* Scikit-learn
* CountVectorizer
* MultinomialNB

---

# 📂 Estrutura do Projeto

```bash
📦 banco-lay
 ┣ 📜 app.py
 ┣ 📜 setup.db.py
 ┣ 📜 cartao.db
 ┣ 📜 requirements.txt
 ┗ 📜 README.md
```

---

# ⚙️ Como Executar o Projeto

## 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/banco-lay.git
```

---

## 2️⃣ Acesse a pasta

```bash
cd banco-lay
```

---

## 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Execute o projeto

```bash
streamlit run app.py
```

---

# 🗄️ Banco de Dados

O sistema utiliza SQLite como banco de dados local.

Tabela principal:

## usuarios

| Campo             | Tipo |
| ----------------- | ---- |
| nome              | TEXT |
| conta             | TEXT |
| senha_acesso      | TEXT |
| limite            | REAL |
| valor_fatura      | REAL |
| vencimento_fatura | TEXT |

---

# 🤖 Inteligência Artificial

O chatbot utiliza:

* `CountVectorizer` para vetorização de texto
* `MultinomialNB` para classificação de intenções

A IA foi treinada para identificar categorias específicas de atendimento bancário.

---

# 📸 Interface

O sistema possui:

* Tela de login
* Chat bancário
* Histórico de mensagens
* Logout seguro
* Interface responsiva

---

# 🔒 Segurança

* Validação de login
* Sessão autenticada
* Consultas protegidas por conta
* Tratamento de exceções

---

# 📈 Melhorias Futuras

* Integração com APIs bancárias
* Cadastro de usuários
* Recuperação de senha
* Dashboard financeiro
* IA mais avançada com NLP
* Banco de dados em nuvem
* Deploy online

---

# 👨‍💻 Autor

Desenvolvido por Layse Sena Baptista 🚀
