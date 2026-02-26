import streamlit as st
from database import get_connection
from datetime import datetime

st.set_page_config(
    page_title="Viveiro de Mudas",
    page_icon="🌱",
    layout="centered"
)

st.title("🌳 Viveiro de Mudas Florestais")

conn = get_connection()
cursor = conn.cursor()

# =============================
# MENU
# =============================
menu = st.radio(
    "O que você quer fazer?",
    ["🌱 Espécie", "📦 Lote", "🧪 Qualidade", "📊 Estoque"]
)

# =============================
# ESPÉCIE
# =============================
if menu == "🌱 Espécie":

    st.header("Nova Espécie")

    nome_popular = st.text_input("Nome popular")
    nome_cientifico = st.text_input("Nome científico")

    if st.button("Salvar espécie"):
        if nome_popular and nome_cientifico:
            cursor.execute("""
                INSERT INTO especies 
                (nome_popular, nome_cientifico)
                VALUES (%s, %s)
            """, (nome_popular, nome_cientifico))

            conn.commit()
            st.success("Espécie cadastrada com sucesso!")
        else:
            st.warning("Preencha todos os campos")

# =============================
# LOTE
# =============================
elif menu == "📦 Lote":

    st.header("Novo Lote")

    cursor.execute("SELECT id, nome_popular FROM especies")
    especies = cursor.fetchall()

    if not especies:
        st.warning("Cadastre uma espécie primeiro.")
    else:

        especie = st.selectbox(
            "Espécie",
            especies,
            format_func=lambda x: x[1]
        )

        codigo_lote = st.text_input("Código do lote")
        quantidade = st.number_input("Quantidade", min_value=1)
        data_semeadura = st.date_input("Data da semeadura")
        status = st.selectbox("Status", ["Em produção", "Pronto", "Descartado"])

        if st.button("Salvar lote"):

            cursor.execute("""
                INSERT INTO lotes
                (especie_id, codigo_lote, quantidade, data_semeadura, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                especie[0],
                codigo_lote,
                quantidade,
                data_semeadura,
                status
            ))

            conn.commit()
            st.success("Lote cadastrado!")

# =============================
# QUALIDADE
# =============================
elif menu == "🧪 Qualidade":

    st.header("Avaliação de Qualidade")

    cursor.execute("""
        SELECT lotes.id, lotes.codigo_lote
        FROM lotes
    """)
    lotes = cursor.fetchall()

    if not lotes:
        st.warning("Cadastre um lote antes.")
    else:

        lote = st.selectbox(
            "Lote",
            lotes,
            format_func=lambda x: x[1]
        )

        altura = st.number_input("Altura (cm)", min_value=0.0)
        diametro = st.number_input("Diâmetro (mm)", min_value=0.0)
        sanidade = st.selectbox("Sanidade", ["Boa", "Regular", "Ruim"])
        vigor = st.selectbox("Vigor", ["Alto", "Médio", "Baixo"])

        if st.button("Calcular e salvar"):

            nota = 0

            if altura >= 30:
                nota += 3
            if diametro >= 3:
                nota += 3

            nota += {"Boa": 2, "Regular": 1, "Ruim": 0}[sanidade]
            nota += {"Alto": 2, "Médio": 1, "Baixo": 0}[vigor]

            classificacao = (
                "A" if nota >= 8 else
                "B" if nota >= 6 else
                "C" if nota >= 4 else
                "Reprovada"
            )

            cursor.execute("""
                INSERT INTO qualidade
                (lote_id, altura, diametro, sanidade, vigor, nota, classificacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                lote[0],
                altura,
                diametro,
                sanidade,
                vigor,
                nota,
                classificacao
            ))

            conn.commit()
            st.success(f"Nota {nota} - Classificação {classificacao}")

# =============================
# ESTOQUE
# =============================
elif menu == "📊 Estoque":

    st.header("Estoque")

    cursor.execute("""
        SELECT 
            lotes.id,
            lotes.codigo_lote,
            especies.nome_popular,
            lotes.quantidade
        FROM lotes
        JOIN especies ON especies.id = lotes.especie_id
    """)

    lotes = cursor.fetchall()

    if not lotes:
        st.warning("Nenhum lote cadastrado.")
    else:

        lote = st.selectbox(
            "Selecione o lote",
            lotes,
            format_func=lambda x: f"{x[1]} - {x[2]} (Estoque: {x[3]})"
        )

        st.write(f"Estoque atual: {lote[3]} mudas")

        qtd_saida = st.number_input(
            "Quantidade de saída",
            min_value=1,
            max_value=lote[3]
        )

        motivo = st.selectbox(
            "Motivo",
            ["Plantio", "Venda", "Doação", "Descarte"]
        )

        if st.button("Registrar saída"):

            novo_estoque = lote[3] - qtd_saida

            cursor.execute(
                "UPDATE lotes SET quantidade = %s WHERE id = %s",
                (novo_estoque, lote[0])
            )

            cursor.execute("""
                INSERT INTO movimentacoes
                (lote_id, tipo, quantidade, motivo)
                VALUES (%s, %s, %s, %s)
            """, (
                lote[0],
                "Saída",
                qtd_saida,
                motivo
            ))

            conn.commit()
            st.success("Saída registrada com sucesso!")