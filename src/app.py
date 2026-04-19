import json
import pandas as pd
import requests
import streamlit as st

#CONFIGURAÇÕES
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

# CARREGAR DADOS
perfil = json.load(open('./data/perfil.json'))
transacoes = pd.read_csv(open('./data/transacoes.csv'))
historico = pd.read_csv(open('./data/historico.csv'))
produtos = json.load(open('./data/produtos.json'))

# MONTAR CONTEXTO
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']} 
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R${perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# SYSTEM PROMPT
SYSTEM_PROMPT = """Você é o Astri, um agente de Swing Trade para iniciantes, amigável e didático.

OBJETIVO:
Ensinar conceitos de finanças pessoais e Swing Trade de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
1. NUNCA recomende investimentos específicos, explique como funcionam e ajude a entender qual seria o melhor caminho a seguir segundo o perfil do cliente;
2. Use os dados fornecidos para dar exemplos personalizados;
3. Linguagem simples, como se explicasse para um amigo;
4. Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
5. Sempre pergunte se o cliente entendeu;
6. Responda de forma sucinta e direta, com no máximo 3 parágrafos.
7. JAMAIS responda perguntas fora do tema de finanças pessoais e Swing Trade, ou que não estejam relacionadas ao perfil do cliente. Quando ocorrer, responda lembrando do seu papel de educador financeiro.
"""

#CHAMAR OLLAMA
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    pergunta: {msg}"""
    """
    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False}) 
    return r.json()['response']
    """
    
    # INTERFACE
    st.title("Astri - Seu Agente de Swing Trade")

    if pergunta := st.chat_input("Sua dúvida sobre finanças ou Swing Trade:"):
        st.chat_message("user").write(pergunta)
        with st.spinner("..."):
            st.chat_message("assistant").write(perguntar(pergunta))
