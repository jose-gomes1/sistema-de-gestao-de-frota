import streamlit as st
from frota import Frota
from veiculo import Veiculo
from carro import Carro
from mota import Mota
from storage import get_conn
st.set_page_config("Gestão de Frota")
st.title("🚗 Gestão de Frota")

# ---------------- FROTA ----------------
@st.cache_resource
def get_frota():
    return Frota()

frota = get_frota()

tab_add, tab_frota = st.tabs(["➕ Adicionar", "📋 Frota"])

# ================= ADD =================

# --- Initialize session state keys if they don't exist ---
for key, default in {
    "tipo_add": "Veículo",
    "marca_add": "",
    "modelo_add": "",
    "preco_add": 0.0,
    "vel_add": 0,
    "comb_add": "Gasolina",
    "cor_add": "#000000",
    "eletrico_add": False,
    "consumo_add": 0.0,
    "cilindrada_add": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

with tab_add:
    tipo = st.selectbox("Tipo", ["Veículo", "Carro", "Mota"], key="tipo_add")
    marca = st.text_input("Marca", key="marca_add")
    modelo = st.text_input("Modelo", key="modelo_add")
    preco = st.number_input("Preço", min_value=0.0, key="preco_add")
    vel = st.number_input("Velocidade", min_value=0, key="vel_add")
    combustivel = st.selectbox("Combustível", ["Gasolina", "Gasóleo"], key="comb_add")
    cor = st.color_picker("Cor", key="cor_add")
    eletrico = st.checkbox("Elétrico", key="eletrico_add")

    consumo = None
    cilindrada = None
    if tipo == "Carro" and eletrico:
        consumo = st.number_input("Consumo kWh/100km", min_value=0.0, key="consumo_add")
        combustivel = "Elétrico"  # override automatically
    if tipo == "Mota":
        cilindrada = st.number_input("Cilindrada", min_value=0, key="cilindrada_add")

    if st.button("Adicionar"):
        # -------- VALIDATION --------
        error_msg = None
        if not st.session_state.marca_add.strip() or not st.session_state.modelo_add.strip() or st.session_state.preco_add <= 0 or st.session_state.vel_add <= 0:
            error_msg = "❌ Preencha todos os campos obrigatórios: marca, modelo, preço, velocidade."
        if tipo == "Carro" and eletrico and (st.session_state.consumo_add <= 0):
            error_msg = "❌ Para carros elétricos, informe o consumo em kWh/100km."
        if tipo == "Mota" and (st.session_state.cilindrada_add <= 0):
            error_msg = "❌ Para motos, informe a cilindrada."

        if error_msg:
            st.error(error_msg)
        else:
            # -------- CREATE VEHICLE --------
            if tipo == "Carro":
                v = Carro(
                    st.session_state.marca_add,
                    st.session_state.modelo_add,
                    st.session_state.preco_add,
                    st.session_state.vel_add,
                    combustivel,
                    st.session_state.cor_add,
                    eletrico,
                    st.session_state.consumo_add if eletrico else None
                )
            elif tipo == "Mota":
                v = Mota(
                    st.session_state.marca_add,
                    st.session_state.modelo_add,
                    st.session_state.preco_add,
                    st.session_state.vel_add,
                    st.session_state.comb_add,
                    st.session_state.cor_add,
                    st.session_state.cilindrada_add
                )
            else:
                v = Veiculo(
                    tipo,
                    st.session_state.marca_add,
                    st.session_state.modelo_add,
                    st.session_state.preco_add,
                    st.session_state.vel_add,
                    st.session_state.comb_add,
                    st.session_state.cor_add
                )

            frota.adicionar_veiculo(v)

            # --- Show blocking alert ---
            st.components.v1.html("""
            <script>
                alert("✅ Veículo adicionado com sucesso!");
            </script>
            """, height=0)

            # -------- CLEAR INPUTS --------
            for key in ["marca_add","modelo_add","preco_add","vel_add","comb_add","cor_add","eletrico_add","consumo_add","cilindrada_add","tipo_add"]:
                if key in st.session_state:
                    del st.session_state[key]

            st.rerun()

# ================= FROTA LIST =================
with tab_frota:
    marca_filtro = st.text_input("Filtrar por marca")
    rows = frota.filtrar_por_marca(marca_filtro) if marca_filtro else frota.listar()

    for v in rows:
        with st.expander(f"#{v['id']} — {v['marca']} {v['modelo']}"):
            # --- Vehicle Info ---
            st.markdown(f"**Preço:** €{v['preco']:.2f} {'(com IVA)' if v['com_iva'] else ''}")
            st.markdown(f"**Velocidade:** {v['vel']} km/h")
            st.markdown(f"**Combustível:** {v['combustivel']}")
            st.markdown(f"**Cor:** {v['cor']}")

            # --- Dynamic fields ---
            if v['tipo'] == "Carro" and v['eletrico']:
                st.markdown(f"**Consumo:** {v['consumo']} kWh/100km")
            if v['tipo'] == "Mota" and v['cilindrada']:
                st.markdown(f"**Cilindrada:** {v['cilindrada']} cc")

            # --- Buttons ---
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                if st.button("✏️ Editar", key=f"edit_{v['id']}"):
                    st.session_state.edit_id = v["id"]
            with col2:
                if st.button("💸 IVA 10%", key=f"desc_{v['id']}"):
                    frota.toggle_desconto(v["id"])
                    st.success("💰 IVA aplicado/removido!")
                    st.rerun()
            with col3:
                if st.button("❌ Remover", key=f"del_{v['id']}"):
                    frota.remover(v["id"])
                    st.success("🗑 Veículo removido!")
                    st.rerun()

            # --- Edit Form ---
            if st.session_state.get("edit_id") == v["id"]:
                st.markdown("### ✏️ Editar veículo")
                emarca = st.text_input("Marca", v["marca"], key=f"m_{v['id']}")
                emodelo = st.text_input("Modelo", v["modelo"], key=f"mo_{v['id']}")
                epreco = st.number_input("Preço", value=v["preco"], key=f"p_{v['id']}")
                evel = st.number_input("Velocidade", value=v["vel"], key=f"v_{v['id']}")

                # --- Combustível selectbox ---
                combustivel_options = ["Gasolina", "Gasóleo"]
                if v["tipo"] == "Carro" and v["eletrico"]:
                    combustivel_options.append("Elétrico")
                ecomb = st.selectbox("Combustível", options=combustivel_options,
                                     index=combustivel_options.index(v["combustivel"]), key=f"c_{v['id']}")

                ecor = st.color_picker("Cor", v["cor"], key=f"cor_{v['id']}")

                # Campos específicos (dynamic)
                consumo_edit = None
                cilindrada_edit = None
                if v["tipo"] == "Carro" and ecomb == "Elétrico":
                    consumo_edit = st.number_input(
                        "Consumo kWh/100km", value=v["consumo"] or 0.0, key=f"cons_{v['id']}"
                    )
                if v["tipo"] == "Mota":
                    cilindrada_edit = st.number_input(
                        "Cilindrada (cc)", value=v["cilindrada"] or 0, key=f"cil_{v['id']}"
                    )

                if st.button("💾 Guardar", key=f"save_{v['id']}"):
                    # -------- VALIDATION --------
                    error_msg = None
                    if not emarca.strip() or not emodelo.strip() or epreco <= 0 or evel <= 0:
                        error_msg = "❌ Preencha todos os campos obrigatórios: marca, modelo, preço, velocidade."
                    if v["tipo"] == "Carro" and ecomb == "Elétrico" and (consumo_edit is None or consumo_edit <= 0):
                        error_msg = "❌ Para carros elétricos, informe o consumo em kWh/100km."
                    if v["tipo"] == "Mota" and (cilindrada_edit is None or cilindrada_edit <= 0):
                        error_msg = "❌ Para motos, informe a cilindrada."

                    if error_msg:
                        st.error(error_msg)
                    else:
                        # -------- UPDATE VEHICLE --------
                        frota.atualizar(v["id"], emarca, emodelo, epreco, evel, ecomb, ecor)

                        conn = get_conn()
                        if v["tipo"] == "Carro" and ecomb == "Elétrico":
                            conn.execute("UPDATE veiculos SET consumo=? WHERE id=?", (consumo_edit, v["id"]))
                        else:
                            # If combustivel changed from Elétrico, remove consumo
                            conn.execute("UPDATE veiculos SET consumo=NULL WHERE id=?", (v["id"],))
                        if v["tipo"] == "Mota":
                            conn.execute("UPDATE veiculos SET cilindrada=? WHERE id=?", (cilindrada_edit, v["id"]))
                        conn.commit()

                        del st.session_state.edit_id
                        st.success("✅ Veículo atualizado com sucesso!")
                        st.rerun()
