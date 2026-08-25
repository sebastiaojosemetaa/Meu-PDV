import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Configuração da página - TEMA CLARO
st.set_page_config(page_title="PDV Web — Sistema de Vendas", layout="wide", initial_sidebar_state="expanded")

# Estilo visual customizado (CSS) para o tema claro (Clean e Profissional)
st.markdown("""
    <style>
        /* Fundo principal */
        .stApp { background-color: #FFFFFF; }
        
        /* Barra Lateral (Sidebar) - Azul Escuro */
        [data-testid="stSidebar"] { background-color: #2D3748; color: white; }
        [data-testid="stSidebar"] span { color: #E2E8F0; }
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label { color: #E2E8F0; }
        
        /* Títulos e Textos Gerais */
        h1, h2, h3, h4, h5, h6 { color: #1A202C; font-family: sans-serif; }
        p, div { color: #2D3748; }

        /* Tabela */
        div[data-testid="stDataFrame"] table { border: 1px solid #E2E8F0; border-radius: 4px; }
        div[data-testid="stDataFrame"] th { background-color: #F7FAFC; color: #1A202C; font-weight: bold; }
        div[data-testid="stDataFrame"] td { color: #4A5568; }

        /* Botões */
        .stButton>button { font-weight: bold; border-radius: 4px; }
        .stButton>button[kind="primary"] { background-color: #3B82F6; color: white; border: none; }
        .stButton>button[kind="secondary"] { background-color: #E2E8F0; color: #4A5568; border: 1px solid #CBD5E0; }
        
        /* Inputs e Fields */
        div[data-testid="stTextInput"] input { border: 1px solid #CBD5E0; border-radius: 4px; }
        div[data-testid="stNumberInput"] input { border: 1px solid #CBD5E0; border-radius: 4px; }
        
        /* Caixas de Informação (Success, Info, Warning) */
        .stSuccess { background-color: #C6F6D5; color: #2F855A; border: none; }
        .stInfo { background-color: #EBF8FF; color: #2B6CB0; border: none; }

        /* Rodapé */
        .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #F7FAFC; color: #718096; text-align: center; padding: 10px; font-size: 14px; border-top: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# Inicializando dados do carrinho na sessão (Produtos de exemplo da imagem)
if "carrinho" not in st.session_state:
    st.session_state.carrinho = [
        {"item": 8, "quantidade": 1, "nome": "Coca Cola 2L", "preco": 13.00, "total": 13.00},
        {"item": 8, "quantidade": 1, "nome": "Abacatinho 2L", "preco": 5.49, "total": 5.49},
        {"item": 8, "quantidade": 1, "nome": "Fanta Uva", "preco": 8.50, "total": 8.50},
        {"item": 8, "quantidade": 1, "nome": "Fanta Uva", "preco": 8.50, "total": 8.50},
        {"item": 8, "quantidade": 1, "nome": "Guaraná", "preco": 2.50, "total": 2.50},
        {"item": 8, "quantidade": 1, "nome": "Beterraba kg", "preco": 2.99, "total": 2.99},
        {"item": 8, "quantidade": 1, "nome": "Banana KG", "preco": 3.99, "total": 3.99},
        {"item": 8, "quantidade": 1, "nome": "Farofa Kikos", "preco": 5.33, "total": 5.33}
    ]

# Menu Lateral Estilizado (Visual Claro)
with st.sidebar:
    st.markdown("### **Administração / PDV Web**")
    st.markdown("---")
    
    # Usando o option-menu com cores claras customizadas pelo CSS
    selected = option_menu(
        None,
        ["Dashboard", "Produto", "PDV", "Vendas", "Swagger", "API", "APP", "CoreUI Doc", "Angular Material", "Sobre"],
        icons=['house', 'box-seam', 'cart-check', 'receipt', 'code-slash', 'hdd-network', 'phone', 'file-text', 'layers', 'info-circle'],
        menu_icon="cast", default_index=2,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#A0AEC0", "font-size": "16px"}, 
            "nav-link": {"color": "#E2E8F0", "font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#4A5568"},
            "nav-link-selected": {"background-color": "#3B82F6", "color": "white", "font-weight": "normal"},
        }
    )

# Lógica das Telas (Visual Claro)
if selected == "PDV":
    st.markdown("Home / Produtos / **PDV**")
    
    # Cabeçalho da Venda com Botões de Ação
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

    # Layout Principal (Tabela e Lançamento)
    col_tab, col_lanca = st.columns([7, 3])

    with col_tab:
        if st.session_state.carrinho:
            df_vendas = pd.DataFrame(st.session_state.carrinho)
            # Tabela formatada (Tema claro)
            st.dataframe(
                df_vendas, 
                column_config={
                    "item": "Item",
                    "quantidade": "Quantidade",
                    "nome": "Nome",
                    "preco": st.column_config.NumberColumn("Preço", format="R$ %.2f"),
                    "total": st.column_config.NumberColumn("Total", format="R$ %.2f")
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Valor Total geral
            total_geral = sum(i["total"] for i in st.session_state.carrinho)
            st.markdown(f"""
                <div style="background-color: #EDF2F7; padding: 15px; border-radius: 4px; text-align: right; margin-top: 10px;">
                    <span style="font-size: 22px; font-weight: bold; color: #1A202C;">Valor total a pagar: R$ {total_geral:.2f}</span>
                </div>
            """, unsafe_allow_html=True)
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
                # Adiciona um produto genérico com base nos inputs
                novo_item = {
                    "item": 8, # Mantendo o '8' como na imagem de exemplo
                    "quantidade": qtd_produto,
                    "nome": f"Produto Ref. {codigo_produto}",
                    "preco": 19.90, # Preço de exemplo novo
                    "total": 19.90 * qtd_produto
                }
                st.session_state.carrinho.append(novo_item)
                st.rerun()

elif selected == "Dashboard":
    st.markdown("<h2>📊 📊 Dashboard Geral</h2>", unsafe_allow_html=True)
    st.info("Esta é a tela de dashboard no tema claro.")
else:
    st.markdown(f"<h2>⚙️ Seção: {selected}</h2>", unsafe_allow_html=True)
    st.write("Área em desenvolvimento no tema claro.")

# Rodapé fixo
st.markdown('<div class="footer">© 2024 PDV Web — Sistema de Vendas — Tema Claro V1</div>', unsafe_allow_html=True)
