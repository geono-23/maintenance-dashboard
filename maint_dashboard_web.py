import streamlit as st
import pandas as pd
import os

CSV_FILE = "MAINT_LIST.csv"
SEPARATOR = ","  # important for European Excel formats

# === Load data ===
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE, sep=SEPARATOR)
else:
    df = pd.DataFrame(columns=[
        "ID_INTERVENTO", "SEDE_TECNICA", "SN_ASSET",
        "DATA", "OPERATORE", "INTERVENTO", "NOTE"
    ])

st.set_page_config(page_title="Maintenance Dashboard", layout="wide")
st.title("🛠️ Maintenance Dashboard")

# === Add new manintenance entry ===

st.subheader("➕ Aggiungi un nuovo intervento")
with st.form("add_task_form", clear_on_submit = True):
    col1, col2 = st.columns(2)
    with col1:
        id_intervento = st.text_input("ID Intervento")
        asset = st.text_input("Seriale asset")
        data = st.date_input("Data intervento")
        operatore = st.text_input("Operatore")
    with col2:
        sede = st.text_input("Sede Tecnica")
        intervento = st.text_input("Intervento effettuato")
        note = st.text_input("Note (facoltativo)")

    submitted = st.form_submit_button("✅ Aggiungi")
    if submitted:
        new_entry = {
            "ID_INTERVENTO": id_intervento,
            "SEDE_TECNICA": sede,
            "SN_ASSET": asset,
            "DATA": data,
            "OPERATORE": operatore,
            "INTERVENTO": intervento,
            "NOTE": note,
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index = True)
        df.to_csv(CSV_FILE, index = False, sep = SEPARATOR)
        st.success("✅ Intervento aggiunto con successo!")
 

# === Filters ===
if not df.empty:
    st.subheader("🔍 Filtra interventi")
    filter_col1, filter_col2 =st.columns(2)

    asset_options = ["Tutti"] + sorted(df["SN_ASSET"].dropna().unique().tolist())
    operator_options = ["Tutti"] + sorted(df["OPERATORE"].dropna().unique().tolist())

    with filter_col1:
        selected_asset = st.selectbox("🔧 Asset", asset_options)
    with filter_col2:
        selected_operator = st.selectbox("👷‍♂️ Operatore", operator_options)

    filtered_df = df.copy()
    if selected_asset != "Tutti":
        filtered_df = filtered_df[filtered_df["SN_ASSET"] == selected_asset]
    if selected_operator != "Tutti":
        filtered_df = filtered_df[filtered_df["OPERATORE"] == selected_operator]

else:
    filtered_df = df
    st.info("📭 Nessun intervento ancora registrato.")


# === Display filtered results ===
st.subheader("📋 Interventi registrati")
st.dataframe(filtered_df, use_container_width = True)

# === Download button ===
if not filtered_df.empty:
    st.download_button(
        label = "📥 Scarica interventi filtrati (CSV)",
        data = filtered_df.to_csv(index = False, sep = SEPARATOR),
        file_name = "interventi_filtrati.csv"
    )

st.caption("App web di manutenzione")


