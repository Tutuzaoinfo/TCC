import pandas as pd
import plotly.express as px
import streamlit as st
import requests
import os

st.set_page_config(page_title="Bancos & Investimentos", layout="wide")
st.title("💸 Smooth Investing")

filepath = os.path.join(os.path.dirname(__file__), "bancos_investimentos.csv")
df = pd.read_csv(filepath)
    
metrics = ["Renda Fixa", "Ações", "FIIs", "Câmbio", "ESG", "Crédito"]
df["Total"] = df[metrics].sum(axis=1)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    metric = st.selectbox("Métrica", metrics, index=0)
with col2:
    sort_dir = st.selectbox("Ordenação", ["Maior → menor", "Menor → maior"])
with col3:
    search = st.text_input("Pesquisar banco...", "")

dff = df[df["Banco"].str.contains(search, case=False, na=False)].copy()
dff = dff.sort_values(metric, ascending=(sort_dir == "Menor → menor"))

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Total Carteira", f"{dff[metrics].sum().sum():,.0f}")
with k2:
    st.metric("Média por Banco", f"{dff['Total'].mean():,.0f}")
with k3:
    st.metric(f"Top {metric}", f"{dff.iloc[0]['Banco'] if len(dff) else '-'}")
with k4:
    st.metric("Nº Bancos", f"{len(dff)}")

c1, c2 = st.columns([2, 1])
with c1:
    fig_bar = px.bar(
        dff,
        x="Banco",
        y=metric,
        color=metric,
        hover_data=metrics,
        title=f"Comparativo — {metric}",
        height=420,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    totals = dff[metrics].sum().reset_index()
    totals.columns = ["Classe", "Valor"]
    fig_pie = px.pie(totals, names="Classe", values="Valor", title="Participação por Classe", height=420)
    st.plotly_chart(fig_pie, use_container_width=True)

st.title("📈 Cotação de Ações — Brapi")

ticker = st.text_input("Digite o ticker da ação:", "PETR4")
headers = {"Authorization": f"Bearer 3GESW9TDeo7A1Jy2T5s1v8"}

if st.button("Buscar cotação"):
    url = f"https://brapi.dev/api/quote/{ticker.upper()}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()["results"][0]

        st.metric("Preço Atual", f"R$ {data['regularMarketPrice']:.2f}")
        st.metric("Variação do Dia", f"{data['regularMarketChangePercent']:.2f}%")
        st.metric("Máxima do Dia", f"R$ {data['regularMarketDayHigh']}")
        st.metric("Mínima do Dia", f"R$ {data['regularMarketDayLow']}")

        hist_url = f"https://brapi.dev/api/quote/{ticker.upper()}?range=1mo&interval=1d"
        hist_resp = requests.get(hist_url, headers=headers)
        if hist_resp.status_code == 200:
            hist = hist_resp.json()["results"][0]["historicalDataPrice"]
            df_hist = pd.DataFrame(hist)
            df_hist["date"] = pd.to_datetime(df_hist["date"], unit="s")
            fig_line = px.line(df_hist, x="date", y="close", title=f"Histórico {ticker.upper()}")
            st.plotly_chart(fig_line, use_container_width=True)

    else:
        st.error(f"Erro {response.status_code}: {response.text}")

st.title("📊 Top 5 Ações Brasil")

TOKEN = "Bearer 3GESW9TDeo7A1Jy2T5s1v8" 

top0_actions = ["PETR4"] 
top1_actions = ["VALE3"] 
top2_actions = ["ITUB4"] 
top3_actions = ["MXRF11"] 
top4_actions = ["BBAS3"] 

def get_quotes(tickers): 
    url = f"https://brapi.dev/api/quote/{','.join(tickers)}" 
    headers = {"Authorization": TOKEN} 
    resp = requests.get(url, headers=headers) 
    if resp.status_code == 200: 
        return resp.json().get("results", []) 
    else: 
        st.error(f"Erro {resp.status_code}: {resp.text}") 
        return []
    
acoes = get_quotes(top0_actions) 
acoes1 = get_quotes(top1_actions) 
acoes2 = get_quotes(top2_actions) 
acoes3 = get_quotes(top3_actions) 
acoes4 = get_quotes(top4_actions) 

if acoes: 
    tabela = [] 
    for acao in acoes: 
        tabela.append({ 
            "Ticker": acao["symbol"],
            "Empresa": acao.get("longName", "-"),
            "Preço": f"R$ {acao['regularMarketPrice']:.2f}",
            "Variação (%)": f"{acao['regularMarketChangePercent']:.2f}%", 
            "Volume": f"{acao['regularMarketVolume']:,}" 
            }) 
        for acao in acoes1: 
            tabela.append({ 
                "Ticker": acao["symbol"], 
                "Empresa": acao.get("longName", "-"), 
                "Preço": f"R$ {acao['regularMarketPrice']:.2f}", 
                "Variação (%)": f"{acao['regularMarketChangePercent']:.2f}%", 
                "Volume": f"{acao['regularMarketVolume']:,}" 
                }) 
        for acao in acoes2: 
            tabela.append({ 
                "Ticker": acao["symbol"], 
                "Empresa": acao.get("longName", "-"), 
                "Preço": f"R$ {acao['regularMarketPrice']:.2f}", 
                "Variação (%)": f"{acao['regularMarketChangePercent']:.2f}%", 
                "Volume": f"{acao['regularMarketVolume']:,}" 
                }) 
        for acao in acoes3: 
            tabela.append({ 
                "Ticker": acao["symbol"], 
                "Empresa": acao.get("longName", "-"), 
                "Preço": f"R$ {acao['regularMarketPrice']:.2f}", 
                "Variação (%)": f"{acao['regularMarketChangePercent']:.2f}%", 
                "Volume": f"{acao['regularMarketVolume']:,}" 
                }) 
        for acao in acoes4: 
            tabela.append({ 
                "Ticker": acao["symbol"], 
                "Empresa": acao.get("longName", "-"), 
                "Preço": f"R$ {acao['regularMarketPrice']:.2f}", 
                "Variação (%)": f"{acao['regularMarketChangePercent']:.2f}%", 
                "Volume": f"{acao['regularMarketVolume']:,}" 
                }) 
                
    st.table(tabela)

st.subheader("Tabela de Detalhes")
st.dataframe(dff.reset_index(drop=True), hide_index=True, use_container_width=True)

st.info("⚠️ Nenhum dado nesse site é real — os dados têm um propósito demonstrativo apenas!")
