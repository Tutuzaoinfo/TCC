import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Calculadora HP12C", layout="wide")
st.title("Calculadora HP12C - Investimentos")

st.markdown("""
<style>
    .big-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: #f0f2f6;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

tab1, tab3 = st.tabs([
    "Juros Compostos", 
    "Parcelas (PMT)",
])

with tab1:
    st.header("Calculadora de Juros Compostos")
    st.write("Calcule quanto seu investimento vai render ao longo do tempo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pv_jc = st.number_input("Valor Inicial (PV)", value=10000.0, step=1000.0, format="%.2f")
        taxa_jc = st.number_input("Taxa de Juros (% ao mês)", value=1.0, step=0.1, format="%.2f")
        periodo_jc = st.number_input("Período (meses)", value=12, step=1, min_value=1)
        aporte_jc = st.number_input("Aporte Mensal (PMT)", value=500.0, step=100.0, format="%.2f")
    
    with col2:
        if st.button("Calcular Juros Compostos", type="primary", use_container_width=True):
            i = taxa_jc / 100
            
            fv_principal = pv_jc * ((1 + i) ** periodo_jc)
            fv_aportes = aporte_jc * (((1 + i) ** periodo_jc - 1) / i) if i > 0 else aporte_jc * periodo_jc
            fv_total = fv_principal + fv_aportes
            
            total_investido = pv_jc + (aporte_jc * periodo_jc)
            rendimento = fv_total - total_investido
            
            st.markdown(f'<div class="big-number">R$ {fv_total:,.2f}</div>', unsafe_allow_html=True)
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Investido", f"R$ {total_investido:,.2f}")
            with m2:
                st.metric("Rendimento", f"R$ {rendimento:,.2f}")
            with m3:
                st.metric("Rentabilidade", f"{(rendimento/total_investido)*100:.2f}%")
    
    if st.checkbox("Mostrar Gráfico de Evolução"):
        i = taxa_jc / 100
        meses = list(range(periodo_jc + 1))
        valores_investidos = [pv_jc + (aporte_jc * m) for m in meses]
        valores_futuros = []
        
        for m in meses:
            fv_p = pv_jc * ((1 + i) ** m)
            fv_a = aporte_jc * (((1 + i) ** m - 1) / i) if i > 0 and m > 0 else 0
            valores_futuros.append(fv_p + fv_a)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=valores_investidos, name="Investido", line=dict(color="orange")))
        fig.add_trace(go.Scatter(x=meses, y=valores_futuros, name="Valor Total", line=dict(color="green")))
        fig.update_layout(title="Evolução do Investimento", xaxis_title="Meses", yaxis_title="Valor (R$)", height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Cálculo de Parcelas (PMT)")
    st.write("Calcule o valor das parcelas de um financiamento ou investimento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        pv_pmt = st.number_input("Valor do Empréstimo/Investimento (PV)", value=50000.0, step=5000.0, format="%.2f", key="pv_pmt")
        taxa_pmt = st.number_input("Taxa de Juros (% ao mês)", value=1.2, step=0.1, format="%.2f", key="taxa_pmt")
        n_pmt = st.number_input("Número de Parcelas", value=36, step=1, min_value=1, key="n_pmt")
        tipo_pmt = st.radio("Tipo de Pagamento", ["Postecipado (fim do período)", "Antecipado (início do período)"], key="tipo_pmt")
    
    with col2:
        if st.button("Calcular Parcela", type="primary", use_container_width=True, key="calc_pmt"):
            i = taxa_pmt / 100
            
            if tipo_pmt == "Postecipado (fim do período)":
                pmt = pv_pmt * (i * (1 + i)**n_pmt) / ((1 + i)**n_pmt - 1)
            else:
                pmt = pv_pmt * (i * (1 + i)**n_pmt) / (((1 + i)**n_pmt - 1) * (1 + i))
            
            total_pago = pmt * n_pmt
            juros_total = total_pago - pv_pmt
            
            st.markdown(f'<div class="big-number">R$ {pmt:,.2f}</div>', unsafe_allow_html=True)
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Valor Financiado", f"R$ {pv_pmt:,.2f}")
            with m2:
                st.metric("Total Pago", f"R$ {total_pago:,.2f}")
            with m3:
                st.metric("Juros Total", f"R$ {juros_total:,.2f}")
    
    if st.checkbox("Mostrar Tabela de Amortização", key="show_amort"):
        i = taxa_pmt / 100
        if tipo_pmt == "Postecipado (fim do período)":
            pmt = pv_pmt * (i * (1 + i)**n_pmt) / ((1 + i)**n_pmt - 1)
        else:
            pmt = pv_pmt * (i * (1 + i)**n_pmt) / (((1 + i)**n_pmt - 1) * (1 + i))
        
        tabela = []
        saldo = pv_pmt
        
        for mes in range(1, n_pmt + 1):
            juros = saldo * i
            amortizacao = pmt - juros
            saldo -= amortizacao
            
            tabela.append({
                "Mês": mes,
                "Saldo Inicial": f"R$ {saldo + amortizacao:,.2f}",
                "Juros": f"R$ {juros:,.2f}",
                "Amortização": f"R$ {amortizacao:,.2f}",
                "Parcela": f"R$ {pmt:,.2f}",
                "Saldo Final": f"R$ {max(0, saldo):,.2f}"
            })
        
        df_amort = pd.DataFrame(tabela)
        st.dataframe(df_amort, use_container_width=True, height=400)
st.divider()