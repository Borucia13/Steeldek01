
import streamlit as st
import pandas as pd
import cx_Oracle as cx
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Analise de Valores pagos: ')
st.write('Média dos valores pagos, por liga, data, espessura e ICMS')

#st.caption('POR DATA E LIGA')

connection = cx.connect('STEELDEK/STEELDEKBD2021@192.168.0.102:1521/AWORKSDB')
cursor = connection.cursor()

opcao = st.sidebar.radio("Selecione uma Liga:",
                ("201", "304", "430", "EN"),index=1 )

agora = dt.date.today()
hoje = agora.strftime("%d/%m/%Y")
antes = agora.replace(day=1)
antes = antes.replace(month=agora.month-1)
antes_str = antes.strftime("%d/%m/%Y")


if opcao == "201":
    LIGA = "201"
elif opcao == "304":
    LIGA = "304"
elif opcao == "430":
    LIGA = "430"
else:
    LIGA = "1803"


DATAINI = st.sidebar.text_input("DIGITE A DATA INICIAL:", antes_str)
DATAFIN = st.sidebar.text_input("DIGITE A DATA FINAL:", hoje)



QUERY = """SELECT CASE
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%040%' THEN '040-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%040%' THEN '040-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%050%' THEN '050-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%050%' THEN '050-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%060%' THEN '060-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%060%' THEN '060-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%080%' THEN '080-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%080%' THEN '080-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%100%' THEN '100-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%100%' THEN '100-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%120%' THEN '120-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%120%' THEN '120-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%150%' THEN '150-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%150%' THEN '150-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%200%' THEN '200-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%200%' THEN '200-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%250%' THEN '200-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%250%' THEN '200-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%300%' THEN '300-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%300%' THEN '300-IMPORTADO'
    ELSE 'OUTROS'
END AS TIPO_PRODUTO,
TRUNC(AVG(IC.VL_UNITARIO_ITEMPEDIDOCOMPRA),2) AS MÉDIA
FROM SEVEN.PEDIDOCOMPRA OC,
    SEVEN.ITEMPEDIDOCOMPRA IC, 
    SEVEN.PRODUTO P, 
    SEVEN.SUBGRUPOPRODUTO SB
WHERE IC.PEDIDOCOMPRAID = OC.PEDIDOCOMPRAID 
AND OC.DT_PEDIDOCOMPRA BETWEEN to_date( '""" + DATAINI + """', 'dd/mm/yyyy') and to_date( '""" + DATAFIN + """', 'dd/mm/yyyy')
AND IC.PRODUTOID = P.PRODUTOID
AND P.SUBGRUPOPRODUTOID = SB.SUBGRUPOPRODUTOID
AND SB.NOME_SUBGRUPOPRODUTO LIKE '%CHAPA%""" + LIGA + """%SP%'
AND P.REFERENCIA_PRODUTO LIKE '%%'
GROUP BY CASE
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%040%' THEN '040-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%040%' THEN '040-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%050%' THEN '050-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%050%' THEN '050-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%060%' THEN '060-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%060%' THEN '060-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%080%' THEN '080-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%080%' THEN '080-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%100%' THEN '100-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%100%' THEN '100-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%120%' THEN '120-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%120%' THEN '120-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%150%' THEN '150-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%150%' THEN '150-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%200%' THEN '200-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%200%' THEN '200-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%250%' THEN '200-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%250%' THEN '200-IMPORTADO'
    WHEN p.referencia_produto like '%SN' AND p.referencia_produto like '%300%' THEN '300-NACIONAL'
    WHEN p.referencia_produto like '%SI' AND p.referencia_produto like '%300%' THEN '300-IMPORTADO'
    ELSE 'OUTROS'
END 
ORDER BY 1"""

cursor.execute(QUERY)
rows = cursor.fetchall()

valores = pd.DataFrame( 
    rows,
     columns=['PRODUTO','VALOR PAGO']
)

qntd_linhas = st.sidebar.slider('Selecione a quantidade de linhas que deseja mostrar na tabela', min_value = 1, max_value = len(rows), step = 1)

def plot_valores(dataframe):

    dados_plot = dataframe

    fig, ax = plt.subplots(figsize=(10,8))
    ax = sns.barplot(x = 'PRODUTO', y = 'VALOR PAGO', data = dados_plot)
    ax.set_title(f'Valores Pagos por Produto', fontsize = 14)
    ax.set_xlabel('PRODUTO', fontsize = 11)
    ax.tick_params(rotation = 20, axis = 'x')
    ax.set_ylabel('VALOR PAGO', fontsize = 11)
  
    return fig
#exibição de dados

if st.sidebar.button ("Trazer Dados"):  


    #st.dataframe(valores)

    st.write(valores.head(qntd_linhas).style.format(subset = ['VALOR PAGO'], formatter="{:.2f}"))

    st.sidebar.markdown('## Filtro para o gráfico')

    figura = plot_valores(valores)

    st.pyplot(figura)

cursor.close()
connection.close()