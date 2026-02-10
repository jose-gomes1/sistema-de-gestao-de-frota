import streamlit as st
from frota import Frota
from veiculo import Veiculo
from carro import Carro
from mota import Mota

st.set_page_config("Gestão de Frota")
st.title("🚗 Gestão de Frota")

# ---------------- FROTA ----------------
@st.cache_resource
def get_frota():
    return Frota()

frota = get_frota()

tab_add, tab_frota = st.tabs(["➕ Adicionar", "📋 Frota"])

# ================= ADD =================
with tab_add:
    tipo = st.selectbox("Tipo", ["Veículo", "Carro", "Mota"])
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    preco = st.number_input("Preço", min_value=0.0)
    vel = st.number_input("Velocidade", min_value=0)
    combustivel = st.selectbox("Combustível", ["Gasolina", "Gasóleo"])
    cor = st.color_picker("Cor")

    eletrico = False
    consumo = None
    cilindrada = None

    if tipo == "Carro":
        eletrico = st.checkbox("Elétrico")
        if eletrico:
            consumo = st.number_input("Consumo kWh/100km", min_value=0.0)
            combustivel = "Elétrico"  # override combustível automaticamente

    if tipo == "Mota":
        cilindrada = st.number_input("Cilindrada", min_value=0)

    if st.button("Adicionar"):
        if tipo == "Carro":
            v = Carro(marca, modelo, preco, vel, combustivel, cor, eletrico, consumo)
        elif tipo == "Mota":
            v = Mota(marca, modelo, preco, vel, combustivel, cor, cilindrada)
        else:
            v = Veiculo(tipo, marca, modelo, preco, vel, combustivel, cor)

        frota.adicionar_veiculo(v)
        
        # ✅ Mostra popup verde
        st.success("✅ Veículo adicionado com sucesso!")
        
        # Atualiza a lista de veículos sem apagar a mensagem
        # Podemos apenas recarregar os dados
        rows = frota.listar()

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
            if v['eletrico']:
                st.markdown(f"**Consumo:** {v['consumo']} kWh/100km")
            if v['cilindrada']:
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
                ecomb = st.text_input("Combustível", v["combustivel"], key=f"c_{v['id']}")
                ecor = st.color_picker("Cor", v["cor"], key=f"cor_{v['id']}")
                
                if st.button("💾 Guardar", key=f"save_{v['id']}"):
                    frota.atualizar(v["id"], emarca, emodelo, epreco, evel, ecomb, ecor)
                    del st.session_state.edit_id
                    st.success("✅ Veículo atualizado!")
                    st.rerun()
