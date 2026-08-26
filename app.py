import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(page_title="PDV Web — Sistema de Vendas", layout="wide", initial_sidebar_state="expanded")

# Estilo visual limpo (Tema Claro)
st.markdown("""
    <style>
        .stApp { background-color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #2D3748; color: white; }
        [data-testid="stSidebar"] span { color: #E2E8F0; }
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label { color: #E2E8F0; }
        h1, h2, h3, h4, h5, h6 { color: #1A202C; }
        p, div { color: #2D3748; }
        div[data-testid="stDataFrame"] table { border: 1px solid #E2E8F0; border-radius: 4px; }
        div[data-testid="stDataFrame"] th { background-color: #F7FAFC; color: #1A202C; font-weight: bold; }
        .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #F7FAFC; color: #718096; text-align: center; padding: 10px; font-size: 14px; border-top: 1px solid #E2E8F0; z-index: 100; }
    </style>
""", unsafe_allow_html=True)

# Estados globais da sessão
if "carrinho" not in st.session_state:
    st.session_state.carrinho = [
        {"item": 1, "quantidade": 1, "nome": "Coca Cola 2L", "preco": 13.00, "total": 13.00},
        {"item": 2, "quantidade": 1, "nome": "Abacatinho 2L", "preco": 5.49, "total": 5.49},
        {"item": 3, "quantidade": 1, "nome": "Fanta Uva", "preco": 8.50, "total": 8.50},
        {"item": 4, "quantidade": 1, "nome": "Guaraná", "preco": 2.50, "total": 2.50}
    ]

if "lista_produtos" not in st.session_state:
    st.session_state.lista_produtos = [
        {"Código": 1, "Produto": "Coca Cola 2L", "Preço": 13.00, "Estoque": 50},
        {"Código": 2, "Produto": "Abacatinho 2L", "Preço": 5.49, "Estoque": 30},
        {"Código": 3, "Produto": "Fanta Uva", "Preço": 8.50, "Estoque": 40},
        {"Código": 4, "Produto": "Guaraná", "Preço": 2.50, "Estoque": 60},
        {"Código": 10, "Produto": "Produto Ref. 10", "Preço": 19.90, "Estoque": 100}
    ]

# Menu Lateral
with st.sidebar:
    st.markdown("<h3><b>Administração / PDV Web</b></h3>", unsafe_allow_html=True)
    st.markdown("---")
    selected = option_menu(
        None,
        ["Dashboard", "Produto", "PDV", "Vendas", "Swagger", "API", "APP", "CoreUI Doc", "Angular Material", "Sobre"],
        icons=['house', 'box-seam', 'cart-check', 'receipt', 'code-slash', 'hdd-network', 'phone', 'file-text', 'layers', 'info-circle'],
        menu_icon="cast", default_index=3,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#A0AEC0", "font-size": "16px"}, 
            "nav-link": {"color": "#E2E8F0", "font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#4A5568"},
            "nav-link-selected": {"background-color": "#3B82F6", "color": "white"},
        }
    )

# Conteúdo de cada tela
if selected == "Dashboard":
    st.markdown("<h2>📊 Dashboard Geral</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Vendas Hoje", "R$ 1.250,00", "+12%")
    col2.metric("Produtos Cadastrados", len(st.session_state.lista_produtos))
    col3.metric("Clientes Atendidos", "14")

elif selected == "Produto":
    st.markdown("<h2>📦 Cadastro e Gestão de Produtos</h2>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.lista_produtos), use_container_width=True, hide_index=True)
    
    with st.form("form_novo_produto"):
        st.markdown("#### Adicionar Novo Produto")
        novo_cod = st.number_input("Código", min_value=1, value=len(st.session_state.lista_produtos)+1)
        novo_nome = st.text_input("Nome do Produto")
        novo_preco = st.number_input("Preço (R$)", min_value=0.0, value=10.0)
        novo_est = st.number_input("Estoque Inicial", min_value=1, value=10)
        
        if st.form_submit_button("Cadastrar Produto"):
            st.session_state.lista_produtos.append({"Código": novo_cod, "Produto": novo_nome, "Preço": novo_preco, "Estoque": novo_est})
            st.success(f"Produto '{novo_nome}' cadastrado com sucesso!")
            st.rerun()

elif selected == "PDV":
    st.markdown("Home / Produtos / **PDV**")
    c1, c2, c3 = st.columns([5, 2, 2])
    with c1:
        st.markdown("<h2><b>Venda em Aberto</b></h2>", unsafe_allow_html=True)
    with c2:
        if st.button("🗑️ Limpar", type="secondary"):
            st.session_state.carrinho = []
            st.rerun()
    with c3:
        if st.button("💾 Salvar", type="primary"):
            st.success("Venda salva com sucesso!")

    col_tab, col_lanca = st.columns([7, 3])
    with col_tab:
        if st.session_state.carrinho:
            df_vendas = pd.DataFrame(st.session_state.carrinho)
            st.dataframe(df_vendas, column_config={"preco": st.column_config.NumberColumn("Preço", format="R$ %.2f"), "total": st.column_config.NumberColumn("Total", format="R$ %.2f")}, hide_index=True, use_container_width=True)
            total_geral = sum(i["total"] for i in st.session_state.carrinho)
            st.markdown(f'<div style="background-color: #EDF2F7; padding: 15px; border-radius: 4px; text-align: right; margin-top: 10px;"><span style="font-size: 22px; font-weight: bold; color: #1A202C;">Valor total a pagar: R$ {total_geral:.2f}</span></div>', unsafe_allow_html=True)
        else:
            st.info("A venda está vazia.")

    with col_lanca:
        st.markdown("<h4>🛒 <b>Painel de Lançamento</b></h4>", unsafe_allow_html=True)
        with st.container():
            st.markdown("---")
            codigo_produto = st.text_input("Código do produto", value="10")
            qtd_produto = st.number_input("Quantidade", min_value=1, value=1)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("+ Incluir Produto", type="primary", use_container_width=True):
                st.session_state.carrinho.append({"item": len(st.session_state.carrinho)+1, "quantidade": qtd_produto, "nome": f"Produto Ref. {codigo_produto}", "preco": 19.90, "total": 19.90 * qtd_produto})
                st.rerun()

elif selected == "Vendas":
    st.markdown("<h2>🧾 Histórico de Vendas Realizadas</h2>", unsafe_allow_html=True)
    vendas_exemplo = pd.DataFrame([
        {"ID Venda": 101, "Cliente": "Carlos Alberto", "Itens": 3, "Total": 45.50, "Data": "24/08/2026"},
        {"ID Venda": 102, "Cliente": "Maria Silva", "Itens": 1, "Total": 13.00, "Data": "24/08/2026"}
    ])
    st.dataframe(
        vendas_exemplo, 
        column_config={"Total": st.column_config.NumberColumn("Total", format="R$ %.2f")},
        use_container_width=True, 
        hide_index=True
    )

elif selected == "Swagger":
    st.markdown("<h2>🔌 Documentação da API (Swagger)</h2>", unsafe_allow_html=True)
    st.info("Endpoints ativos para integração externa do PDV.")
    st.code("GET /api/v1/produtos\nPOST /api/v1/vendas\nGET /api/v1/estoque", language="json")

elif selected == "API":
    st.markdown("<h2>🌐 Status da API</h2>", unsafe_allow_html=True)
    st.success("API Online e operando na nuvem com resposta de 14ms.")

elif selected == "APP":
    st.markdown("<h2>📱 Versão Mobile / App</h2>", unsafe_allow_html=True)
    st.write("Acesse o sistema responsivo direto pelo navegador do seu smartphone usando o mesmo link.")

elif selected == "CoreUI Doc":
    st.markdown("<h2>📄 Documentação CoreUI</h2>", unsafe_allow_html=True)
    st.write("Padrão de componentes visuais integrados ao layout web.")

elif selected == "Angular Material":
    st.markdown("<h2>🎨 Angular Material & Componentes</h2>", unsafe_allow_html=True)
    st.write("Referências de design adaptadas para a interface leve em Python.")

else:
    st.markdown("<h2>ℹ️ Sobre o Sistema</h2>", unsafe_allow_html=True)
    st.write("PDV Web desenvolvido para alta performance em nuvem sem consumo local de hardware.")

st.markdown('<div class="footer">© 2026 PDV Web — Sistema de Vendas — Tema Claro V2</div>', unsafe_allow_html=True)
