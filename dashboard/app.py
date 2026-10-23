"""Dashboard de vendas do DataShop (Streamlit + Plotly)."""

import sqlite3

import plotly.express as px
import streamlit as st

import dados
from main import formatar_moeda  # reaproveita a formatação em reais do menu

# Paleta: azul-marinho, azul e ciano
AZUL_ESCURO = "#0B2545"
AZUL = "#1D4ED8"
CIANO = "#06B6D4"
CORES_STATUS = {"enviado": AZUL, "pago": CIANO, "pendente": "#93C5FD", "cancelado": "#CBD5E1"}

st.set_page_config(page_title="DataShop | Inteligência de Vendas", page_icon="📊", layout="wide")

# Pequeno ajuste visual: cards brancos com borda lateral ciano
st.markdown(
    f"""
    <style>
    [data-testid="stMetric"] {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid {CIANO};
        border-radius: 10px;
        padding: 14px 18px;
    }}
    [data-testid="stMetricValue"] {{ color: {AZUL_ESCURO}; font-weight: 700; font-size: 1.6rem; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def sem_dados(tabela, titulo):
    """Mostra um aviso no lugar do gráfico quando não há vendas válidas para exibir."""
    if tabela.empty:
        st.info(f"**{titulo}:** sem vendas válidas para os filtros escolhidos.")
        return True
    return False


def grafico_barras(tabela, x, y, titulo, texto, hover):
    """Barra horizontal padrão do dashboard."""
    fig = px.bar(tabela, x=x, y=y, orientation="h", text=texto,
                 color_discrete_sequence=[AZUL], custom_data=hover)
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig = estilizar(fig, titulo)
    # Espaço extra à direita para o rótulo da maior barra; o valor já aparece na barra
    fig.update_xaxes(range=[0, tabela[x].max() * 1.3], showticklabels=False)
    return fig


def estilizar(fig, titulo):
    """Aplica o mesmo visual (fundo, fonte, margens, moeda BR) a todos os gráficos."""
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=16, color=AZUL_ESCURO)),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=30, t=50, b=10), height=340,
        separators=",.",  # vírgula decimal e ponto de milhar
        xaxis_title=None, yaxis_title=None, showlegend=False,
        font=dict(color=AZUL_ESCURO),
    )
    fig.update_xaxes(gridcolor="#EEF2F7")
    return fig


# ---------- Carregamento dos dados ----------
st.title("📊 DataShop | Inteligência de Vendas")
st.caption("Painel de vendas com dados fictícios lidos do banco SQLite do projeto.")



@st.cache_resource  # executa uma única vez por servidor, mesmo com vários acessos
def preparar_banco():
    return dados.garantir_banco()


if not preparar_banco():
    st.error("Não foi possível criar o banco de dados.")
    st.markdown("Crie o banco executando, na pasta do projeto:\n\n"
                "```\npython src/database.py\n```\n\nDepois, recarregue esta página.")
    st.stop()

try:
    itens = dados.carregar_itens()
    total_clientes, total_produtos = dados.contar_cadastros()
except sqlite3.Error as erro:
    st.error(f"Erro ao ler o banco: {erro}")
    st.markdown("Recrie o banco com `python src/database.py` e recarregue a página.")
    st.stop()

# ---------- Filtros (barra lateral) ----------
with st.sidebar:
    st.header("Filtros")
    categorias = sorted(itens["categoria"].unique())
    status = sorted(itens["status"].unique())
    cat_escolhidas = st.multiselect("Categoria", categorias, default=categorias)
    status_escolhidos = st.multiselect("Status do pedido", status, default=status)
    periodo = st.date_input(
        "Período",
        value=(itens["data_pedido"].min().date(), itens["data_pedido"].max().date()),
        format="DD/MM/YYYY",
    )
    st.caption("Pedidos cancelados nunca entram no faturamento nem no ticket médio.")

# O seletor de período devolve só 1 data enquanto o usuário escolhe a segunda
if len(periodo) != 2:
    st.info("Selecione a data final do período.")
    st.stop()

filtrados = dados.filtrar(itens, cat_escolhidas, status_escolhidos, *periodo)
if filtrados.empty:
    st.warning("Nenhum pedido encontrado com esses filtros.")
    st.stop()

# ---------- Indicadores ----------
ind = dados.calcular_indicadores(filtrados)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Faturamento", formatar_moeda(ind["faturamento"]), help="Exclui pedidos cancelados")
c2.metric("Pedidos", ind["total_pedidos"], help=f"{ind['pedidos_cancelados']} cancelado(s) no filtro")
c3.metric("Clientes cadastrados", total_clientes)
c4.metric("Produtos cadastrados", total_produtos)
c5.metric("Ticket médio", formatar_moeda(ind["ticket_medio"]), help="Faturamento ÷ pedidos não cancelados")

st.divider()

# ---------- Gráficos ----------
esq, dir_ = st.columns(2)

with esq:
    tab = dados.faturamento_por_categoria(filtrados)
    if not sem_dados(tab, "Faturamento por categoria"):
        fig = grafico_barras(tab, "valor", "categoria", "Faturamento por categoria",
                             tab["valor"].map(formatar_moeda), ["categoria"])
        fig.update_traces(hovertemplate="%{customdata[0]}<br>R$ %{x:,.2f}<extra></extra>")
        st.plotly_chart(fig, width="stretch")

with dir_:
    tab = dados.pedidos_por_status(filtrados)
    fig = px.pie(tab, names="status", values="pedidos", hole=0.55,
                 color="status", color_discrete_map=CORES_STATUS)
    fig.update_traces(textinfo="label+value",
                      hovertemplate="%{label}: %{value} pedido(s)<extra></extra>")
    st.plotly_chart(estilizar(fig, "Pedidos por status"), width="stretch")

tab = dados.vendas_por_mes(filtrados)
if not sem_dados(tab, "Evolução do faturamento por mês"):
    fig = px.area(tab, x="mes", y="faturamento", markers=True,
                  color_discrete_sequence=[CIANO], custom_data=["pedidos"])
    fig.update_traces(line=dict(width=3),
                      hovertemplate="%{x|%m/%Y}<br>R$ %{y:,.2f}<br>%{customdata[0]} pedido(s)<extra></extra>")
    fig.update_xaxes(dtick="M1", tickformat="%m/%Y")
    fig.update_yaxes(tickprefix="R$ ", gridcolor="#EEF2F7")
    st.plotly_chart(estilizar(fig, "Evolução do faturamento por mês"), width="stretch")

esq, dir_ = st.columns(2)

with esq:
    tab = dados.ranking_clientes(filtrados)
    if not sem_dados(tab, "Clientes que mais compraram"):
        fig = grafico_barras(tab, "total", "cliente", "Clientes que mais compraram",
                             tab["total"].map(formatar_moeda), ["pedidos"])
        fig.update_traces(hovertemplate="%{y}<br>R$ %{x:,.2f}<br>%{customdata[0]} pedido(s)<extra></extra>")
        st.plotly_chart(fig, width="stretch")

with dir_:
    tab = dados.produtos_mais_vendidos(filtrados)
    if not sem_dados(tab, "Produtos mais vendidos"):
        fig = grafico_barras(tab, "quantidade", "produto", "Produtos mais vendidos (unidades)",
                             tab["quantidade"], ["valor"])
        fig.update_traces(marker_color=CIANO,
                          hovertemplate="%{y}<br>%{x} un.<br>R$ %{customdata[0]:,.2f}<extra></extra>")
        st.plotly_chart(fig, width="stretch")

with st.expander("Ver dados detalhados"):
    st.dataframe(
        filtrados.drop(columns="mes").sort_values("data_pedido"),
        hide_index=True, width="stretch",
        column_config={
            "data_pedido": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "preco_unitario": st.column_config.NumberColumn("Preço unit.", format="R$ %.2f"),
            "valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
        },
    )
