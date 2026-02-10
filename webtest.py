import streamlit as st
from frota import Frota
from veiculo import Veiculo
from carro import Carro
from mota import Mota

st.set_page_config(page_title="Gestão de Frota", layout="centered")
st.title("🚗 Gestão de Frota")

# -----------------------------
# STATE (load only once)
# -----------------------------
if "frota" not in st.session_state:
    st.session_state.frota = Frota()
    st.session_state.cor = "#FFFFFF"

frota = st.session_state.frota

# =============================
# TABS
# =============================
tab_add, tab_frota = st.tabs(["➕ Adicionar veículo", "📋 Frota"])

# =====================================================
# TAB 1 — ADD VEHICLE
# =====================================================
with tab_add:
    st.header("Novo veículo")

    tipo = st.selectbox(
        "Tipo",
        ["Veiculo", "Carro", "Mota"],
        key="tipo"
    )

    marca = st.text_input("Marca", key="marca_add")
    modelo = st.text_input("Modelo", key="modelo_add")
    preco = st.number_input("Preço (€)", min_value=0.0, step=0.1, key="preco_add")
    vel = st.number_input("Velocidade (km/h)", min_value=0, step=1, key="vel_add")

    combustivel = st.selectbox(
        "Combustível",
        ["Gasolina", "Gasóleo"],
        key="comb_add"
    )

    # ---- Carro elétrico
    eletrico = False
    consumo = None

    if tipo == "Carro":
        eletrico = st.checkbox("Elétrico", key="eletrico_check")
        if eletrico:
            consumo = st.number_input(
                "Consumo (kWh/100km)",
                min_value=0.0,
                step=0.1,
                key="consumo_add"
            )
            combustivel = "Elétrico"

    # ---- Mota
    cilindrada = None
    if tipo == "Mota":
        cilindrada = st.number_input(
            "Cilindrada (cc)",
            min_value=0,
            step=50,
            key="cilindrada_add"
        )

    # ---- Color picker
    st.session_state.cor = st.color_picker(
        "Cor do veículo",
        st.session_state.cor,
        key="cor_picker"
    )

    if st.button("Adicionar veículo", key="btn_add"):
        try:
            if tipo == "Carro":
                v = Carro(
                    marca, modelo, preco, vel, combustivel, st.session_state.cor,
                    eletrico=eletrico,
                    consumo_kwh=consumo
                )
            elif tipo == "Mota":
                v = Mota(
                    marca, modelo, preco, vel, combustivel,
                    st.session_state.cor, cilindrada
                )
            else:
                v = Veiculo(
                    tipo="Veiculo",
                    marca=marca,
                    modelo=modelo,
                    preco=preco,
                    vel=vel,
                    combustivel=combustivel,
                    cor=st.session_state.cor
                )

            frota.adicionar_veiculo(v)
            frota.criarFicheiro()
            st.success("✅ Veículo adicionado com sucesso!")

        except Exception as e:
            st.error(f"Erro ao adicionar veículo: {e}")

# =====================================================
# TAB 2 — FROTA (/frota)
# =====================================================
with tab_frota:
    st.header("Frota")

    # -------------------------
    # FILTER BY BRAND
    # -------------------------
    st.subheader("🔍 Filtrar por marca")

    marca_filtro = st.text_input("Marca", key="marca_filtro")

    if marca_filtro:
        veiculos = frota.filtrar_por_marca(marca_filtro)
    else:
        veiculos = frota.veiculos

    # -------------------------
    # LIST VEHICLES
    # -------------------------
    if not veiculos:
        st.info("Nenhum veículo encontrado.")
    else:
        for i, v in enumerate(veiculos):
            texto = f"""
**{i}** — {v.tipo} | {v.marca} | {v.modelo}  
💰 {v.preco:.2f}€ | 🚀 {v.vel} km/h | ⛽ {v.combustivel}  
🎨 {v.cor}
"""
            if isinstance(v, Carro) and getattr(v, "eletrico", False):
                texto += f"\n⚡ Elétrico | {v.consumo_kwh} kWh/100km"

            if isinstance(v, Mota):
                texto += f"\n🏍 {v.cilindrada} cc"

            st.markdown(texto)
            st.divider()

    # -------------------------
    # DISCOUNT
    # -------------------------
    st.subheader("💸 Aplicar desconto")

    if frota.veiculos:
        idx_desc = st.number_input(
            "Índice do veículo",
            min_value=0,
            max_value=len(frota.veiculos) - 1,
            step=1,
            key="idx_desc"
        )

        if st.button("Aplicar desconto 10%", key="btn_desc"):
            carro = frota.veiculos[int(idx_desc)]
            frota.desconto(carro, 0.1)
            frota.criarFicheiro()
            st.success("Desconto aplicado!")

    # -------------------------
    # REMOVE VEHICLE
    # -------------------------
    st.subheader("❌ Remover veículo")

    if frota.veiculos:
        idx_remover = st.number_input(
            "Índice do veículo a remover",
            min_value=0,
            max_value=len(frota.veiculos) - 1,
            step=1,
            key="idx_remove"
        )

        if st.button("Remover veículo", key="btn_remove"):
            v = frota.veiculos[int(idx_remover)]
            frota.remover_veiculo(v)
            frota.criarFicheiro()
            st.success("Veículo removido!")
