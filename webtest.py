import streamlit as st
from frota import Frota
from veiculo import Veiculo
from carro import Carro
from mota import Mota

# -----------------------------
# Página
# -----------------------------
st.set_page_config("Gestão de Frota")
st.title("🚗 Gestão de Frota")

# Inicializar frota
frota = Frota()

# Estado para edição
if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# -----------------------------
# Tabs
# -----------------------------
tab_add, tab_frota = st.tabs(["➕ Adicionar", "📋 Frota"])

# ================= ADD =================
with tab_add:
    st.subheader("➕ Adicionar veículo")

    with st.form("add_form", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["Veículo", "Carro", "Mota"], key="tipo_add")
        marca = st.text_input("Marca", key="marca_add")
        modelo = st.text_input("Modelo", key="modelo_add")
        preco = st.number_input("Preço (€)", min_value=0.0, key="preco_add")
        vel = st.number_input("Velocidade (km/h)", min_value=0, key="vel_add")
        combustivel = st.selectbox("Combustível", ["Gasolina", "Gasóleo"], key="comb_add")
        cor = st.color_picker("Cor", key="cor_add")

        eletrico = False
        consumo = None
        cilindrada = None

        if tipo == "Carro":
            eletrico = st.checkbox("Elétrico", key="eletrico_add")
            if eletrico:
                combustivel = "Elétrico"
                consumo = st.number_input("Consumo (kWh/100km)", min_value=0.0, key="consumo_add")

        if tipo == "Mota":
            cilindrada = st.number_input("Cilindrada (cc)", min_value=0, key="cilindrada_add")

        submitted = st.form_submit_button("Adicionar")

        if submitted:
            # Validações
            if not marca.strip() or not modelo.strip() or preco <= 0 or vel <= 0:
                st.error("❌ Preencha todos os campos obrigatórios.")
            elif tipo == "Carro" and eletrico and (consumo is None or consumo <= 0):
                st.error("❌ Para carros elétricos, informe consumo.")
            elif tipo == "Mota" and (cilindrada is None or cilindrada <= 0):
                st.error("❌ Para motos, informe cilindrada.")
            else:
                # Criar veículo
                if tipo == "Carro":
                    v = Carro(marca, modelo, preco, vel, combustivel, cor, eletrico, consumo)
                elif tipo == "Mota":
                    v = Mota(marca, modelo, preco, vel, combustivel, cor, cilindrada)
                else:
                    v = Veiculo(tipo, marca, modelo, preco, vel, combustivel, cor)

                frota.adicionar_veiculo(v)

                # ALERTA JS
                st.components.v1.html(
                    "<script>alert('✅ Veículo adicionado com sucesso!');</script>",
                    height=0
                )

                st.experimental_rerun()

# ================= FROTA =================
with tab_frota:
    st.subheader("📋 Frota")

    rows = frota.listar()

    if not rows:
        st.info("Nenhum veículo registado.")
    else:
        for v in rows:
            with st.expander(f"#{v['id']} — {v['marca']} {v['modelo']}"):
                st.markdown(f"**Tipo:** {v['tipo']}")
                st.markdown(f"**Preço:** €{v['preco']:.2f}")
                st.markdown(f"**Velocidade:** {v['vel']} km/h")
                st.markdown(f"**Combustível:** {v['combustivel']}")
                st.markdown(f"**Cor:** {v['cor']}")

                if v["tipo"] == "Carro" and v["eletrico"]:
                    st.markdown(f"**Consumo:** {v['consumo']} kWh/100km")
                if v["tipo"] == "Mota":
                    st.markdown(f"**Cilindrada:** {v['cilindrada']} cc")

                col1, col2 = st.columns(2)

                # EDIT
                with col1:
                    if st.button("✏️ Editar", key=f"edit_{v['id']}"):
                        st.session_state.edit_id = v["id"]

                # DELETE
                with col2:
                    if st.button("❌ Remover", key=f"del_{v['id']}"):
                        frota.remover(v["id"])
                        st.success("🗑 Veículo removido!")
                        st.experimental_rerun()

                # ---------------- EDIT ----------------
                if st.session_state.edit_id == v["id"]:
                    st.markdown("### ✏️ Editar veículo")

                    emarca = st.text_input("Marca", v["marca"], key=f"m_{v['id']}")
                    emodelo = st.text_input("Modelo", v["modelo"], key=f"mo_{v['id']}")
                    epreco = st.number_input("Preço (€)", value=v["preco"], key=f"p_{v['id']}")
                    evel = st.number_input("Velocidade (km/h)", value=v["vel"], key=f"v_{v['id']}")
                    ecor = st.color_picker("Cor", v["cor"], key=f"cor_{v['id']}")

                    # Combustível editável
                    combustiveis = ["Gasolina", "Gasóleo"]
                    if v["tipo"] == "Carro" and v["eletrico"]:
                        combustiveis.append("Elétrico")

                    ecomb = st.selectbox(
                        "Combustível",
                        options=combustiveis,
                        index=combustiveis.index(v["combustivel"]),
                        key=f"c_{v['id']}"
                    )

                    # Carro elétrico: consumo
                    econsumo = v.get("consumo")
                    if v["tipo"] == "Carro" and ecomb == "Elétrico":
                        econsumo = st.number_input(
                            "Consumo (kWh/100km)",
                            value=v["consumo"] or 0.0,
                            key=f"cons_{v['id']}"
                        )

                    # Mota: cilindrada
                    ecil = v.get("cilindrada")
                    if v["tipo"] == "Mota":
                        ecil = st.number_input(
                            "Cilindrada (cc)",
                            value=v["cilindrada"] or 0,
                            key=f"cil_{v['id']}"
                        )

                    if st.button("💾 Guardar", key=f"save_{v['id']}"):
                        if not emarca.strip() or not emodelo.strip() or epreco <= 0 or evel <= 0:
                            st.error("❌ Preencha todos os campos obrigatórios.")
                        elif v["tipo"] == "Carro" and ecomb == "Elétrico" and (econsumo is None or econsumo <= 0):
                            st.error("❌ Informe o consumo para carro elétrico.")
                        elif v["tipo"] == "Mota" and (ecil is None or ecil <= 0):
                            st.error("❌ Informe a cilindrada para a mota.")
                        else:
                            # Atualiza veículo
                            frota.atualizar(
                                v["id"],
                                emarca,
                                emodelo,
                                epreco,
                                evel,
                                ecomb,
                                ecor,
                                consumo=econsumo,
                                cilindrada=ecil
                            )
                            st.success("✅ Veículo atualizado!")
                            st.session_state.edit_id = None
                            st.experimental_rerun()
