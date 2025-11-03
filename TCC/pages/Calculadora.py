import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Calculadora & Simulador — Renda Fixa", layout="wide")

def ir_rate_by_days(days):
    if days <= 180:
        return 0.225
    elif days <= 360:
        return 0.20
    elif days <= 720:
        return 0.175
    else:
        return 0.15


def compound_lump_sum(principal, annual_rate, years, compounds_per_year=12):
    r = annual_rate
    n = compounds_per_year
    t = years
    fv = principal * (1 + r / n) ** (n * t)
    return fv


def compound_with_contributions(principal, monthly_contribution, annual_rate, years):
    months = int(years * 12)
    monthly_rate = annual_rate / 12

    balance = principal
    records = []
    for m in range(1, months + 1):
        balance = balance * (1 + monthly_rate)
        balance += monthly_contribution
        records.append({"Mes": m, "Saldo": balance})

    df = pd.DataFrame(records)
    df["Ano"] = (df["Mes"] / 12).apply(lambda x: int(np.floor(x)) + 1)
    return df


def apply_tax_and_inflation(gross, principal, years, inflation_rate=0.0):
    invested = principal
    gain = gross - invested
    days = int(years * 365)
    aliquot = ir_rate_by_days(days)
    tax = gain * aliquot
    net = gross - tax
    real_net = net / ((1 + inflation_rate) ** years)
    return {"gross": gross, "tax": tax, "net": net, "real_net": real_net, "aliquot": aliquot}


st.title("Calculadora de Investimentos — Renda Fixa & Simulação")
st.markdown("---")

st.header("Parâmetros Gerais")

col1, col2, col3 = st.columns(3)

with col1:
    initial_aporte = st.number_input(
        "Aporte inicial (R$)", 
        min_value=0.0, 
        value=10000.0, 
        step=100.0, 
        format="%.2f"
    )
    
    monthly_aporte = st.number_input(
        "Aporte mensal (R$)", 
        min_value=0.0, 
        value=500.0, 
        step=50.0, 
        format="%.2f"
    )

with col2:
    annual_rate_pct = st.number_input(
        "Taxa anual nominal (%)", 
        value=8.0, 
        step=0.1, 
        format="%.2f"
    )
    
    years = st.slider(
        "Horizonte (anos)", 
        min_value=1, 
        max_value=50, 
        value=10
    )

with col3:    
    inflation_pct = st.number_input(
        "Inflação anual estimada (%)", 
        value=3.5, 
        step=0.1, 
        format="%.2f"
    )

annual_rate = annual_rate_pct / 100.0
inflation_rate = inflation_pct / 100.0

st.markdown("---")

with st.expander("**Resumo dos Parâmetros Configurados**", expanded=False):
    col1, col2, col3 = st.columns(3)
    col1.metric("Aporte Inicial", f"R$ {initial_aporte:,.2f}")
    col2.metric("Aporte Mensal", f"R$ {monthly_aporte:,.2f}")
    col3.metric("Taxa Anual", f"{annual_rate_pct:.2f}%")
    
    col4, col5, col6 = st.columns(3)
    col4.metric("Horizonte", f"{years} anos")
    col6.metric("Inflação Estimada", f"{inflation_pct:.2f}%")

st.markdown("---")

st.header("Simulação — Aporte Inicial + Aportes Mensais")

if monthly_aporte == 0 and initial_aporte == 0:
    st.warning("Insira pelo menos um aporte inicial ou aporte mensal para simular.")
else:
    df_sim = compound_with_contributions(initial_aporte, monthly_aporte, annual_rate, years)
    fv_monthly = df_sim.iloc[-1]["Saldo"] if not df_sim.empty else initial_aporte
    total_invested = initial_aporte + monthly_aporte * years * 12

    tax_info2 = apply_tax_and_inflation(fv_monthly, total_invested, years, inflation_rate=inflation_rate)

    m1, m2, m3 = st.columns(3)
    m1.metric("Valor final bruto (R$)", f"{fv_monthly:,.2f}")
    m2.metric("Total investido (R$)", f"{total_invested:,.2f}")
    m3.metric("Ganho líquido após IR (R$)", f"{tax_info2['net'] - total_invested:,.2f}")

    df_sim["Ano"] = ((df_sim["Mes"] - 1) // 12) + 1
    resumo = df_sim.groupby("Ano")["Saldo"].last().reset_index()
    resumo["Total Investido (R$)"] = resumo["Ano"].apply(lambda a: initial_aporte + monthly_aporte * (a * 12))
    resumo["Ganho Bruto (R$)"] = resumo["Saldo"] - resumo["Total Investido (R$)"]
    resumo["Saldo (R$)"] = resumo["Saldo"]

    resumo_display = resumo[["Ano", "Total Investido (R$)", "Saldo (R$)", "Ganho Bruto (R$)"]].copy()

    st.subheader("Evolução Anual do Investimento")
    st.dataframe(resumo_display.style.format({
        "Total Investido (R$)": "R$ {:,.2f}",
        "Saldo (R$)": "R$ {:,.2f}",
        "Ganho Bruto (R$)": "R$ {:,.2f}"
    }), use_container_width=True, height=400)

st.markdown("---")

