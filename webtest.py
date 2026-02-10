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

def adicionar_veiculo_callback():
    error_msg = None
    if not st.session_state.marca.strip() or not st.session_state.modelo.strip() or st.session_state.preco <= 0 or st.session_state.vel <= 0:
        error_msg = "❌ Preencha todos os campos obrigatórios: marca, modelo, preço, velocidade."
    if st.session_state.tipo == "Carro" and st.session_state.eletrico and (st.session_state.consumo is None or st.session_state.consumo <= 0):
        error_msg = "❌ Para carros elétricos, informe o consumo em kWh/100km."
    if st.session_state.tipo == "Mota" and (st.session_state.cilindrada is None or st.session_state.cilindrada <= 0):
        error_msg = "❌ Para motos, informe a cilindrada."

    if error_msg:
        st.error(error_msg)
        return

    # --- CREATE VEHICLE ---
    if st.session_state.tipo == "Carro":
        v = Carro(
            st.session_state.marca,
            st.session_state.modelo,
            st.session_state.preco,
            st.session_state.vel,
            st.session_state.combustivel,
            st.session_state.cor,
            st.session_state.eletrico,
            st.session_state.consumo
        )
    elif st.session_state.tipo == "Mota":
        v = Mota(
            st.session_state.marca,
            st.session_state.modelo,
            st.session_state.preco,
            st.session_state.vel,
            st.session_state.combustivel,
            st.session_state.cor,
            st.session_state.cilindrada
        )
    else:
        v = Veiculo(
            st.session_state.tipo,
            st.session_state.marca,
            st.session_state.modelo,
            st.session_state.preco,
            st.session_state.vel,
            st.session_state.combustivel,
            st.session_state.cor
        )

    frota.adicionar_veiculo(v)
    st.success("✅ Veículo adicionado com sucesso!")

    # --- RESET FIELDS SAFELY ---
    st.session_state.update({
        "tipo": "Veículo",
        "marca": "",
        "modelo": "",
        "preco": 0.0,
        "vel": 0,
        "combustivel": "Gasolina",
        "cor": "#000000",
        "eletrico": False,
        "consumo": 0.0,
        "cilindrada": 0
    })


# --- Inputs bound to session_state ---
tipo = st.selectbox("Tipo", ["Veículo", "Carro", "Mota"], key="tipo")
marca = st.text_input("Marca", key="marca")
modelo = st.text_input("Modelo", key="modelo")
preco = st.number_input("Preço", min_value=0.0, key="preco")
vel = st.number_input("Velocidade", min_value=0, key="vel")
combustivel = st.selectbox("Combustível", ["Gasolina", "Gasóleo"], key="combustivel")
cor = st.color_picker("Cor", key="cor")

eletrico = st.checkbox("Elétrico", key="eletrico") if tipo == "Carro" else False
consumo = st.number_input("Consumo kWh/100km", min_value=0.0, key="consumo") if tipo == "Carro" and eletrico else None
cilindrada = st.number_input("Cilindrada", min_value=0, key="cilindrada") if tipo == "Mota" else None

if st.button("Adicionar"):
    adicionar_veiculo_callback()

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
