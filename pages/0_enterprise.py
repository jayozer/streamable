import streamlit as st
import pandas as pd


def main():
    st.set_page_config(layout="centered", page_title="Streamable", page_icon="🧮")
    st.title("✍️ Doma Streamable Data Editor")
    
    st.caption("This is the associate list of `Enterprise`.")

    st.write("")

    """Add the employee_email and id and then pick a jon function name for Enterprise Resware Associates"""

    # df = pd.DataFrame(
    #     [
    #         {"employee_email", "employee_id", "job_function_name"}
           
    #     ]
    # )


    # create an example list of data
    data_enterprise = [
        ['john.doe@musicprod.com', 1234567, 'Title & Curative'],
        ['jane.smith@musicprod.com', 2345678, 'Policy'],
        ['david.wong@musicprod.com', 3456789, 'Recording'],
        ['sarah.jones@musicprod.com', 4567890, 'Document Intake'],
        ['alex.garcia@musicprod.com', 5678901, 'Closing']
    ]

    # create a pandas DataFrame with the specified column names
    df = pd.DataFrame(data_enterprise, columns=['employee_email', 'employee_id', 'job_function_name']) 
    # convert all columns to str
    df.employee_id = df.employee_id.astype(str) 
    df.employee_email = df.employee_email.astype(str)  

    df.job_function_name = df.job_function_name.astype("category")
    df.job_function_name = df.job_function_name.cat.add_categories(("Compliance", "Scheduling", "Concierge", "Funding", "Post Closing"))

    st.write("Edit the dataframe below for Job Function:")
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

    # favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
    # st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

    st.download_button(
        "⬇️ Download resware associates list as .csv", resware_associates.to_csv(), "resware_associates.csv", use_container_width=True
    )
if __name__ == "__main__":
    main()
