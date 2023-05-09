# streamlit_app.py

import streamlit as st

# Initialize connection.
conn_config = {
    "username": "DATAACROBAT",
    "password": "4!KwmRPcxgaKUdi",
    "account": "OHHXQVK-UPA17131",
    "database": "PETS",
    "schema": "PUBLIC",
    "dialect": "snowflake"
}
conn = st.experimental_connection('snowflake', type='sql', **conn_config)

# Perform query.
df = conn.query('SELECT * from EMPLOYEE_TEAM_AGENCY;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")
