import streamlit as st
import pandas as pd
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
import json
import tempfile

# === Set page title ===
st.set_page_config(page_title = "Maintenance Dashboard", layout = "wide")
st.title("🔧 Maintenance Dashboard")

# === Authenticate with Google Sheets ===
creds_dict = dict(st.secrets["google_service_account"])

with tempfile.NamedTemporaryFile(mode = 'w', delete = False) as f:
    json.dump(creds_dict, f)
    f.flush()
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(f.name, scope)
    client = gspread.authorize(creds)

# === Load worksheet ===
try:
    sheet = client.open("maint_sheet").sheet1
except gspread.SpreadsheetNotFound:
    st.error("❌ Google Sheet not found. Check the name and sharing settings.")
    st.stop()

# === Read Existing Data === 
data = sheet.get_all_records()
df = pd.DataFrame(data)

# === Form for new entry ===
st.subheader("➕ Aggiungi un nuovo intervento")
with st.form("entry_form", clear_on_submit=True):
    id_intervento = st.text_input("ID Intervento")
    sede = st.text_input("Sede Tecnica")
    asset = st.text_input("Seriale Asset")
    data_interv = st.date_input("Data Intervento")
    operatore = st.text_input("Operatore")
    intervento = st.text_input("Intervento")
    note = st.text_input("Note (facoltativo)")

    submitted = st.form_submit_button("Aggiungi")

    if submitted:
        new_row = [id_intervento, sede, asset, str(data_interv), operatore, intervento, note]
        try:
            sheet.append_row(new_row)
            st.success("✅ Intervento aggiunto con successo!")
        except Exception as e:
            st.error(f"Errore nel salvataggio: {e}")

# --- Reload updated data ---
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Filters ---
st.subheader("🔍 Filtra interventi")

if not df.empty:
    assets = ["Tutti"] + sorted(df["Seriale Asset"].dropna().unique().tolist())
    operators = ["Tutti"] + sorted(df["Operatore"].dropna().unique().tolist())

    selected_asset = st.selectbox("📦 Filtro per asset", assets)
    selected_operator = st.selectbox("👷‍♂️ Filtro per operatore", operators)

    filtered_df = df.copy()
    if selected_asset != "Tutti":
        filtered_df = filtered_df[filtered_df["Seriale Asset"] == selected_asset]
    if selected_operator != "Tutti":
        filtered_df = filtered_df[filtered_df["Operatore"] == selected_operator]

    # --- Show table ---
    st.subheader("📋 Interventi registrati")
    st.dataframe(filtered_df, use_container_width=True)

    # --- Download filtered data ---
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Scarica CSV", data=csv, file_name="interventi.csv")
else:
    st.info("📭 Nessun intervento registrato ancora.")

