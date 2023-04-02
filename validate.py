#!/usr/bin/env python
from sqlalchemy import create_engine
import os

import dotenv
from dotenv import load_dotenv

load_dotenv()
# see all the deprecation warnings
os.environ["SQLALCHEMY_WARN_20"] = "1"


user=os.getenv('SNOWFLAKE_USER')
password=os.getenv('SNOWFLAKE_PASSWORD') 
account=os.getenv('SNOWFLAKE_ACCOUNT')
database=os.getenv('SNOWFLAKE_DATABASE')
warehouse=os.getenv('SNOWFLAKE_WAREHOUSE')
schema=os.getenv('SNOWFLAKE_SCHEMA')
table=os.getenv('SNOWFLAKE_TABLE')
role=os.getenv('SNOWFLAKE_ROLE')

# print(user)
# print(password)
# print(account)

engine = create_engine(
    'snowflake://{user}:{password}@{account_identifier}/?role={role}&warehouse={warehouse}'.format(
        user=user,
        password=password,
        account_identifier=account,
        role=role,
        warehouse=warehouse
    )
)

try:
    connection = engine.connect()
    results = connection.execute('select * from DEMO_DB.STREAMABLE.EMPLOYEE_JOB_FUNCTIONS').fetchone()
    print(results[0])
finally:
    connection.close()
    engine.dispose()

# engine = create_engine(
#     'snowflake://{user}:{password}@{account_identifier}/'.format(
#         user=user,
#         password=password,
#         account_identifier=account,
#     )
# )
# try:
#     connection = engine.connect()
#     results = connection.execute('select current_version()').fetchone()
#     print(results[0])
# finally:
#     connection.close()
#     engine.dispose()


#'snowflake://<user_login_name>:<password>@<account_identifier>/<database_name>/<schema_name>?warehouse=<warehouse_name>&role=<role_name>'