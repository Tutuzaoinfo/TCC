import pandas as pd
import plotly.express as px
import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Indicadores BCB", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    h1 {color: #1e3a8a;}
    </style>
""", unsafe_allow_html=True)

st.title("Dashboard de Indicadores Econômicos - Banco Central")
st.markdown("Dados oficiais do Banco Central do Brasil em tempo real")

@st.cache_data(ttl=3600)
def buscar_selic(anos=4):
    codigo_serie = 1178
    data_final = datetime.today().strftime('%d/%m/%Y')
    data_inicial = (datetime.today() - timedelta(days=anos*365)).strftime('%d/%m/%Y')
    
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
    
    try:
        resposta = requests.get(url, timeout=10)
        dados = resposta.json()
        
        df = pd.DataFrame(dados)
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        df['valor'] = df['valor'].astype(float)
        df = df.sort_values('data').reset_index(drop=True)
        
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados: {str(e)}")
        return None

series_disponiveis = {
    "1178": {"nome": "Taxa SELIC", "unidade": "% a.a."},
    "433": {"nome": "IPCA", "unidade": "% mês"},
    "1": {"nome": "Dólar Compra", "unidade": "R$"},
    "12": {"nome": "CDI", "unidade": "% a.a."}
}

serie_selecionada = st.selectbox(
    "Indicador Principal",
    options=list(series_disponiveis.keys()),
    format_func=lambda x: series_disponiveis[x]["nome"],
    index=0
)

anos_periodo = st.slider("Período (anos)", min_value=1, max_value=10, value=4, key="anos_slider")

with st.spinner("Carregando dados do Banco Central..."):
    if serie_selecionada == "1178":
        df_principal = buscar_selic(anos=anos_periodo)
    else:
        codigo_serie = int(serie_selecionada)
        data_final = datetime.today().strftime('%d/%m/%Y')
        data_inicial = (datetime.today() - timedelta(days=anos_periodo*365)).strftime('%d/%m/%Y')
        
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
        
        try:
            resposta = requests.get(url, timeout=10)
            dados = resposta.json()
            
            df_principal = pd.DataFrame(dados)
            df_principal['data'] = pd.to_datetime(df_principal['data'], dayfirst=True)
            df_principal['valor'] = df_principal['valor'].astype(float)
            df_principal = df_principal.sort_values('data').reset_index(drop=True)
        except Exception as e:
            st.error(f"Erro ao buscar dados: {str(e)}")
            df_principal = None

if df_principal is not None and not df_principal.empty:
    
    info = series_disponiveis[serie_selecionada]
    
    valor_atual = df_principal['valor'].iloc[-1]
    valor_anterior = df_principal['valor'].iloc[-2] if len(df_principal) > 1 else valor_atual
    variacao = valor_atual - valor_anterior
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            f"{info['nome']} Atual",
            f"{valor_atual:.2f} {info['unidade']}",
            f"{variacao:+.2f}" if variacao != 0 else "—"
        )
    with col2:
        st.metric("Máxima", f"{df_principal['valor'].max():.2f} {info['unidade']}")
    with col3:
        st.metric("Mínima", f"{df_principal['valor'].min():.2f} {info['unidade']}")
        
    st.subheader(f"Evolução: {info['nome']}")
    
    fig_principal = px.line(
        df_principal,
        x='data',
        y='valor',
        title=f"{info['nome']} - Últimos {anos_periodo} anos",
        labels={'valor': info['unidade'], 'data': 'Data'},
        markers=True
    )
    fig_principal.update_traces(line_color='#1e3a8a', line_width=2)
    fig_principal.update_layout(
        hovermode='x unified',
        height=700,
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#e5e7eb'),
        yaxis=dict(showgrid=True, gridcolor='#e5e7eb')
    )
    st.plotly_chart(fig_principal, use_container_width=True)
    
    with st.expander("Ver Dados Completos"):
        df_show = df_principal.copy()
        df_show = df_show.sort_values('data', ascending=True)
        df_show['data'] = df_show['data'].dt.strftime('%d/%m/%Y')
        df_show = df_show.rename(
            columns={'data': 'Data', 'valor': f'Valor ({info["unidade"]})'}
        )
        st.dataframe(df_show, hide_index=True, use_container_width=True)
    
else:
    st.warning("Não foi possível carregar os dados.")

st.divider()
st.markdown("""
    <div style='text-align: center; color: #6b7280; font-size: 0.9em;'>
    Dados oficiais do Banco Central do Brasil | Atualização em tempo real<br>
    API BCB: <a href='https://dadosabertos.bcb.gov.br' target='_blank'>dadosabertos.bcb.gov.br</a>
    </div>
""", unsafe_allow_html=True)