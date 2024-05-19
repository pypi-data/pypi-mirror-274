from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

local_string_database_name = "lapa"

local_string_schema_name = "public"

Base = declarative_base(metadata=MetaData(schema=local_string_schema_name))

data_to_insert = []
