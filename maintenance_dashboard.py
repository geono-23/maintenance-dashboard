import streamlit as st
import pandas as pd
import os

CSV_FILE = "MAINT_LIST.csv"

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns = ["ID_INTERVENTO", "SEDE_TECNICA", "SN_ASSET", "DATA", "OPERATORE", "INTERVENTO", "NOTE"])

st.title("Maintenance Dashboard")

#form to add new tasks
st.subheader("Aggiungi un nuovo intervento")
with st.form("add_task_form", clear_on_submit = True):
    id_intervento = st.text_input("Inserire ID dell'intervento")
    sede = st.text_input("Sede tecnica")
    asset = st.text_input("Seriale asset")
    data = st.date_input("Data dell'intervento")
    operatore = st.text_input("Nome Cognome dell'operatore")
    intervento = st.text_input("Intervento effettuato")
    note = st.text_input("Note (facoltativo)")
    submitted = st.form_submit_button("Aggiungi intervento")

    if submitted:
        new_task = {
            "ID_INTERVENTO": id_intervento,
            "SEDE_TECNICA": sede,
            "SN_ASSET": asset,
            "DATA": data,           
            "OPERATORE": operatore,
            "INTERVENTO": intervento,
            "NOTE": note,
        }
        df = pd.concat([df, pd.DataFrame([new_task])], ignore_index = True)
        df.to_csv(CSV_FILE, index = False)
        st.success("Intervento aggiunto correttamente!")

# Filter section
#st.subheader("View & Filter Tasks")       
#print(df.columns.tolist())
#filter_asset = st.multiselect("Filter by asset", df["SN_ASSET"].unique(), default = list(df["SN_ASSET"].unique()))
#filtered_df =df[df["SN_ASSET"].isin(filter_asset)]

# Display table 
#st.dataframe(filtered_df, use_container_width = True)
st.dataframe(df, use_container_width=True)


# Optional: download data
#st.download_button("Download CSV", data = filtered_df.to_csv(index = False), file_name = "filtered_tasks.csv")

#st.caption("Local Maintenance Dashboard App – Streamlit + CSV backend")

#python maintenance_dashboard.py