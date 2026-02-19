import streamlit as st
from frota import Frota
from veiculo import Veiculo
from carro import Carro
from mota import Mota
from storage import get_conn

# --------------------------------------------------
# PAGE
# --------------------------------------------------
st.set_page_config("Gestão de Frota")
st.title("🚗 Gestão de Frota")

# --------------------------------------------------
# INIT
# --------------------------------------------------
frota = Frota()

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab_add, tab_frota = st.tabs(["➕ Adicionar", "📋 Frota"])

# ==================================================
# ADD
# ==================================================
with tab_add:
    st.subheader("➕ Adicionar veículo")

    tipo = st.selectbox("Tipo", ["Veículo", "Carro", "Mota"])
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    preco = st.number_input("Preço (€)", min_value=0.0)
    vel = st.number_input("Velocidade (km/h)", min_value=0)

    combustivel = st.selectbox("Combustível", ["Gasolina", "Gasóleo"])
    cor = st.color_picker("Cor")

    eletrico = False
    consumo = None
    cilindrada = None

    if tipo == "Carro":
        eletrico = st.checkbox("Elétrico")
        if eletrico:
            combustivel = "Elétrico"
            consumo = st.number_input("Consumo (kWh/100km)", min_value=0.0)

    if tipo == "Mota":
        cilindrada = st.number_input("Cilindrada (cc)", min_value=0)

    if st.button("Adicionar"):
        if not marca.strip() or not modelo.strip() or preco <= 0 or vel <= 0:
            st.error("❌ Preencha todos os campos obrigatórios.")
        elif tipo == "Carro" and eletrico and consumo <= 0:
            st.error("❌ Consumo inválido.")
        elif tipo == "Mota" and cilindrada <= 0:
            st.error("❌ Cilindrada inválida.")
        else:
            if tipo == "Carro":
                v = Carro(marca, modelo, preco, vel, combustivel, cor, eletrico, consumo)
            elif tipo == "Mota":
                v = Mota(marca, modelo, preco, vel, combustivel, cor, cilindrada)
            else:
                v = Veiculo(tipo, marca, modelo, preco, vel, combustivel, cor)

            frota.adicionar_veiculo(v)

            # ALERT
            st.components.v1.html(
                "<script>alert('✅ Veículo adicionado com sucesso!');</script>",
                height=0
            )

            # CLEAR + RERUN
            st.rerun()

# ==================================================
# FROTA
# ==================================================
with tab_frota:
    st.subheader("📋 Frota")

    rows = frota.listar()

    if not rows:
        st.info("Nenhum veículo registado.")
    else:
        for v in rows:
            with st.expander(f"#{v['id']} — {v['marca']} {v['modelo']}"):
                preco_final = v["preco"] * (1.10 if v["com_iva"] else 1)

                st.write(f"**Preço:** €{preco_final:.2f}")
                st.write(f"**Velocidade:** {v['vel']} km/h")
                st.write(f"**Combustível:** {v['combustivel']}")
                st.write(f"**Cor:** {v['cor']}")

                if v["tipo"] == "Carro" and v["eletrico"]:
                    st.write(f"**Consumo:** {v['consumo']} kWh/100km")

                if v["tipo"] == "Mota":
                    st.write(f"**Cilindrada:** {v['cilindrada']} cc")

                c1, c2, c3 = st.columns(3)

                # EDIT
                with c1:
                    if st.button("✏️ Editar", key=f"e{v['id']}"):
                        st.session_state.edit_id = v["id"]

                # IVA TOGGLE
                with c2:
                    if st.button("💸 IVA 10%", key=f"iva{v['id']}"):
                        frota.toggle_desconto(v["id"])
                        st.rerun()

                # DELETE
                with c3:
                    if st.button("❌ Remover", key=f"d{v['id']}"):
                        frota.remover(v["id"])
                        st.rerun()

                # ---------------- EDIT ----------------
                if st.session_state.edit_id == v["id"]:
                    st.markdown("### ✏️ Editar veículo")

                    emarca = st.text_input("Marca", v["marca"], key=f"m{v['id']}")
                    emodelo = st.text_input("Modelo", v["modelo"], key=f"mo{v['id']}")
                    epreco = st.number_input("Preço (€)", value=v["preco"], key=f"p{v['id']}")
                    evel = st.number_input("Velocidade", value=v["vel"], key=f"v{v['id']}")
                    ecor = st.color_picker("Cor", v["cor"], key=f"cor{v['id']}")

                    if st.button("💾 Guardar", key=f"s{v['id']}"):
                        frota.atualizar(
                            v["id"], emarca, emodelo, epreco, evel, v["combustivel"], ecor
                        )
                        st.session_state.edit_id = None
                        st.success("✅ Veículo atualizado!")
                        st.rerun()
