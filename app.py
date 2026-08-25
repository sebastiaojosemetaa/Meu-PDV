import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(page_title="PDV Web System", layout="wide", page_icon="🛒")

# Estilo visual moderno (Cores e Layout)
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
        .css-1d391kg { background-color: #0f172a; color: white; }
    </style>
""", unsafe_allow_html=True)

# Inicializando dados de produtos e carrinho na sessão
if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {"item": 1, "quantidade": 1, "nome": "Coca Cola 2L", "preco": 13.00, "total": 13.00},
        {"item": 2, "quantidade": 1, "nome": "Abacatinho 2L", "preco": 5.49, "total": 5.49},
        {"item": 3, "quantidade": 1, "nome": "Fanta Uva", "preco": 8.50, "total": 8.50},
        {"item": 4, "quantidade": 1, "nome": "Guaraná", "preco": 2.50, "total": 2.50},
        {"item": 5, "quantidade": 1, "nome": "Beterraba kg", "preco": 2.99, "total": 2.99},
        {"item": 6, "quantidade": 1, "nome": "Banana KG", "preco": 3.99, "total": 3.99},
        {"item": 7, "quantidade": 1, "nome": "Farofa Kikos", "preco": 5.33, "total": 5.33}
    ]

if "carrinho" not in st.session_state:
    st.session_state.carrinho = list(st.session_state.produtos)

# Menu Lateral Estilizado
with st.sidebar:
    st.image("https://img.icons8.com/color/96/shopping-cart--v1.png", width=60)
    st.markdown("### **Sistema de Vendas PDV Web**")
    st.markdown("---")
    
    selected = option_menu(
        "Menu Principal",
        ["Dashboard", "Produto", "PDV", "Vendas", "Swagger", "API", "APP", "CoreUI Doc", "Angular Material", "Sobre"],
        icons=['house', 'box-seam', 'cart-check', 'receipt', 'code-slash', 'hdd-network', 'phone', 'file-text', 'layers', 'info-circle'],
        menu_icon="cast", default_index=2,
    )

# Lógica das Telas
if selected == "PDV":
    st.markdown("### **Home / Produtos / PDV**")
    
    # Cabeçalho da Venda com Botões de Ação
    col_topo1, col_topo2 = st.columns([8, 2])
    with col_topo1:
        st.markdown("## **Venda em Aberto**")
    with col_topo2:
        btn_limpar = st.button("🗑️ Limpar", type="secondary")
        btn_salvar = st.button("💾 Salvar", type="primary")

    if btn_limpar:
        st.session_state.carrinho = []
        st.rerun()

    # Layout Principal dividindo a tabela de itens e o painel de lançamento
    col_esq, col_dir = st.columns([7, 3])

    with col_esq:
        if st.session_state.carrinho:
            df_vendas = pd.DataFrame(st.session_state.carrinho)
            # Exibe a tabela formatada no padrão limpo
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
                <div style="background-color: #f1f3f5; padding: 15px; border-radius: 8px; text-align: right; margin-top: 15px;">
                    <span style="font-size: 20px; font-weight: bold; color: #212529;">Valor total a pagar: R$ {total_geral:.2f}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Nenhum item na venda atual.")

    with col_dir:
        st.markdown("#### 🛒 Painel de Lançamento")
        with st.container():
            st.markdown("---")
            codigo_produto = st.text_input("Código do produto", value="10")
            qtd_produto = st.number_input("Quantidade", min_value=1, value=1)
            
            # Espaçamento e Botão de inclusão estilizado igual ao print
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("+ Incluir Produto", type="primary", use_container_width=True):
                novo_item = {
                    "item": len(st.session_state.carrinho) + 1,
                    "quantidade": qtd_produto,
                    "nome": f"Produto Ref. {codigo_produto}",
                    "preco": 15.00,
                    "total": 15.00 * qtd_produto
                }
                st.session_state.carrinho.append(novo_item)
                st.success("Adicionado!")
                st.rerun()

elif selected == "Dashboard":
    st.markdown("## 📊 Dashboard de Vendas")
    st.success("Bem-vindo ao painel gerencial do sistema.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Vendas Hoje", "R$ 1.250,00", "+12%")
    col2.metric("Itens Vendidos", "48", "+5")
    col3.metric("Clientes Atendidos", "14", "0")

elif selected == "Produto":
    st.markdown("## 📦 Gerenciamento de Produtos")
    st.dataframe(pd.DataFrame(st.session_state.produtos), use_container_width=True)

else:
    st.markdown(f"## ⚙️ Seção: {selected}")
    st.write("Esta área está integrada ao seu ambiente web na nuvem.")
