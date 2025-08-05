import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# === Authenticate with Google Sheets ===
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes = scope)
client = gspread.authorize(creds)

# Open the Google Sheet
try:
    sheet = client.open("maint_sheet").sheet1
except gspread.SpreadsheetNotFound:
    st.error("❌ Google Sheet 'maint_sheet' not found. Make sure it exists and is shared with your service account email.")
    st.stop()

# Streamlit UI 
st.set_page_config(page_title = "Maintenance Dashboard", layout = "wide")
st.title("🛠️ Maintenance Log Dashboard")

# === Form for new entry ===

st.subheader("➕ Aggiungi un nuovo intervento")
with st.form("log_form"):
    id_intervento = st.text_input("ID Intervento")
    sede = st.text_input("Sede Tecnica")
    asset = st.text_input("Seriale Asset")
    data_interv = st.date_input("Data Intervento")
    operatore = st.text_input("Operatore")
    intervento = st.text_input("Intervento")
    note = st.text_input("Note (facoltativo)")

    submitted = st.form_submit_button("Aggiungi")

    if submitted:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = [id_intervento, sede, asset, str(data_interv), operatore, intervento, note, timestamp]
        try:
            sheet.append_row(new_row)
            st.success("✅ Intervento aggiunto con successo!")
        except Exception as e:
            st.success(f"Errore nel salvataggio: {e}")
        
        else:
            st.warning("⚠️ Please fill in all fields before submitting.")


##################################################################


# --- Filters ---
data = sheet.get_all_values()
if data:
    df = pd.DataFrame(data[1:], columns = data[0])
    #df["Timestamp"] = pd.to_datetime(df)

    st.subheader("🔍 Filtra interventi")

    col1, col2 =st.columns(2)

    with col1:
        machine_filter = st.selectbox("Filter by machine", options=["All"] + sorted(df["Seriale Asset"].unique().tolist()))
    with col2:
        tech_filter = st.selectbox("Filter by technician", options=["All"] + sorted(df["Operatore"].unique().tolist()))

    date_range = st.date_input("Filter by date range", [])

    # Apply filters
    filtered_df = df.copy()
    if machine_filter != "All":
        filtered_df = filtered_df[filtered_df["Seriale Asset"] == machine_filter]
    if tech_filter != "All":
        filtered_df = filtered_df[filtered_df["Operatore"] == tech_filter]
    if len(date_range) == 2:
        start, end = pd.to_datetime(date_range)
        filtered_df = filtered_df[(filtered_df["Timestamp"] >= start) & (filtered_df["Timestamp"] <= end)]

    st.dataframe(filtered_df, use_container_width=True)


    # --- Download filtered data ---
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Scarica CSV", data=csv, file_name="interventi.csv")

    
else:
    st.info("Sheet is empty.")

