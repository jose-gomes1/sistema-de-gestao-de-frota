import streamlit as st
import json
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ----------------
st.set_page_config("Gestão de Frota")
st.title("🚗 Gestão de Frota (Client-side Persistente)")

FROTA_KEY = "frota_data"

# ---------------- INIT SESSION STATE ----------------
if "frota" not in st.session_state:
    st.session_state.frota = []

# ---------------- LOAD FROM localStorage (JS → Python) ----------------
components.html(
    f"""
    <script>
    const key = "{FROTA_KEY}";
    let data = localStorage.getItem(key);
    if (!data) {{
        localStorage.setItem(key, JSON.stringify([]));
        data = "[]";
    }}
    window.parent.postMessage({{
        type: "STREAMLIT_SET",
        key: "frota",
        value: JSON.parse(data)
    }}, "*");
    </script>
    """,
    height=0,
)

# ---------------- RECEIVE DATA FROM JS ----------------
if "streamlitMessage" not in st.session_state:
    st.session_state.streamlitMessage = None

components.html(
    """
    <script>
    window.addEventListener("message", (event) => {
        const out = document.getElementById("out");
        out.value = JSON.stringify(event.data);
        out.dispatchEvent(new Event("change"));
    });
    </script>
    <textarea id="out" style="display:none;"></textarea>
    """,
    height=0,
)

msg = st.session_state.get("streamlitMessage")
if isinstance(msg, dict) and msg.get("type") == "STREAMLIT_SET":
    st.session_state.frota = msg["value"]

frota = st.session_state.frota

# ---------------- SAVE TO localStorage (Python → JS) ----------------
def save_frota():
    components.html(
        f"""
        <script>
        localStorage.setItem("{FROTA_KEY}", JSON.stringify({json.dumps(st.session_state.frota)}));
        </script>
        """,
        height=0,
    )

# ---------------- ADD VEHICLE ----------------
st.subheader("➕ Adicionar veículo")

with st.form("add", clear_on_submit=True):
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

    if st.form_submit_button("Adicionar"):
        if not marca.strip() or not modelo.strip() or preco <= 0 or vel <= 0:
            st.error("❌ Preencha todos os campos.")
        elif tipo == "Carro" and eletrico and (not consumo or consumo <= 0):
            st.error("❌ Consumo inválido.")
        elif tipo == "Mota" and (not cilindrada or cilindrada <= 0):
            st.error("❌ Cilindrada inválida.")
        else:
            frota.append({
                "id": max([v["id"] for v in frota], default=0) + 1,
                "tipo": tipo,
                "marca": marca,
                "modelo": modelo,
                "preco": preco,
                "vel": vel,
                "eletrico": eletrico,
                "consumo": consumo,
                "cilindrada": cilindrada
            })
            save_frota()
            st.success("✅ Guardado permanentemente no browser")
            st.rerun()

# ---------------- LIST ----------------
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
                st.write(f"**Consumo:** {v['consumo']} kWh/100km")

            if v["tipo"] == "Mota":
                st.write(f"**Cilindrada:** {v['cilindrada']} cc")

            if st.button("❌ Remover", key=f"del_{v['id']}"):
                st.session_state.frota = [x for x in frota if x["id"] != v["id"]]
                save_frota()
                st.rerun()
