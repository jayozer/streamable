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

    st.caption("This is the associate list of `Agency`.")
    st.write("")

    """Add the employee_email and id and then pick a job function name for Agency Resware Associates"""

    # create an example list of data
    data_agency = [
        ['john.doe@musicprod.com', 1234567, 'Manager/Director'],
        ['jane.smith@musicprod.com', 2345678, 'Examiner']
    ]

    # create a pandas DataFrame with the specified column names
    df = pd.DataFrame(data_agency, columns=['employee_email', 'employee_id', 'team_name']) 
    # convert all columns to str
    df.employee_id = df.employee_id.astype(str) 
    df.employee_email = df.employee_email.astype(str)  

    df.job_function_name = df.job_function_name.astype("category")
    df.job_function_name = df.job_function_name.cat.add_categories(("Title Asisstant"))

    st.write("Edit the dataframe below for Job Function:")
    agency_associates = st.experimental_data_editor(
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

    if agency_associates is not None:
        st.download_button(
            "⬇️ Download agency associates list as .csv", agency_associates.to_csv(), "agency_associates.csv", use_container_width=True
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
    if button_clicked and agency_associates is not None:
        load_dataframe_to_snowflake_table(agency_associates, table, schema, user, password, account, warehouse, database)

if __name__ == "__main__":
    main()
