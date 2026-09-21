import streamlit as st
import plotly.express as px
import pandas as pd  # Adicionado para corrigir o NameError

df = st.session_state['df']

st.title("📈 Análise de Avaliações dos Usuários")

if df.empty:
    st.warning("Nenhum dado encontrado para a combinação de filtros selecionada.")
else:
    st.subheader("Distribuição das Notas")
    
    df_notas = df.copy()
    df_notas['user_rating_str'] = df_notas['user_rating'].apply(lambda x: 'Sem avaliação' if x == 0 else str(x))
    
    avaliacoes = df_notas['user_rating_str'].value_counts().reset_index()
    avaliacoes.columns = ['Avaliação', 'Quantidade']
    
    ordem_notas = ['Sem avaliação', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5', '5.0']
    avaliacoes['Avaliação'] = pd.Categorical(avaliacoes['Avaliação'], categories=ordem_notas, ordered=True)
    avaliacoes = avaliacoes.sort_values('Avaliação')

    fig1 = px.bar(avaliacoes, x='Avaliação', y='Quantidade', text='Quantidade',
                  template="plotly_dark", color='Quantidade', color_continuous_scale='Purples')
    fig1.update_traces(textposition='outside')
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Volume de Avaliações vs. Nota Final")
    avaliados = df[df['user_rating'] > 0]

    fig2 = px.scatter(avaliados, x='rating_count_tot', y='user_rating', 
                      log_x=True, opacity=0.4, template="plotly_dark",
                      labels={'rating_count_tot': 'Qtd Avaliações (Log)', 'user_rating': 'Nota do Usuário'},
                      hover_name='track_name', hover_data=['prime_genre', 'price'])
    fig2.update_traces(marker=dict(size=10, color='#00f2fe'))
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)
