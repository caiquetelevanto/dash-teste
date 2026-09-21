import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Apple Store", layout="wide")

@st.cache_data
def carregar_dados():
    caminho_csv = r"c:\Users\Pichau\Desktop\Coisas de estudar\sql\appstore\AppleStore.csv"
    df = pd.read_csv(caminho_csv)
    df['tipo_preco'] = df['price'].apply(lambda x: 'Gratuito' if x == 0 else 'Pago')
    return df

# Inicializa o dataframe original na sessão
if 'df_original' not in st.session_state:
    st.session_state['df_original'] = carregar_dados()

df_orig = st.session_state['df_original']

# --- CRIANDO OS FILTROS NA BARRA LATERAL ---
st.sidebar.header("🎯 Filtros do Dashboard")

# Filtro 1: Tipo de Preço
opcoes_preco = ['Todos'] + list(df_orig['tipo_preco'].unique())
filtro_preco = st.sidebar.selectbox("Selecione o Modelo de Preço:", opcoes_preco)

# Filtro 2: Categorias
opcoes_categoria = ['Todas'] + sorted(list(df_orig['prime_genre'].unique()))
filtro_categoria = st.sidebar.multiselect("Selecione as Categorias:", opcoes_categoria, default=['Todas'])

# Aplicando a lógica dos filtros
df_filtrado = df_orig.copy()

if filtro_preco != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['tipo_preco'] == filtro_preco]

if 'Todas' not in filtro_categoria and len(filtro_categoria) > 0:
    df_filtrado = df_filtrado[df_filtrado['prime_genre'].isin(filtro_categoria)]

# Guarda o dataframe FILTRADO para as páginas usarem
st.session_state['df'] = df_filtrado

# Configuração das Páginas
pg1 = st.Page("pagina1.py", title="📊 Visão Geral", default=True)
pg2 = st.Page("pagina2.py", title="📈 Análise de Avaliações")

pg = st.navigation([pg1, pg2])
pg.run()
