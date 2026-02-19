import streamlit as st
import json
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ----------------
st.set_page_config("Gestão de Frota", layout="centered")
st.title("🚗 Gestão de Frota (Client-side, Persistente)")

# ---------------- LOCAL STORAGE BRIDGE ----------------
def load_local_storage(key, default):
    component = components.html(
        f"""
        <script>
        const key = "{key}";
        const defaultValue = {json.dumps(default)};

        function send(value) {{
            const out = document.getElementById("out");
            out.value = JSON.stringify(value);
            out.dispatchEvent(new Event("change"));
        }}

        let data = localStorage.getItem(key);
        if (!data) {{
            localStorage.setItem(key, JSON.stringify(defaultValue));
            data = JSON.stringify(defaultValue);
        }}

        send(JSON.parse(data));
        </script>

        <textarea id="out" style="display:none;"></textarea>
        """,
        height=0,
    )

    if component:
        return json.loads(component)
    return default


def save_local_storage(key, value):
    components.html(
        f"""
        <script>
        localStorage.setItem("{key}", JSON.stringify({json.dumps(value)}));
        </script>
        """,
        height=0,
    )


# ---------------- LOAD DATA ----------------
FROTA_KEY = "frota_data"
frota = load_local_storage(FROTA_KEY, [])

# ---------------- ADD VEHICLE ----------------
st.subheader("➕ Adicionar veículo")

with st.form("add_vehicle", clear_on_submit=True):
    tipo = st.selectbox("Tipo", ["Carro", "Mota"])
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    preco = st.number_input("Preço (€)", min_value=0.0)
    vel = st.number_input("Velocidade (km/h)", min_value=0)

    eletrico = False
    consumo = None
    cilindrada = None

    if tipo == "Carro":
        eletrico = st.checkbox("Elétrico")
        if eletrico:
            consumo = st.number_input("Consumo (kWh/100km)", min_value=0.0)

    if tipo == "Mota":
        cilindrada = st.number_input("Cilindrada (cc)", min_value=0)

    submitted = st.form_submit_button("Adicionar")

    if submitted:
        if not marca.strip() or not modelo.strip() or preco <= 0 or vel <= 0:
            st.error("❌ Preencha todos os campos obrigatórios.")
        elif tipo == "Carro" and eletrico and (not consumo or consumo <= 0):
            st.error("❌ Informe o consumo do carro elétrico.")
        elif tipo == "Mota" and (not cilindrada or cilindrada <= 0):
            st.error("❌ Informe a cilindrada da mota.")
        else:
            new_vehicle = {
                "id": max([v["id"] for v in frota], default=0) + 1,
                "tipo": tipo,
                "marca": marca,
                "modelo": modelo,
                "preco": preco,
                "vel": vel,
                "eletrico": eletrico,
                "consumo": consumo,
                "cilindrada": cilindrada
            }
            frota.append(new_vehicle)
            save_local_storage(FROTA_KEY, frota)
            st.success("✅ Guardado permanentemente no browser!")
            st.rerun()

# ---------------- LIST VEHICLES ----------------
st.divider()
st.subheader("📋 Frota")

if not frota:
    st.info("Nenhum veículo registado.")
else:
    for v in frota:
        with st.expander(f"#{v['id']} — {v['marca']} {v['modelo']}"):
            st.write(f"**Tipo:** {v['tipo']}")
            st.write(f"**Preço:** €{v['preco']:.2f}")
            st.write(f"**Velocidade:** {v['vel']} km/h")

            if v["tipo"] == "Carro" and v.get("eletrico"):
                st.write(f"**Elétrico:** Sim")
                st.write(f"**Consumo:** {v['consumo']} kWh/100km")

            if v["tipo"] == "Mota":
                st.write(f"**Cilindrada:** {v['cilindrada']} cc")

            col1, col2 = st.columns(2)

            # -------- DELETE --------
            with col1:
                if st.button("❌ Remover", key=f"del_{v['id']}"):
                    frota = [x for x in frota if x["id"] != v["id"]]
                    save_local_storage(FROTA_KEY, frota)
                    st.success("🗑 Removido do browser")
                    st.rerun()

            # -------- EDIT --------
            with col2:
                if st.button("✏️ Editar", key=f"edit_{v['id']}"):
                    st.session_state.edit_id = v["id"]

            # -------- EDIT FORM --------
            if st.session_state.get("edit_id") == v["id"]:
                st.markdown("### ✏️ Editar veículo")

                emarca = st.text_input("Marca", v["marca"], key=f"m_{v['id']}")
                emodelo = st.text_input("Modelo", v["modelo"], key=f"mo_{v['id']}")
                epreco = st.number_input("Preço (€)", value=v["preco"], key=f"p_{v['id']}")
                evel = st.number_input("Velocidade", value=v["vel"], key=f"v_{v['id']}")

                econsumo = v.get("consumo")
                ecil = v.get("cilindrada")

                if v["tipo"] == "Carro" and v.get("eletrico"):
                    econsumo = st.number_input(
                        "Consumo (kWh/100km)", value=v["consumo"], key=f"c_{v['id']}"
                    )

                if v["tipo"] == "Mota":
                    ecil = st.number_input(
                        "Cilindrada (cc)", value=v["cilindrada"], key=f"cil_{v['id']}"
                    )

                if st.button("💾 Guardar", key=f"save_{v['id']}"):
                    if not emarca.strip() or not emodelo.strip() or epreco <= 0 or evel <= 0:
                        st.error("❌ Campos inválidos.")
                    else:
                        for x in frota:
                            if x["id"] == v["id"]:
                                x["marca"] = emarca
                                x["modelo"] = emodelo
                                x["preco"] = epreco
                                x["vel"] = evel
                                x["consumo"] = econsumo
                                x["cilindrada"] = ecil

                        save_local_storage(FROTA_KEY, frota)
                        del st.session_state.edit_id
                        st.success("✅ Atualizado no browser")
                        st.rerun()
