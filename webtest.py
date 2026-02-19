import streamlit as st
import json
import streamlit.components.v1 as components

# ---------------- CONFIG ----------------
st.set_page_config("Gestão de Frota")
st.title("🚗 Gestão de Frota (Client-side Persistente)")

FROTA_KEY = "frota_data"

# ---------------- SESSION STATE ----------------
if "frota" not in st.session_state:
    st.session_state.frota = []

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

# ---------------- LOAD FROM localStorage ----------------
components.html(
    f"""
    <script>
    const key = "{FROTA_KEY}";
    let data = localStorage.getItem(key);
    if (!data) {{
        localStorage.setItem(key, JSON.stringify([]));
        data = "[]";
    }}
    const event = new CustomEvent("STREAMLIT_DATA", {{
        detail: JSON.parse(data)
    }});
    window.dispatchEvent(event);
    </script>
    """,
    height=0,
)

components.html(
    """
    <script>
    window.addEventListener("STREAMLIT_DATA", (e) => {
        const out = document.getElementById("out");
        out.value = JSON.stringify(e.detail);
        out.dispatchEvent(new Event("change"));
    });
    </script>
    <textarea id="out" style="display:none;"></textarea>
    """,
    height=0,
)

if "out" in st.session_state:
    st.session_state.frota = json.loads(st.session_state.out)

# ---------------- SAVE TO localStorage ----------------
def save_frota():
    components.html(
        f"""
        <script>
        localStorage.setItem("{FROTA_KEY}", JSON.stringify({json.dumps(st.session_state.frota)}));
        </script>
        """,
        height=0,
    )

# ---------------- TABS ----------------
tab_add, tab_frota = st.tabs(["➕ Adicionar", "📋 Frota"])

# ================= ADD =================
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
        elif tipo == "Carro" and eletrico and (not consumo or consumo <= 0):
            st.error("❌ Informe o consumo do carro elétrico.")
        elif tipo == "Mota" and (not cilindrada or cilindrada <= 0):
            st.error("❌ Informe a cilindrada da mota.")
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
                "cilindrada": cilindrada
            })
            save_frota()
            st.success("✅ Veículo guardado no browser")
            st.rerun()

# ================= FROTA =================
with tab_frota:
    st.subheader("📋 Frota")

    if not st.session_state.frota:
        st.info("Nenhum veículo registado.")
    else:
        for v in st.session_state.frota:
            with st.expander(f"#{v['id']} — {v['marca']} {v['modelo']}"):
                st.write(f"**Tipo:** {v['tipo']}")
                st.write(f"**Preço:** €{v['preco']:.2f}")
                st.write(f"**Velocidade:** {v['vel']} km/h")
                st.write(f"**Combustível:** {v['combustivel']}")
                st.write(f"**Cor:** {v['cor']}")

                if v["tipo"] == "Carro" and v.get("eletrico"):
                    st.write(f"**Consumo:** {v['consumo']} kWh/100km")

                if v["tipo"] == "Mota":
                    st.write(f"**Cilindrada:** {v['cilindrada']} cc")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✏️ Editar", key=f"edit_{v['id']}"):
                        st.session_state.edit_id = v["id"]

                with col2:
                    if st.button("❌ Remover", key=f"del_{v['id']}"):
                        st.session_state.frota = [
                            x for x in st.session_state.frota if x["id"] != v["id"]
                        ]
                        save_frota()
                        st.rerun()

                # ---------- EDIT ----------
                if st.session_state.edit_id == v["id"]:
                    st.markdown("### ✏️ Editar veículo")

                    emarca = st.text_input("Marca", v["marca"], key=f"m_{v['id']}")
                    emodelo = st.text_input("Modelo", v["modelo"], key=f"mo_{v['id']}")
                    epreco = st.number_input("Preço (€)", value=v["preco"], key=f"p_{v['id']}")
                    evel = st.number_input("Velocidade", value=v["vel"], key=f"v_{v['id']}")

                    combustiveis = ["Gasolina", "Gasóleo"]
                    if v["tipo"] == "Carro" and v["eletrico"]:
                        combustiveis.append("Elétrico")

                    ecomb = st.selectbox(
                        "Combustível",
                        combustiveis,
                        index=combustiveis.index(v["combustivel"]),
                        key=f"c_{v['id']}"
                    )

                    ecor = st.color_picker("Cor", v["cor"], key=f"cor_{v['id']}")

                    econsumo = v.get("consumo")
                    ecil = v.get("cilindrada")

                    if v["tipo"] == "Carro" and ecomb == "Elétrico":
                        econsumo = st.number_input(
                            "Consumo (kWh/100km)",
                            value=v["consumo"],
                            key=f"cons_{v['id']}"
                        )

                    if v["tipo"] == "Mota":
                        ecil = st.number_input(
                            "Cilindrada (cc)",
                            value=v["cilindrada"],
                            key=f"cil_{v['id']}"
                        )

                    if st.button("💾 Guardar", key=f"save_{v['id']}"):
                        if not emarca.strip() or not emodelo.strip() or epreco <= 0 or evel <= 0:
                            st.error("❌ Campos inválidos.")
                        else:
                            for x in st.session_state.frota:
                                if x["id"] == v["id"]:
                                    x.update({
                                        "marca": emarca,
                                        "modelo": emodelo,
                                        "preco": epreco,
                                        "vel": evel,
                                        "combustivel": ecomb,
                                        "cor": ecor,
                                        "consumo": econsumo,
                                        "cilindrada": ecil
                                    })
                            st.session_state.edit_id = None
                            save_frota()
                            st.success("✅ Atualizado no browser")
                            st.rerun()
