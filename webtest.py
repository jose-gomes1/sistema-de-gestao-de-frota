import streamlit as st
from frota import Frota
from veiculo import Veiculo
from carro import Carro
from mota import Mota

# ---------------------------------------------
# Página
# ---------------------------------------------
st.set_page_config("Gestão de Frota")
st.title("🚗 Gestão de Frota")

frota = Frota()

# ---------------------------------------------
# Estado para editar
# ---------------------------------------------
if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# ---------------------------------------------
# Tabs
# ---------------------------------------------
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

                st.success("Adicionado ✔️")
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

                with col1:
                    if st.button("✏️ Editar", key=f"edit_{v['id']}"):
                        st.session_state.edit_id = v["id"]

                with col2:
                    if st.button("❌ Remover", key=f"del_{v['id']}"):
                        frota.remover(v["id"])
                        st.success("🗑 Veículo removido!")
                        st.experimental_rerun()

                # EDIT FORM
                if st.session_state.edit_id == v["id"]:
                    st.markdown("### ✏️ Editar veículo")

                    emarca = st.text_input("Marca", v["marca"], key=f"m_{v['id']}")
                    emodelo = st.text_input("Modelo", v["modelo"], key=f"mo_{v['id']}")
                    epreco = st.number_input("Preço (€)", value=v["preco"], key=f"p_{v['id']}")
                    evel = st.number_input("Velocidade (km/h)", value=v["vel"], key=f"v_{v['id']}")
                    ecor = st.color_picker("Cor", v["cor"], key=f"cor_{v['id']}")

                    if st.button("💾 Guardar", key=f"save_{v['id']}"):
                        if not emarca.strip() or not emodelo.strip() or epreco <= 0 or evel <= 0:
                            st.error("❌ Preencha todos os campos obrigatórios.")
                        else:
                            frota.atualizar(v["id"], emarca, emodelo, epreco, evel, v["combustivel"], ecor)
                            st.success("✅ Alterações guardadas!")
                            st.session_state.edit_id = None
                            st.experimental_rerun()
