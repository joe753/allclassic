from sqlalchemy import create_engine, Table, Column
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Declare connection
mysql_url = "mysql+pymysql://root:allclassic@34.85.1.117/allclassic?charset=utf8"
engine = create_engine(mysql_url, echo=True, convert_unicode=True, pool_size=20, max_overflow=0)
# Declare & create Session
db_session = scoped_session( sessionmaker(autocommit=False, autoflush=False, bind=engine) )
# Create SqlAlchemy Base Instance
Base = declarative_base()
Base.query = db_session.query_property()

def init_database():
   Base.metadata.create_all(bind=engine)