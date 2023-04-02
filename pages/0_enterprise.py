import streamlit as st
from snowflake.connector.pandas_tools import pd_writer
import pandas as pd
import os
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

# see all the deprecation warnings
os.environ["SQLALCHEMY_WARN_20"] = "1"  

def main():
    st.set_page_config(layout="centered", page_title="Streamable Data Editor", page_icon="🧮")
    image = "images/dj1.jpeg"

    #st.title("My Title<img src='{}' width='100' align='center'>".format(image), unsafe_allow_html=True)

    st.caption("This is the associate list of `Enterprise`.")
    st.write("")

    """Add the employee_email and id and then pick a team name for Enterprise Resware Associates"""

    # create an example list of data
    data_enterprise = [
        ['john.doe@musicprod.com', 1234567, 'Ownership & Shuffle'],        
        ['jane.smith@musicprod.com', 2345678, 'Insurance Dance'],
        ['david.wong@musicprod.com', 3456789, 'Stampede'],
        ['sarah.jones@musicprod.com', 4567890, 'Paper Chase'],
        ['alex.garcia@musicprod.com', 5678901, 'Sign-Off']
    ]

    # create a pandas DataFrame with the specified column names
    df = pd.DataFrame(data_enterprise, columns=['employee_email', 'employee_id', 'team_name']) 
    # convert all columns to str
    df.employee_id = df.employee_id.astype(str) 
    df.employee_email = df.employee_email.astype(str)  
    df.team_name = df.team_name.astype("category")
    df.team_name = df.team_name.cat.add_categories(("Rulebook Rumble", "Calendar Conga", "Service Shuffle", "Money Move", "Aftermath Party"))

    st.write("Edit the dataframe below for Team:")
    resware_associates = st.experimental_data_editor(
        data=df,
        width=None,
        height=None,
        use_container_width=False,
        num_rows="dynamic",
        disabled=False,       
        key=None,
        on_change=None,
        args=None,
        kwargs=None,
    )

    if resware_associates is not None:
        st.download_button(
            "⬇️ Download resware associates list as .csv", resware_associates.to_csv(), "resware_associates.csv", use_container_width=True
        )

        user=os.getenv('SNOWFLAKE_USER')
        password=os.getenv('SNOWFLAKE_PASSWORD') 
        account=os.getenv('SNOWFLAKE_ACCOUNT')
        database=os.getenv('SNOWFLAKE_DATABASE')
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE')
        schema=os.getenv('SNOWFLAKE_SCHEMA')
        table=os.getenv('SNOWFLAKE_TABLE')
        role=os.getenv('SNOWFLAKE_ROLE')

        

        def load_dataframe_to_snowflake_table(df, table_name, schema_name, usr, pwd, acct, warehouse, database_name):
            engine = create_engine('snowflake://{user}:{password}@{account_identifier}/?role={role}&warehouse={warehouse}'.format(
            user=user,
            password=password,
            account_identifier=account,
            role=role,
            warehouse=warehouse)
            )
            # truncate the table in Snowflake using SQL
            with engine.begin() as conn: 
                conn.execute(f'TRUNCATE TABLE {schema}.{table}')

            # use pandas DataFrame's to_sql method to insert the data into Snowflake table
            df.to_sql(table_name, engine, schema=schema_name, if_exists='append', index=False)

            


    #Call the function
    button_clicked = st.button("Sync to Snowflake", use_container_width=True)
    if button_clicked and resware_associates is not None:
        load_dataframe_to_snowflake_table(resware_associates, table, schema, user, password, account, warehouse, database)

if __name__ == "__main__":
    main()
