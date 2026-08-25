import streamlit as st
import pandas as pd

st.set_page_config(page_title="PDV — Frente de Caixa", layout="wide", page_icon="🛒")

st.title("🛒 PDV — Frente de Caixa (Múltiplos Produtos)")
st.warning("⚠️ Atenção: Não há nenhum caixa aberto no momento.")

# Menu Lateral
st.sidebar.title("Acesso ao Sistema")
menu = st.sidebar.radio("Navegação", [
    "PDV — Frente de Caixa", 
    "Abertura e Fechamento de Caixa", 
    "Estoque de Produtos", 
    "Cadastros"
])

if "produtos" not in st.session_state:
    st.session_state.produtos = [
        {"nome": "ABACATE", "fornecedor": "BAHIA", "grupo": "FRUTAS", "preco": 117.00, "estoque": 15},
        {"nome": "ARROZ 5KG", "fornecedor": "TIO JOÃO", "grupo": "GRÃOS", "preco": 28.50, "estoque": 30}
    ]

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if menu == "PDV — Frente de Caixa":
    st.header("⚡ Frente de Caixa (PDV)")
    cliente = st.selectbox("Cliente do Atendimento", ["Carlos Alberto", "Maria Silva", "Cliente Balcão"])
    
    nomes_produtos = [p["nome"] for p in st.session_state.produtos]
    produto_escolhido = st.selectbox("Produto", nomes_produtos)
    prod_obj = next(p for p in st.session_state.produtos if p["nome"] == produto_escolhido)
    
    quantidade = st.number_input("Quantidade", min_value=1.0, value=1.0, step=1.0)
    preco_venda = st.number_input("Preço de Venda (R$)", value=float(prod_obj["preco"]), step=1.0)
    
    total_item = quantidade * preco_venda
    st.info(f"**Total do Item:** R$ {total_item:.2f}")
    
    if st.button("Incluir Produto ao Carrinho", type="primary"):
        st.session_state.carrinho.append({
            "Cliente": cliente,
            "Produto": prod_obj["nome"],
            "Quantidade": quantidade,
            "Preço Un.": preco_venda,
            "Total": total_item
        })
        st.success("Item adicionado com sucesso!")

    st.subheader("📦 Itens no Carrinho")
    if st.session_state.carrinho:
        df_carrinho = pd.DataFrame(st.session_state.carrinho)
        st.dataframe(df_carrinho, use_container_width=True)
        
        total_geral = sum(item["Total"] for item in st.session_state.carrinho)
        st.markdown(f"### 💰 Total a Pagar: R$ {total_geral:.2f}")
        
        if st.button("Finalizar Venda"):
            st.success("Venda finalizada com sucesso!")
            st.session_state.carrinho = []
            st.rerun()
    else:
        st.write("Carrinho vazio.")

elif menu == "Estoque de Produtos":
    st.header("📦 Estoque")
    st.dataframe(pd.DataFrame(st.session_state.produtos), use_container_width=True)

elif menu == "Abertura e Fechamento de Caixa":
    st.header("🔒 Controle de Caixa")
    st.radio("Status Atual", ["Fechado", "Aberto"])

elif menu == "Cadastros":
    st.header("📝 Cadastrar Produto")
    novo_nome = st.text_input("Nome do Produto")
    novo_preco = st.number_input("Preço (R$)", min_value=0.0, value=10.0)
    if st.button("Salvar"):
        if novo_nome:
            st.session_state.produtos.append({"nome": novo_nome.upper(), "fornecedor": "GERAL", "grupo": "GERAL", "preco": novo_preco, "estoque": 10})
            st.success("Cadastrado com sucesso!")
