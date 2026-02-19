import streamlit as st
import json
import streamlit.components.v1 as components

# --------------------------------------------------
# PAGE
# --------------------------------------------------
st.set_page_config("Gestão de Frota")
st.title("🚗 Gestão de Frota")

FROTA_KEY = "frota_data"

# --------------------------------------------------
# BOOTSTRAP localStorage → session_state
# --------------------------------------------------
components.html(
    f"""
    <script>
    const key = "{FROTA_KEY}";
    const data = localStorage.getItem(key) || "[]";

    window.streamlitSessionState = window.streamlitSessionState || {{}};
    window.streamlitSessionState.frota = JSON.parse(data);
    </script>
    """,
    height=0,
)

if "frota" not in st.session_state:
    st.session_state.frota = []

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# --------------------------------------------------
# SAVE helper
# --------------------------------------------------
def save():
    components.html(
        f"""
        <script>
        localStorage.setItem(
            "{FROTA_KEY}",
            JSON.stringify({json.dumps(st.session_state.frota)})
        );
        </script>
        """,
        height=0,
    )

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
        if not marca or not modelo or preco <= 0 or vel <= 0:
            st.error("❌ Preencha todos os campos obrigatórios.")
        elif tipo == "Carro" and eletrico and consumo <= 0:
            st.error("❌ Consumo inválido.")
        elif tipo == "Mota" and cilindrada <= 0:
            st.error("❌ Cilindrada inválida.")
        else:
            st.session_state.frota.append({
                "id": max([v["id"] for v in st.session_state.frota], default=0) + 1,
                "tipo": tipo,
                "marca": marca,
                "modelo": modelo,
                "preco": preco,
                "vel": vel,
                "combustivel": combustivel,
                "cor": cor,
                "eletrico": eletrico,
                "consumo": consumo,
                "cilindrada": cilindrada,
                "com_iva": False
            })
            save()

            # ✅ ALERT
            components.html(
                "<script>alert('✅ Veículo adicionado com sucesso!');</script>",
                height=0
            )

            # ✅ LIMPAR CAMPOS
            st.rerun()

# ==================================================
# FROTA
# ==================================================
with tab_frota:
    st.subheader("📋 Frota")

    if not st.session_state.frota:
        st.info("Nenhum veículo registado.")
    else:
        for v in st.session_state.frota:
            with st.expander(f"#{v['id']} — {v['marca']} {v['modelo']}"):
                preco = v["preco"] * (1.10 if v["com_iva"] else 1)
                st.write(f"**Preço:** €{preco:.2f}")
                st.write(f"**Velocidade:** {v['vel']} km/h")
                st.write(f"**Combustível:** {v['combustivel']}")
                st.write(f"**Cor:** {v['cor']}")

                if v["tipo"] == "Carro" and v["eletrico"]:
                    st.write(f"**Consumo:** {v['consumo']} kWh/100km")

                if v["tipo"] == "Mota":
                    st.write(f"**Cilindrada:** {v['cilindrada']} cc")

                c1, c2, c3 = st.columns(3)

                with c1:
                    if st.button("✏️ Editar", key=f"e{v['id']}"):
                        st.session_state.edit_id = v["id"]

                with c2:
                    if st.button("💸 IVA 10%", key=f"iva{v['id']}"):
                        v["com_iva"] = not v["com_iva"]
                        save()
                        st.rerun()

                with c3:
                    if st.button("❌ Remover", key=f"d{v['id']}"):
                        st.session_state.frota = [
                            x for x in st.session_state.frota if x["id"] != v["id"]
                        ]
                        save()
                        st.rerun()

                # ---------------- EDIT ----------------
                if st.session_state.edit_id == v["id"]:
                    st.markdown("### ✏️ Editar veículo")

                    emarca = st.text_input("Marca", v["marca"], key=f"m{v['id']}")
                    emodelo = st.text_input("Modelo", v["modelo"], key=f"mo{v['id']}")
                    epreco = st.number_input("Preço", value=v["preco"], key=f"p{v['id']}")
                    evel = st.number_input("Velocidade", value=v["vel"], key=f"v{v['id']}")

                    if st.button("💾 Guardar", key=f"s{v['id']}"):
                        v.update({
                            "marca": emarca,
                            "modelo": emodelo,
                            "preco": epreco,
                            "vel": evel
                        })
                        st.session_state.edit_id = None
                        save()
                        st.success("✅ Atualizado!")
                        st.rerun()
