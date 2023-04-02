
# streamable
An Airtable data entery feature replacement with Streamlit and Snowflake
V1:
- Add Authorization page
- Side table list for Agency, Enterprise
- Add `Push to Snowflake` button. But this button only appears when Admin password is used.
- There should be Agency and Enterprise on side bar but both push into same Snowflake table.
- Each list - Enterprise and Agency should write to a different source but the Snowflake view should union them all. Thi way they are in dependent from each other

V2: 
Streamlit - experimental data editor add-ons