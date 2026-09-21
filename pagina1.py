import streamlit as st
import plotly.express as px

df = st.session_state['df']

st.title("📊 Visão Geral do Mercado de Apps")
st.write(f"Exibindo dados para **{len(df)}** aplicativos com base nos filtros selecionados.")

if df.empty:
    st.warning("Nenhum dado encontrado para a combinação de filtros selecionada.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Categorias")
        top_10 = df['prime_genre'].value_counts().head(10).reset_index()
        top_10.columns = ['Categoria', 'Quantidade']
        top_10 = top_10.sort_values(by='Quantidade')
        
        fig1 = px.bar(top_10, x='Quantidade', y='Categoria', orientation='h',
                      text='Quantidade', template="plotly_dark",
                      color='Quantidade', color_continuous_scale='Blues')
        fig1.update_traces(textposition='outside')
        fig1.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Modelos de Preço")
        tipo_preco = df['tipo_preco'].value_counts().reset_index()
        tipo_preco.columns = ['Tipo', 'Quantidade']
        
        fig2 = px.pie(tipo_preco, values='Quantidade', names='Tipo', 
                      template="plotly_dark", hole=0.4,
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
