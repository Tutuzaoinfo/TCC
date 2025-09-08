import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Bancos & Investimentos", layout="wide")

st.title("🏦 Dashboard — Bancos & Investimentos")
st.caption("Dados fictícios para demonstração • Substitua o CSV pelos seus dados")

df = pd.read_csv("bancos_investimentos.csv")

metrics = ["Renda Fixa","Ações","FIIs","Câmbio","ESG","Crédito"]
df["Total"] = df[metrics].sum(axis=1)

col1, col2, col3 = st.columns([1,1,2])
with col1:
    metric = st.selectbox("Métrica", metrics, index=0)
with col2:
    sort_dir = st.selectbox("Ordenação", ["Maior → menor","Menor → maior"])
with col3:
    search = st.text_input("Pesquisar banco...", "")

dff = df[df["Banco"].str.contains(search, case=False, na=False)].copy()
dff = dff.sort_values(metric, ascending=(sort_dir=="Menor → menor"))

k1, k2, k3, k4 = st.columns(4)
with k1: st.metric("Total Carteira", f"{dff[metrics].sum().sum():,.0f}")
with k2: st.metric("Média por Banco", f"{dff['Total'].mean():,.0f}")
with k3: st.metric(f"Top {metric}", f"{dff.iloc[0]['Banco'] if len(dff) else '-'}")
with k4: st.metric("Nº Bancos", f"{len(dff)}")

c1, c2 = st.columns([2,1])
with c1:
    fig_bar = px.bar(dff, x="Banco", y=metric, title=f"Comparativo — {metric}", height=420)
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    totals = dff[metrics].sum().reset_index()
    totals.columns = ["Classe","Valor"]
    fig_pie = px.pie(totals, names="Classe", values="Valor", title="Participação por Classe", height=420)
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Tabela de Detalhes")
st.dataframe(dff, use_container_width=True)

st.info("Para usar com seus dados, substitua o arquivo **bancos_investimentos.csv** pelo seu CSV no mesmo formato.")
