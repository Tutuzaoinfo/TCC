import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Calculadora HP12C", layout="wide")
st.title("📊 Calculadora HP12C - Investimentos")

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

tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Juros Compostos", 
    "📈 Valor Futuro/Presente", 
    "🏦 Parcelas (PMT)",
    "📊 Taxa Interna de Retorno"
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

with tab2:
    st.header("Valor Futuro e Valor Presente")
    st.write("Calcule FV (Valor Futuro) ou PV (Valor Presente)")
    
    calc_type = st.radio("O que deseja calcular?", ["Valor Futuro (FV)", "Valor Presente (PV)"], horizontal=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if calc_type == "Valor Futuro (FV)":
            pv_vf = st.number_input("Valor Presente (PV)", value=5000.0, step=500.0, format="%.2f", key="pv_vf")
            taxa_vf = st.number_input("Taxa (% ao período)", value=1.5, step=0.1, format="%.2f", key="taxa_vf")
            n_vf = st.number_input("Número de Períodos (n)", value=24, step=1, min_value=1, key="n_vf")
        else:
            fv_vp = st.number_input("Valor Futuro (FV)", value=10000.0, step=500.0, format="%.2f", key="fv_vp")
            taxa_vp = st.number_input("Taxa (% ao período)", value=1.5, step=0.1, format="%.2f", key="taxa_vp")
            n_vp = st.number_input("Número de Períodos (n)", value=24, step=1, min_value=1, key="n_vp")
    
    with col2:
        if st.button("Calcular", type="primary", use_container_width=True, key="calc_fv_pv"):
            if calc_type == "Valor Futuro (FV)":
                i = taxa_vf / 100
                fv = pv_vf * ((1 + i) ** n_vf)
                st.markdown(f'<div class="big-number">R$ {fv:,.2f}</div>', unsafe_allow_html=True)
                st.success(f"Seu investimento de R$ {pv_vf:,.2f} valerá R$ {fv:,.2f} após {n_vf} períodos")
            else:
                i = taxa_vp / 100
                pv = fv_vp / ((1 + i) ** n_vp)
                st.markdown(f'<div class="big-number">R$ {pv:,.2f}</div>', unsafe_allow_html=True)
                st.success(f"Você precisa investir R$ {pv:,.2f} hoje para ter R$ {fv_vp:,.2f} após {n_vp} períodos")

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

with tab4:
    st.header("Taxa Interna de Retorno (TIR)")
    st.write("Calcule a taxa de retorno de um investimento com múltiplos fluxos de caixa")
    
    st.subheader("Fluxos de Caixa")
    st.info("Valores negativos representam investimentos (saídas). Valores positivos representam retornos (entradas).")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        num_fluxos = st.number_input("Número de períodos", value=5, min_value=2, max_value=20, step=1)
        
        fluxos = []
        cols = st.columns(min(5, num_fluxos))
        
        for i in range(num_fluxos):
            with cols[i % 5]:
                valor = st.number_input(
                    f"Período {i}", 
                    value=-10000.0 if i == 0 else 3000.0,
                    step=100.0,
                    format="%.2f",
                    key=f"fluxo_{i}"
                )
                fluxos.append(valor)
    
    with col2:
        if st.button("Calcular TIR", type="primary", use_container_width=True, key="calc_tir"):
            try:
                tir = np.irr(fluxos) * 100
                
                st.markdown(f'<div class="big-number">{tir:.2f}%</div>', unsafe_allow_html=True)
                st.success(f"Taxa Interna de Retorno: {tir:.2f}% ao período")
                
                taxas = np.linspace(-5, 20, 100)
                vpls = []
                
                for taxa in taxas:
                    i = taxa / 100
                    vpl = sum([fluxo / ((1 + i) ** idx) for idx, fluxo in enumerate(fluxos)])
                    vpls.append(vpl)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=taxas, y=vpls, name="VPL", line=dict(color="blue")))
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                fig.add_vline(x=tir, line_dash="dash", line_color="green", annotation_text=f"TIR = {tir:.2f}%")
                fig.update_layout(title="Valor Presente Líquido vs Taxa", xaxis_title="Taxa (%)", yaxis_title="VPL (R$)", height=400)
                st.plotly_chart(fig, use_container_width=True)
                
            except:
                st.error("Não foi possível calcular a TIR. Verifique os fluxos de caixa.")
        
        st.info("📌 A TIR é a taxa que faz o VPL = 0")

st.divider()
st.caption("💡 Calculadora HP12C Financeira | Ferramenta educacional para cálculos de investimentos")