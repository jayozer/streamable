
# streamable
An Airtable data entery feature replacement with Streamlit and Snowflake /n

V1:
+ Add Authorization page
+ Side table list for Agency, Enterprise
+ Add `Push to Snowflake` button. 
- `Push to Snowflake` only appears when Admin password is used.
+ There should be Agency and Enterprise on side bar but both push into same Snowflake table. (Solved by a view!)

V2: 
Streamlit - experimental data editor add-ons
- Add a check that counts if a name is added more then once. 
- LLM capability on names? Camel case?
- Check data types (numeric accepts numeric only)
- A way to track who made the change. Maybe get the login credentials and populate the audit fields automatically, including time of the add/ update. This way it will be complete replacement. 
- Change name to TE_Time_Employee_Map, remove agency and enterprise, add EDM Metadata section and under it addrogram_metadata_lkp, source_system_lkp, order_project_channel_map, order_statusgroup_Lkp
- Instead of creating an initial list of data, I should read what is in the DB.table first and display that in a editable data frame. Then I need to add to that and rerun......