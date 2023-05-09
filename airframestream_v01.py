import streamlit as st
from snowflake.connector.pandas_tools import pd_writer
import pandas as pd
import os
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

# see all the deprecation warnings
os.environ["SQLALCHEMY_WARN_20"] = "1"  # Removes warning message in SQLAlchemy
st.set_page_config(layout="centered", page_title="Airframe-Stream", page_icon="👩🏻‍💻")
image = "images/icon_one.png"
st.image(image, width=100)

# st.title(f"My Title<img src='{image}' width='100' align='center'>".format(image))
st.title(':orange[Airframe-Stream: ] Ingest data into Snowflake ')


st.markdown("**:blue[TETime Employee Map:]** The list of `Enterprise` and `Agency` associates.", unsafe_allow_html=False, help="Enter the associate email, id and team name.")
st.caption("The data frame will be used to replace the current Airtable implementation.")

# Load authorized usernames and passwords from environment variables
user=os.getenv('SNOWFLAKE_USER')
password=os.getenv('SNOWFLAKE_PASSWORD') 
account=os.getenv('SNOWFLAKE_ACCOUNT')
database=os.getenv('SNOWFLAKE_DATABASE')
warehouse=os.getenv('SNOWFLAKE_WAREHOUSE')
schema=os.getenv('SNOWFLAKE_SCHEMA')
table=os.getenv('SNOWFLAKE_TABLE')
role=os.getenv('SNOWFLAKE_ROLE')
streamlit_user=os.getenv('STREAMLIT_USERNAME') # Ultimately this will be populated by an user account from AD.

#read from snowflake. Select the table and schema according to the sidebar radio button choice for sheets.
def read_from_snowflake_table(table, schema, user, password, account, warehouse, database):
    engine = create_engine('snowflake://{user}:{password}@{account_identifier}/?role={role}&warehouse={warehouse}'.format(
    user=user,
    password=password,
    account_identifier=account,
    role=role,
    warehouse=warehouse,
    database=database)
    )
    # use pandas DataFrame's read_sql method to query data from Snowflake
    df = pd.read_sql(f'SELECT * FROM {schema}.{table}', engine)
    return df    

# read the current table from snowflake
associates_df=read_from_snowflake_table(table, schema, user, password, account, warehouse, database)
# update the categories for the drop down menu in Streamlit front end.
associates_df['team_name'] = associates_df['team_name'].astype('category').cat.add_categories(["Rulebook Rumble", "Calendar Conga", "Service Shuffle", "Money Move", "Aftermath Party"])
# Assign the df to editable experimental data editor
associates = st.experimental_data_editor(
    data=associates_df,
    width=None,
    height=None,
    use_container_width=True,
    num_rows="dynamic",
    disabled=False,       
    key=None,
    on_change=None,
    args=None,
    kwargs=None,
    )

# Download option because people love to download. 
if associates is not None:
    st.download_button(
        "⬇ Download associates list as .csv", associates.to_csv(), "associates.csv", use_container_width=True
    )

# Push to Snwoflake - Right now it is a complete truncate and load but I need to merge the dataframes. 
# Using front end as the source of truth.
def load_dataframe_to_snowflake_table(df, table_name, schema_name, usr, pwd, acct, warehouse, database_name):
    engine = create_engine('snowflake://{user}:{password}@{account_identifier}/?role={role}&warehouse={warehouse}'.format(
    user=user,
    password=password,
    account_identifier=account,
    role=role,
    warehouse=warehouse,
    database=database)
    )
    # truncate the table in Snowflake using SQL
    with engine.begin() as conn: 
        conn.execute(f'TRUNCATE TABLE {schema}.{table}')

    # use pandas DataFrame's to_sql method to insert the data into Snowflake table
    df.to_sql(table_name, engine, schema=schema_name, if_exists='append', index=False)


#Call the function
button_clicked = st.button("Sync to Snowflake", use_container_width=True)
if button_clicked and associates is not None:
    load_dataframe_to_snowflake_table(associates, table, schema, user, password, account, warehouse, database)

